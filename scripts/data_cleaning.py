"""
data_cleaning.py

Cleans the raw NBA player stats and contracts datasets and saves processed
versions ready for integration. Now includes advanced stats merged into the
player stats output.

Operations:
    - Loads base stats and advanced stats from the API
    - Merges them on PLAYER_ID into a single stats dataframe
    - Selects useful columns from both
    - Standardizes column names (snake_case)
    - Computes per-game versions of counting stats
    - Strips whitespace from player names
    - Converts salary strings ('$1,234,567') to numeric values
    - Drops rows missing critical fields
    - Filters out players with fewer than MIN_GAMES_PLAYED games
    - Deduplicates contracts (Basketball Reference lists one row per future
      contract year per player)

Inputs:
    data/raw/nba_player_stats.csv
    data/raw/nba_player_advanced.csv
    data/raw/nba_contracts_raw.csv

Outputs:
    data/processed/nba_player_stats_cleaned.csv
    data/processed/nba_contracts_cleaned.csv
"""

import os
from pathlib import Path

import pandas as pd

# Resolve paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

# Config
STATS_RAW = Path("data/raw/nba_player_stats.csv")
ADVANCED_RAW = Path("data/raw/nba_player_advanced.csv")
CONTRACTS_RAW = Path("data/raw/nba_contracts_raw.csv")
STATS_OUT = Path("data/processed/nba_player_stats_cleaned.csv")
CONTRACTS_OUT = Path("data/processed/nba_contracts_cleaned.csv")

MIN_GAMES_PLAYED = 8
SEASON_LABEL = "2025-26"

Path("data/processed").mkdir(parents=True, exist_ok=True)


# Load
print("Loading raw datasets...")
stats = pd.read_csv(STATS_RAW)
advanced = pd.read_csv(ADVANCED_RAW)
contracts = pd.read_csv(CONTRACTS_RAW)
print(f"  base stats:     {len(stats)} rows")
print(f"  advanced stats: {len(advanced)} rows")
print(f"  contracts:      {len(contracts)} rows")


# PLAYER_ID is the merge key.
adv_cols_keep = [
    "PLAYER_ID",
    "OFF_RATING",
    "DEF_RATING",
    "NET_RATING",
    "USG_PCT",
    "TS_PCT",
    "PIE",  # Player Impact Estimate (NBA's all-in-one production metric)
    "AST_PCT",
    "REB_PCT",
]
# Defensive: only keep columns that actually exist in the API
adv_cols_keep = [c for c in adv_cols_keep if c in advanced.columns]
advanced = advanced[adv_cols_keep]

stats = stats.merge(advanced, on="PLAYER_ID", how="left")
print(f"\nAfter merging advanced stats: {len(stats)} rows")


# Inspect missing values (for the data quality writeup)
print("\nMissing values in stats (post-merge):")
print(stats.isnull().sum())
print("\nMissing values in contracts:")
print(contracts.isnull().sum())


# Select useful columns
base_cols = [
    "PLAYER_ID",
    "PLAYER_NAME",
    "TEAM_ABBREVIATION",
    "AGE",
    "GP",
    "MIN",
    "PTS",
    "REB",
    "AST",
    "STL",
    "BLK",
    "FG_PCT",
    "FG3_PCT",
    "FG3A",   # 3-point attempts (used to identify 3-and-D archetype)
    "FT_PCT",
    "PLUS_MINUS",
]
keep_cols = base_cols + adv_cols_keep[1:]  # skip PLAYER_ID dup
keep_cols = [c for c in keep_cols if c in stats.columns]
stats = stats[keep_cols]

contracts = contracts[
    [
        "Player",
        "Tm",
        "2025-26",
        "Guaranteed",
    ]
]


# Rename columns to snake_case
stats = stats.rename(
    columns={
        "PLAYER_ID": "player_id",
        "PLAYER_NAME": "player_name",
        "TEAM_ABBREVIATION": "team",
        "AGE": "age",
        "GP": "gp",
        "MIN": "minutes",
        "PTS": "points",
        "REB": "rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "FG_PCT": "fg_pct",
        "FG3_PCT": "fg3_pct",
        "FG3A": "fg3a",
        "FT_PCT": "ft_pct",
        "PLUS_MINUS": "plus_minus",
        "OFF_RATING": "off_rating",
        "DEF_RATING": "def_rating",
        "NET_RATING": "net_rating",
        "USG_PCT": "usage_pct",
        "TS_PCT": "true_shooting_pct",
        "PIE": "pie",
        "AST_PCT": "ast_pct",
        "REB_PCT": "reb_pct",
    }
)

contracts = contracts.rename(
    columns={
        "Player": "player_name",
        "Tm": "team",
        "2025-26": "salary",
        "Guaranteed": "guaranteed",
    }
)


# Per-game versions of counting stats

per_game_cols = ["points", "rebounds", "assists", "steals", "blocks", "fg3a", "minutes"]
for col in per_game_cols:
    if col in stats.columns:
        stats[f"{col}_pg"] = (stats[col] / stats["gp"]).round(2)


# Clean player names (strip whitespace; full normalization happens in
# data_integration.py)
stats["player_name"] = stats["player_name"].astype(str).str.strip()
contracts["player_name"] = contracts["player_name"].astype(str).str.strip()


# Clean salary columns
for col in ["salary", "guaranteed"]:
    contracts[col] = (
        contracts[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("", pd.NA)
    )
    contracts[col] = pd.to_numeric(contracts[col], errors="coerce")


# Drop rows with missing critical fields
before_stats = len(stats)
stats = stats.dropna(subset=["player_name", "gp"])
print(f"\nDropped {before_stats - len(stats)} stats rows with missing player_name/gp")

before_contracts = len(contracts)
contracts = contracts.dropna(subset=["player_name", "salary"])
print(f"Dropped {before_contracts - len(contracts)} contracts rows with missing player_name/salary")


# Filter out players with fewer than MIN_GAMES_PLAYED games
before = len(stats)
stats = stats[stats["gp"] >= MIN_GAMES_PLAYED]
print(f"Filtered out {before - len(stats)} stats rows with fewer than {MIN_GAMES_PLAYED} games played")

MIN_TOTAL_MINUTES = 250

before = len(stats)
stats = stats[stats["minutes"] >= MIN_TOTAL_MINUTES]
print(f"Filtered out {before - len(stats)} stats rows with fewer than {MIN_TOTAL_MINUTES} minutes played")

before = len(contracts)
contracts = (
    contracts.sort_values("guaranteed", ascending=False, na_position="last")
    .drop_duplicates(subset=["player_name"], keep="first")
    .reset_index(drop=True)
)
print(f"Deduplicated contracts: {before} -> {len(contracts)} rows ({before - len(contracts)} duplicates removed)")

# Defensive dedup of stats
before = len(stats)
stats = (
    stats.sort_values("gp", ascending=False)
    .drop_duplicates(subset=["player_name"], keep="first")
    .reset_index(drop=True)
)
print(f"Deduplicated stats: {before} -> {len(stats)} rows ({before - len(stats)} duplicates removed)")


# Add season column
stats["season"] = SEASON_LABEL
contracts["season"] = SEASON_LABEL


# Save
stats.to_csv(STATS_OUT, index=False)
contracts.to_csv(CONTRACTS_OUT, index=False)

print("\nSaved:")
print(f"  {STATS_OUT}  ({len(stats)} rows, {len(stats.columns)} cols)")
print(f"  {CONTRACTS_OUT}  ({len(contracts)} rows)")
print("\nDone.")