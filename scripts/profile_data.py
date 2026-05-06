"""
profile_data.py

Profiles the cleaned and integrated NBA datasets to generate the numbers
needed for the README's "Data quality" section. Outputs both stdout summary
and a text report saved to data/processed/data_quality_report.txt.

Inputs:
    data/processed/nba_player_stats_cleaned.csv
    data/processed/nba_contracts_cleaned.csv
    data/processed/nba_merged.csv

Outputs:
    data/processed/data_quality_report.txt
"""

import os
from pathlib import Path

import pandas as pd

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

STATS_PATH = Path("data/processed/nba_player_stats_cleaned.csv")
CONTRACTS_PATH = Path("data/processed/nba_contracts_cleaned.csv")
MERGED_PATH = Path("data/processed/nba_merged.csv")
REPORT_PATH = Path("data/processed/data_quality_report.txt")


# Helpers
def section(title: str, char: str = "=") -> str:
    """Format a section header for the report."""
    return f"\n{char * 70}\n{title}\n{char * 70}\n"


def profile_dataframe(df: pd.DataFrame, name: str) -> str:
    """Generate a profile summary string for a single dataframe."""
    lines = []
    lines.append(section(f"Profile: {name}"))
    lines.append(f"Rows:    {len(df)}")
    lines.append(f"Columns: {len(df.columns)}")
    lines.append(f"\nColumn types:")
    for col, dtype in df.dtypes.items():
        lines.append(f"  {col:20s} {dtype}")

    lines.append(f"\nMissing values per column:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            pct = 100 * count / len(df)
            lines.append(f"  {col:20s} {count} ({pct:.1f}%)")
    if missing.sum() == 0:
        lines.append("  (none)")

    lines.append(f"\nDuplicate rows: {df.duplicated().sum()}")
    if "player_name" in df.columns:
        lines.append(f"Duplicate player_names: {df['player_name'].duplicated().sum()}")

    return "\n".join(lines)


def profile_numeric(df: pd.DataFrame, columns: list, name: str) -> str:
    """Summary statistics for numeric columns."""
    lines = []
    lines.append(section(f"Numeric distributions: {name}", char="-"))
    desc = df[columns].describe().round(2)
    lines.append(desc.to_string())
    return "\n".join(lines)


def flag_outliers(df: pd.DataFrame, name: str) -> str:
    """Flag suspicious values that warrant attention."""
    lines = []
    lines.append(section(f"Suspicious values: {name}", char="-"))

    flags = []

    # Negative values that shouldn't be negative
    for col in ["points", "rebounds", "assists", "steals", "blocks", "gp", "minutes"]:
        if col in df.columns:
            count = (df[col] < 0).sum()
            if count > 0:
                flags.append(f"  {col}: {count} negative values")

    # between league minimum and supermax
    if "salary" in df.columns:
        below_min = (df["salary"] < 50_000).sum()
        above_max = (df["salary"] > 80_000_000).sum()
        if below_min > 0:
            flags.append(f"  salary below $500k: {below_min} players")
        if above_max > 0:
            flags.append(f"  salary above $80M: {above_max} players")

    for col in ["fg_pct", "fg3_pct", "ft_pct"]:
        if col in df.columns:
            out_of_range = ((df[col] < 0) | (df[col] > 1)).sum()
            if out_of_range > 0:
                flags.append(f"  {col} out of [0,1] range: {out_of_range}")

    # Zero values that might be real but worth noting
    if "minutes" in df.columns:
        zero_min = (df["minutes"] == 0).sum()
        if zero_min > 0:
            flags.append(f"  players with 0 minutes: {zero_min}")

    if flags:
        lines.extend(flags)
    else:
        lines.append("  (no suspicious values detected)")

    return "\n".join(lines)


def integration_summary(stats: pd.DataFrame, contracts: pd.DataFrame, merged: pd.DataFrame) -> str:
    """Summary of the integration coverage."""
    lines = []
    lines.append(section("Integration coverage"))
    lines.append(f"Stats players (after filtering):     {len(stats)}")
    lines.append(f"Contracts players (after dedup):     {len(contracts)}")
    lines.append(f"Successfully merged:                 {len(merged)}")
    pct = 100 * len(merged) / len(stats) if len(stats) > 0 else 0
    lines.append(f"Match rate (vs. stats):              {pct:.1f}%")
    lines.append(f"\nStats players unmatched:             {len(stats) - len(merged)}")
    lines.append(f"Contracts players unmatched:         {len(contracts) - len(merged)}")
    lines.append(
        "\nUnmatched players were investigated manually and identified as\n"
        "predominantly free agents, two-way contract players, and mid-season\n"
        "waivers/buyouts whose contracts are not listed on Basketball Reference."
    )
    return "\n".join(lines)


def top_bottom_etd(merged: pd.DataFrame) -> str:
    """Show the top and bottom players by EtD ratio for a sanity check."""
    lines = []
    lines.append(section("EtD ratio sanity check", char="-"))
    if "etd_ratio" not in merged.columns:
        lines.append("  (etd_ratio column not present)")
        return "\n".join(lines)

    cols = ["player_name", "salary", "production_score", "etd_ratio"]
    available = [c for c in cols if c in merged.columns]

    lines.append("Top 10 by EtD (best value):")
    top = merged.nlargest(10, "etd_ratio")[available].round(2)
    lines.append(top.to_string(index=False))

    lines.append("\nBottom 10 by EtD (worst value):")
    bot = merged.nsmallest(10, "etd_ratio")[available].round(2)
    lines.append(bot.to_string(index=False))

    return "\n".join(lines)


# Main
def main():
    print("Loading datasets...")
    stats = pd.read_csv(STATS_PATH)
    contracts = pd.read_csv(CONTRACTS_PATH)
    merged = pd.read_csv(MERGED_PATH)

    report_parts = []
    report_parts.append("NBA ROI PROJECT - DATA QUALITY REPORT")
    report_parts.append(f"Generated from: {STATS_PATH}, {CONTRACTS_PATH}, {MERGED_PATH}")

    # Per-dataset profiles
    report_parts.append(profile_dataframe(stats, "stats (cleaned)"))
    report_parts.append(profile_dataframe(contracts, "contracts (cleaned)"))
    report_parts.append(profile_dataframe(merged, "merged"))

    stat_numerics = [
        "age", "gp", "minutes", "points", "rebounds", "assists",
        "steals", "blocks", "fg_pct", "fg3_pct", "ft_pct", "plus_minus",
    ]
    stat_numerics = [c for c in stat_numerics if c in stats.columns]
    report_parts.append(profile_numeric(stats, stat_numerics, "stats"))

    contract_numerics = [c for c in ["salary", "guaranteed"] if c in contracts.columns]
    report_parts.append(profile_numeric(contracts, contract_numerics, "contracts"))

    report_parts.append(flag_outliers(stats, "stats"))
    report_parts.append(flag_outliers(contracts, "contracts"))
    report_parts.append(flag_outliers(merged, "merged"))

    # Integration summary
    report_parts.append(integration_summary(stats, contracts, merged))

    # EtD sanity
    report_parts.append(top_bottom_etd(merged))

    full_report = "\n".join(report_parts)

    # Write to file
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(full_report, encoding="utf-8")

    print(full_report)
    print(f"\n\nReport saved to {REPORT_PATH}")


if __name__ == "__main__":
    main()