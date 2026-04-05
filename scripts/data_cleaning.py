import pandas as pd
from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)

stats = pd.read_csv("data/raw/nba_player_stats.csv")
contracts = pd.read_csv("data/raw/nba_contracts_raw.csv")

# Inspect missing values
print("Missing values in stats:")
print(stats.isnull().sum())
print("\nMissing values in contracts:")
print(contracts.isnull().sum())

# Keeping useful columns
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

# Renaming columns
stats = stats.rename(columns={
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
})

contracts = contracts.rename(columns={
    "Player": "player_name",
    "Tm": "team",
    "2025-26": "salary",
    "Guaranteed": "guaranteed",
})

# Clean player names
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

# Drop rows with missing values
stats = stats.dropna(subset=["player_name", "gp"])
contracts = contracts.dropna(subset=["player_name", "salary"])

# Filter out players with fewer than 8 games
stats = stats[stats["gp"] >= 8]

# Add season column
stats["season"] = "2025-26"
contracts["season"] = "2025-26"

# Save cleaned files
stats.to_csv("data/processed/nba_player_stats_cleaned.csv", index=False)
contracts.to_csv("data/processed/nba_contracts_cleaned.csv", index=False)

print("Saved:")
print("- data/processed/nba_player_stats_cleaned.csv")
print("- data/processed/nba_contracts_cleaned.csv")