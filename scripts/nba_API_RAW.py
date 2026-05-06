"""
nba_API_RAW.py

Pulls NBA player statistics from the official NBA API for the 2024-25 regular
season. Pulls two views and saves them separately:
    1. Base stats (traditional box score) -> nba_player_stats.csv
    2. Advanced stats (efficiency metrics, on/off ratings, usage)
       -> nba_player_advanced.csv

The two files are merged on PLAYER_ID downstream in data_cleaning.py.

Outputs:
    data/raw/nba_player_stats.csv
    data/raw/nba_player_advanced.csv
"""

import time
from pathlib import Path

import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

# Config
SEASON = "2024-25"
SEASON_TYPE = "Regular Season"

OUT_DIR = Path("data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_OUT = OUT_DIR / "nba_player_stats.csv"
ADV_OUT = OUT_DIR / "nba_player_advanced.csv"


# Pull base/traditional stats
print(f"Pulling base stats for {SEASON} ({SEASON_TYPE})...")
base = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON,
    season_type_all_star=SEASON_TYPE,
    measure_type_detailed_defense="Base",
)
base_df = base.get_data_frames()[0]
base_df.to_csv(BASE_OUT, index=False)
print(f"  Saved {len(base_df)} rows -> {BASE_OUT}")

time.sleep(1)


# 2. Pull advanced stats
print(f"\nPulling advanced stats for {SEASON} ({SEASON_TYPE})...")
adv = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON,
    season_type_all_star=SEASON_TYPE,
    measure_type_detailed_defense="Advanced",
)
adv_df = adv.get_data_frames()[0]
adv_df.to_csv(ADV_OUT, index=False)
print(f"  Saved {len(adv_df)} rows -> {ADV_OUT}")

print("\nDone.")