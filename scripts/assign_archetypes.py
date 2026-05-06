"""
assign_archetypes.py

Assigns each player in the merged dataset to one of eight archetypes based on
per-game stats, advanced metrics, age, and salary. Computes an updated EtD
ratio using the NBA's PIE (Player Impact Estimate) metric.

Archetypes (applied in priority order, first match wins):
    1. Rookie Contributor       - young (<= 22), regardless of role
    2. Veteran Star             - age >= 28, heavy minutes, top salary
    3. Prime Star               - age 23-27, heavy minutes, mid-high salary
    4. 3-and-D Wing             - high 3PT volume + efficiency, good defense, low usage
    5. High-Volume Scorer       - high usage and scoring (didn't fit star buckets)
    6. Sixth Man / Bench Scorer - high-usage off the bench, mid points
    7. Defensive Specialist     - elite defense, low usage, plays meaningful minutes
    8. Role Player              - catch-all

Design notes:
    - Per-game stats normalize for games missed.
    - 3-and-D defensive threshold uses the league median DEF_RATING.
    - Defensive Specialist threshold uses the league 25th percentile DEF_RATING
      (top quarter of defenders, since lower is better).
    - The EtD ratio uses PIE, the NBA's all-in-one production metric.

Inputs:
    data/processed/nba_merged.csv

Outputs:
    data/processed/nba_merged_with_archetypes.csv
    data/processed/archetype_summary.csv
"""

import os
import sys
from pathlib import Path

import pandas as pd

# Force UTF-8 output so terminal doesn't crash on accented player names
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

MERGED_IN = Path("data/processed/nba_merged.csv")
MERGED_OUT = Path("data/processed/nba_merged_with_archetypes.csv")
SUMMARY_OUT = Path("data/processed/archetype_summary.csv")


# Archetype thresholds
ROOKIE_MAX_AGE = 22

VETERAN_MIN_AGE = 28
VETERAN_MIN_MINUTES_PG = 28
VETERAN_MIN_SALARY = 20_000_000

PRIME_STAR_MIN_AGE = 23
PRIME_STAR_MAX_AGE = 27
PRIME_STAR_MIN_MINUTES_PG = 28
PRIME_STAR_MIN_SALARY = 15_000_000

THREE_AND_D_MIN_FG3A_PG = 3.5
THREE_AND_D_MIN_FG3_PCT = 0.35
THREE_AND_D_MAX_USAGE = 0.20

HIGH_VOLUME_MIN_USAGE = 0.25
HIGH_VOLUME_MIN_PTS_PG = 18

SIXTH_MAN_MIN_USAGE = 0.20
SIXTH_MAN_MIN_PTS_PG = 12
SIXTH_MAN_MAX_MINUTES_PG = 28

DEF_SPECIALIST_MAX_USAGE = 0.18
DEF_SPECIALIST_MIN_MINUTES_PG = 15

# Load
print("Loading merged dataset...")
df = pd.read_csv(MERGED_IN)
print(f"  {len(df)} rows")


# Compute league percentile thresholds for DEF_RATING
# (Lower DEF_RATING = better defense.)
DEF_RATING_MEDIAN = df["def_rating"].median()
DEF_RATING_TOP_QUARTILE = df["def_rating"].quantile(0.25)

print(f"League median DEF_RATING:        {DEF_RATING_MEDIAN:.2f} (3-and-D threshold)")
print(f"League 25th percentile DEF_RATING: {DEF_RATING_TOP_QUARTILE:.2f} (Def. Specialist threshold)")


