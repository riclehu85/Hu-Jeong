"""
run_all.py

End-to-end pipeline runner. Executes every stage of the analysis in order:
    1. Acquire raw data from NBA API
    2. Clean both datasets
    3. Integrate them
    4. Assign archetypes
    5. Profile data quality
    6. Generate visualizations

Usage:
    python run_all.py             # skip API pull if raw files exist
    python run_all.py --refresh   # force re-pull from NBA API

Notes:
    - The contracts file (data/raw/nba_contracts_raw.csv) is acquired manually
      from Basketball Reference; this script assumes it already exists at that
      path. See README for instructions.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent

STAGES = [
    ("Acquire NBA API data",     "scripts/nba_API_RAW.py"),
    ("Clean datasets",            "scripts/data_cleaning.py"),
    ("Integrate datasets",        "scripts/data_integration.py"),
    ("Assign archetypes",         "scripts/assign_archetypes.py"),
    ("Profile data quality",      "scripts/profile_data.py"),
    ("Generate visualizations",   "scripts/make_visualizations.py"),
]


def run_stage(description: str, script: str) -> None:
    print(f"\n{'=' * 70}")
    print(f"STAGE: {description}")
    print(f"  -> python {script}")
    print(f"{'=' * 70}")
    result = subprocess.run([sys.executable, script], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print(f"\n!!! Stage failed: {description} !!!")
        sys.exit(result.returncode)


def main() -> None:
    refresh = "--refresh" in sys.argv
    raw_stats = PROJECT_ROOT / "data/raw/nba_player_stats.csv"

    for description, script in STAGES:
        if "nba_API_RAW" in script and raw_stats.exists() and not refresh:
            print(f"\nSkipping API pull (raw stats already exist; use --refresh to force).")
            continue
        run_stage(description, script)

    print("\n" + "=" * 70)
    print("ALL STAGES COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()