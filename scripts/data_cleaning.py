"""
data_cleaning.py

Cleans the raw NBA player stats and contracts datasets and saves processed
versions ready for integration.

Operations:
    - Selects useful columns
    - Standardizes column names (snake_case)
    - Strips whitespace from player names
    - Converts salary strings ('$1,234,567') to numeric values
    - Drops rows missing critical fields (player_name, salary, gp)
    - Filters out players with fewer than 8 games (low-sample noise)
    - Deduplicates contracts (Basketball Reference lists one row per future
      contract year per player; we collapse to one row per player)
    - Adds a season column for downstream joins

Inputs:
    data/raw/nba_player_stats.csv
    data/raw/nba_contracts_raw.csv

Outputs:
    data/processed/nba_player_stats_cleaned.csv
    data/processed/nba_contracts_cleaned.csv
"""

import os
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Resolve paths relative to project root, regardless of where script is run
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
STATS_RAW = Path("data/raw/nba_player_stats.csv")
CONTRACTS_RAW = Path("data/raw/nba_contracts_raw.csv")
STATS_OUT = Path("data/processed/nba_player_stats_cleaned.csv")
CONTRACTS_OUT = Path("data/processed/nba_contracts_cleaned.csv")

MIN_GAMES_PLAYED = 8  # filter out small-sample players
SEASON_LABEL = "2025-26"

# Ensure output directory exists
Path("data/processed").mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
print("Loading raw datasets...")
stats = pd.read_csv(STATS_RAW)
contracts = pd.read_csv(CONTRACTS_RAW)
print(f"  stats:     {len(stats)} rows")
print(f"  contracts: {len(contracts)} rows")


# ---------------------------------------------------------------------------
# Inspect missing values (for the data quality writeup)
# ---------------------------------------------------------------------------
print("\nMissing values in stats:")
print(stats.isnull().sum())
print("\nMissing values in contracts:")
print(contracts.isnull().sum())


# ---------------------------------------------------------------------------
# Select useful columns
# ---------------------------------------------------------------------------
stats = stats[
    [
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
        "FT_PCT",
        "PLUS_MINUS",
    ]
]

contracts = contracts[
    [
        "Player",
        "Tm",
        "2025-26",
        "Guaranteed",
    ]
]


# ---------------------------------------------------------------------------
# Rename columns to snake_case for consistency
# ---------------------------------------------------------------------------
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
        "FT_PCT": "ft_pct",
        "PLUS_MINUS": "plus_minus",
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


# ---------------------------------------------------------------------------
# Clean player names (strip whitespace; keeps original casing/punctuation
# since name normalization for matching happens in data_integration.py)
# ---------------------------------------------------------------------------
stats["player_name"] = stats["player_name"].astype(str).str.strip()
contracts["player_name"] = contracts["player_name"].astype(str).str.strip()


# ---------------------------------------------------------------------------
# Clean salary columns: strip '$' and ',' then convert to numeric
# ---------------------------------------------------------------------------
for col in ["salary", "guaranteed"]:
    contracts[col] = (
        contracts[col]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("", pd.NA)
    )
    contracts[col] = pd.to_numeric(contracts[col], errors="coerce")


# ---------------------------------------------------------------------------
# Drop rows with missing critical fields
# ---------------------------------------------------------------------------
before_stats = len(stats)
stats = stats.dropna(subset=["player_name", "gp"])
print(f"\nDropped {before_stats - len(stats)} stats rows with missing player_name/gp")

before_contracts = len(contracts)
contracts = contracts.dropna(subset=["player_name", "salary"])
print(f"Dropped {before_contracts - len(contracts)} contracts rows with missing player_name/salary")


# ---------------------------------------------------------------------------
# Filter out players with fewer than MIN_GAMES_PLAYED games (low-sample noise)
# ---------------------------------------------------------------------------
before = len(stats)
stats = stats[stats["gp"] >= MIN_GAMES_PLAYED]
print(f"Filtered out {before - len(stats)} stats rows with fewer than {MIN_GAMES_PLAYED} games played")


# ---------------------------------------------------------------------------
# Deduplicate contracts
#
# Basketball Reference's contracts table includes one row per future contract
# year per player. The annual salary is the same across these rows, but the
# "Guaranteed" amount varies year-to-year (early years are typically fully
# guaranteed; later years often have team options or partial guarantees).
#
# Because our research question concerns ROI for the 2025-26 season
# specifically, we collapse to a single row per player and keep the row with
# the highest guaranteed amount, which represents the most committed year of
# the contract.
# ---------------------------------------------------------------------------
before = len(contracts)
contracts = (
    contracts.sort_values("guaranteed", ascending=False, na_position="last")
    .drop_duplicates(subset=["player_name"], keep="first")
    .reset_index(drop=True)
)
print(f"Deduplicated contracts: {before} -> {len(contracts)} rows ({before - len(contracts)} duplicates removed)")

# Defensive dedup of stats too (the NBA API shouldn't return duplicates, but
# this catches any unexpected issues and keeps the pipeline robust).
before = len(stats)
stats = (
    stats.sort_values("gp", ascending=False)
    .drop_duplicates(subset=["player_name"], keep="first")
    .reset_index(drop=True)
)
print(f"Deduplicated stats: {before} -> {len(stats)} rows ({before - len(stats)} duplicates removed)")


# ---------------------------------------------------------------------------
# Add season column for downstream joins / multi-season analyses
# ---------------------------------------------------------------------------
stats["season"] = SEASON_LABEL
contracts["season"] = SEASON_LABEL


# ---------------------------------------------------------------------------
# Save cleaned files
# ---------------------------------------------------------------------------
stats.to_csv(STATS_OUT, index=False)
contracts.to_csv(CONTRACTS_OUT, index=False)

print("\nSaved:")
print(f"  {STATS_OUT}  ({len(stats)} rows)")
print(f"  {CONTRACTS_OUT}  ({len(contracts)} rows)")
print("\nDone.")