# Assign archetypes
def assign_archetype(row: pd.Series) -> str:
    """Return the archetype label for a single player row."""
    # 1. Rookie Contributor
    if row["age"] <= ROOKIE_MAX_AGE:
        return "Rookie Contributor"

    # 2. Veteran Star
    if (
        row["age"] >= VETERAN_MIN_AGE
        and row["minutes_pg"] >= VETERAN_MIN_MINUTES_PG
        and row["salary"] >= VETERAN_MIN_SALARY
    ):
        return "Veteran Star"

    # 3. Prime Star
    if (
        PRIME_STAR_MIN_AGE <= row["age"] <= PRIME_STAR_MAX_AGE
        and row["minutes_pg"] >= PRIME_STAR_MIN_MINUTES_PG
        and row["salary"] >= PRIME_STAR_MIN_SALARY
    ):
        return "Prime Star"

    # 4. 3-and-D Wing
    if (
        row["fg3a_pg"] >= THREE_AND_D_MIN_FG3A_PG
        and row["fg3_pct"] >= THREE_AND_D_MIN_FG3_PCT
        and row["def_rating"] <= DEF_RATING_MEDIAN
        and row["usage_pct"] < THREE_AND_D_MAX_USAGE
    ):
        return "3-and-D Wing"

    # 5. High-Volume Scorer
    if (
        row["usage_pct"] >= HIGH_VOLUME_MIN_USAGE
        and row["points_pg"] >= HIGH_VOLUME_MIN_PTS_PG
    ):
        return "High-Volume Scorer"

    # 6. Sixth Man / Bench Scorer
    if (
        row["usage_pct"] >= SIXTH_MAN_MIN_USAGE
        and row["points_pg"] >= SIXTH_MAN_MIN_PTS_PG
        and row["minutes_pg"] < SIXTH_MAN_MAX_MINUTES_PG
    ):
        return "Sixth Man"

    # 7. Defensive Specialist
    if (
        row["def_rating"] <= DEF_RATING_TOP_QUARTILE
        and row["usage_pct"] < DEF_SPECIALIST_MAX_USAGE
        and row["minutes_pg"] >= DEF_SPECIALIST_MIN_MINUTES_PG
    ):
        return "Defensive Specialist"

    # 8. Role Player (catch-all)
    return "Role Player"


df["archetype"] = df.apply(assign_archetype, axis=1)


# Recompute EtD using PIE
df["pie_x100"] = df["pie"] * 100
df["etd_pie"] = df["pie_x100"] / df["salary_millions"].replace(0, pd.NA)


# Per-archetype summary
summary = (
    df.groupby("archetype")
    .agg(
        n_players=("player_name", "count"),
        avg_age=("age", "mean"),
        avg_minutes_pg=("minutes_pg", "mean"),
        avg_points_pg=("points_pg", "mean"),
        avg_usage_pct=("usage_pct", "mean"),
        avg_pie=("pie", "mean"),
        avg_def_rating=("def_rating", "mean"),
        avg_salary=("salary", "mean"),
        median_salary=("salary", "median"),
        avg_etd_pie=("etd_pie", "mean"),
        median_etd_pie=("etd_pie", "median"),
    )
    .round(3)
    .sort_values("avg_etd_pie", ascending=False)
)


# Save outputs
df.to_csv(MERGED_OUT, index=False)
summary.to_csv(SUMMARY_OUT)

print(f"\nSaved enriched merged dataset -> {MERGED_OUT}")
print(f"Saved archetype summary       -> {SUMMARY_OUT}")


# Print summary
print("\n" + "=" * 70)
print("ARCHETYPE DISTRIBUTION")
print("=" * 70)
print(df["archetype"].value_counts().to_string())

print("\n" + "=" * 70)
print("ARCHETYPE SUMMARY (sorted by avg EtD-PIE, best value first)")
print("=" * 70)
print(summary.to_string())

print("\n" + "=" * 70)
print("TOP 5 PLAYERS BY EtD-PIE WITHIN EACH ARCHETYPE")
print("=" * 70)
for archetype in df["archetype"].value_counts().index:
    subset = df[df["archetype"] == archetype].nlargest(5, "etd_pie")
    print(f"\n{archetype}:")
    print(
        subset[["player_name", "age", "salary", "pie", "etd_pie"]]
        .round(3)
        .to_string(index=False)
    )