"""
data_integration.py

Integrates the cleaned NBA player stats and contracts datasets into a single
merged dataset using normalized player names as the join key. Handles naming
inconsistencies through normalization and fuzzy matching.

Inputs:
    data/processed/nba_player_stats_cleaned.csv
    data/processed/nba_contracts_cleaned.csv

Outputs:
    data/processed/nba_merged.csv          (analysis-ready integrated dataset)
    data/processed/unmatched_players.csv   (rows that failed to match, for QA)
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd
from rapidfuzz import process, fuzz


STATS_PATH = Path("data/processed/nba_player_stats_cleaned.csv")
CONTRACTS_PATH = Path("data/processed/nba_contracts_cleaned.csv")
MERGED_OUT = Path("data/processed/nba_merged.csv")
UNMATCHED_OUT = Path("data/processed/unmatched_players.csv")

FUZZY_THRESHOLD = 90

def normalize_name(name: str) -> str:
    """
    Standardize a player name for matching.
    - Lowercase
    - Strip accents (Dončić -> doncic)
    - Remove punctuation (P.J. -> pj)
    - Remove suffixes (Jr., Sr., II, III, IV)
    - Collapse whitespace
    """
    if not isinstance(name, str):
        return ""
    
    # Strip accents
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))

    # Lowercase
    name = name.lower()

    # Remove suffixes
    name = re.sub(r"\b(jr|sr|ii|iii|iv)\.?\b", "", name)

    # Remove punctuation
    name = re.sub(r"[^\w\s]", "", name)

    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()

    return name

print("Loading cleaned datasets...")
stats = pd.read_csv(STATS_PATH)
contracts = pd.read_csv(CONTRACTS_PATH)

print(f"  stats:     {len(stats)} rows")
print(f"  contracts: {len(contracts)} rows")

# Add normalized name column to both
stats["name_norm"] = stats["player_name"].apply(normalize_name)
contracts["name_norm"] = contracts["player_name"].apply(normalize_name)

# Step 1: Exact merge on normalized name
contracts_renamed = contracts.rename(columns={"team": "team_contract"})
stats_renamed = stats.rename(columns={"team": "team_stats"})

exact_merged = stats_renamed.merge(
    contracts_renamed.drop(columns=["player_name", "season"]),
    on="name_norm",
    how="inner",
)

print(f"\nExact match: {len(exact_merged)} rows merged")

matched_norms = set(exact_merged["name_norm"])
stats_unmatched = stats_renamed[~stats_renamed["name_norm"].isin(matched_norms)].copy()
contracts_unmatched = contracts_renamed[
    ~contracts_renamed["name_norm"].isin(matched_norms)
].copy()

print(f"  unmatched stats players:     {len(stats_unmatched)}")
print(f"  unmatched contracts players: {len(contracts_unmatched)}")

# Step 2: Fuzzy match the leftovers
print(f"\nFuzzy matching leftovers (threshold={FUZZY_THRESHOLD})...")

contract_choices = contracts_unmatched["name_norm"].tolist()
fuzzy_rows = []
fuzzy_log = []  # for printing what got matched, useful for the report

for _, stat_row in stats_unmatched.iterrows():
    stat_name = stat_row["name_norm"]
    if not stat_name or not contract_choices:
        continue

    match = process.extractOne(
        stat_name, contract_choices, scorer=fuzz.token_sort_ratio
    )
    if match is None:
        continue

    matched_name, score, _ = match
    if score >= FUZZY_THRESHOLD:
        contract_row = contracts_unmatched[
            contracts_unmatched["name_norm"] == matched_name
        ].iloc[0]

        combined = stat_row.to_dict()
        for col in contracts_unmatched.columns:
            if col in ("player_name", "season", "name_norm"):
                continue
            combined[col] = contract_row[col]

        fuzzy_rows.append(combined)
        fuzzy_log.append((stat_row["player_name"], contract_row["player_name"], score))

fuzzy_merged = pd.DataFrame(fuzzy_rows)

print(f"  matched via fuzzy: {len(fuzzy_merged)}")
if fuzzy_log:
    print("  examples:")
    for stat_n, contract_n, score in fuzzy_log[:10]:
        print(f"    {stat_n!r}  <->  {contract_n!r}  (score={score})")
        
# Step 3: Combine exact + fuzzy
merged = pd.concat([exact_merged, fuzzy_merged], ignore_index=True)

# Drop the helper column before saving
merged = merged.drop(columns=["name_norm"])

print(f"\nFinal merged dataset: {len(merged)} rows")

# Step 4: Compute Efficiency-to-Dollar (EtD) ratio
# Simple production score from the columns we have. You can refine this once
# you pull advanced stats. The point here is to have *something* computable
# from current data so the pipeline runs end-to-end.
#
# production_score is per-game. We then divide by salary in millions to get
# a ratio that is intuitive: "production points per million dollars."
merged["production_score"] = (
    merged["points"]
    + 1.2 * merged["rebounds"]
    + 1.5 * merged["assists"]
    + 2.0 * merged["steals"]
    + 2.0 * merged["blocks"]
)

merged["salary_millions"] = merged["salary"] / 1_000_000
# Avoid division by zero for minimum-salary edge cases
merged["etd_ratio"] = merged["production_score"] / merged["salary_millions"].replace(
    0, pd.NA
)

# Step 5: Save outputs
MERGED_OUT.parent.mkdir(parents=True, exist_ok=True)
merged.to_csv(MERGED_OUT, index=False)
print(f"\nSaved merged dataset -> {MERGED_OUT}")

# Track what didn't match for the data quality writeup
matched_norms_final = set(
    pd.concat([exact_merged["name_norm"], fuzzy_merged.get("name_norm", pd.Series(dtype=str))])
)

still_unmatched_stats = stats[~stats["name_norm"].isin(matched_norms_final)].copy()
still_unmatched_contracts = contracts[
    ~contracts["name_norm"].isin(matched_norms_final)
].copy()

still_unmatched_stats["source"] = "stats"
still_unmatched_contracts["source"] = "contracts"

unmatched = pd.concat(
    [still_unmatched_stats, still_unmatched_contracts], ignore_index=True
)
unmatched.to_csv(UNMATCHED_OUT, index=False)
print(f"Saved unmatched rows -> {UNMATCHED_OUT}")

print("\nDone.")