import pandas as pd

contracts = pd.read_csv("data/nba_contracts_raw.csv")
stats = pd.read_csv("data/nba_player_stats.csv")

print(contracts.head())
print(stats.head())

print(contracts.info())
print(stats.info())

print(contracts.isnull().sum())
print(stats.isnull().sum())

contracts.columns = contracts.columns.str.strip().str.lower().str.replace(" ", "_")
stats.columns = stats.columns.str.strip().str.lower().str.replace(" ", "_")

contracts["salary"] = (
    contracts["salary"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

contracts["salary"] = pd.to_numeric(contracts["salary"], errors="coerce")

print(contracts[contracts["salary"].isnull()])

contracts = contracts.dropna(subset=["player_name", "salary"])
stats = stats.dropna(subset=["player_name"])

contracts["player_name"] = contracts["player_name"].str.strip().str.lower()
stats["player_name"] = stats["player_name"].str.strip().str.lower()

stats = stats[stats["gp"] >= 8]  # gp = games played

contracts.to_csv("data/processed/cleaned_contracts.csv", index=False)
stats.to_csv("data/processed/cleaned_stats.csv", index=False)
