# Data Dictionary

This document describes every column in the analytical datasets produced by this project. The primary analytical dataset is `data/processed/nba_merged_with_archetypes.csv`, which integrates NBA player statistics with contract data and adds derived metrics and archetype labels.

## File: `nba_merged_with_archetypes.csv`

The main analytical dataset. One row per player, 387 rows total (after filtering for minimum games and minimum total minutes), 41 columns.

### Identifier columns

| Column | Type | Description | Source |
|---|---|---|---|
| `player_id` | int | NBA's internal unique identifier for each player | NBA API |
| `player_name` | string | Player's full name | NBA API |
| `season` | string | NBA season label (e.g., "2025-26") | Derived |

### Team columns

| Column | Type | Description | Source |
|---|---|---|---|
| `team_stats` | string | Team abbreviation as listed in NBA stats data (e.g., "LAL", "BOS") | NBA API |
| `team_contract` | string | Team abbreviation as listed in Basketball Reference contracts | Basketball Reference |

### Demographics

| Column | Type | Units | Description | Source |
|---|---|---|---|---|
| `age` | float | years | Player's age as of the season start | NBA API |

### Traditional box score totals (season aggregates)

| Column | Type | Units | Description | Source |
|---|---|---|---|---|
| `gp` | int | games | Games played | NBA API |
| `minutes` | float | minutes | Total minutes played across the season | NBA API |
| `points` | int | points | Total points scored | NBA API |
| `rebounds` | int | rebounds | Total rebounds (offensive + defensive) | NBA API |
| `assists` | int | assists | Total assists | NBA API |
| `steals` | int | steals | Total steals | NBA API |
| `blocks` | int | blocks | Total blocks | NBA API |
| `fg3a` | int | attempts | Total three-point attempts | NBA API |
| `plus_minus` | int | points | Cumulative plus/minus across all games played | NBA API |

### Shooting percentages

| Column | Type | Units | Description | Source |
|---|---|---|---|---|
| `fg_pct` | float | proportion (0-1) | Field goal percentage | NBA API |
| `fg3_pct` | float | proportion (0-1) | Three-point percentage | NBA API |
| `ft_pct` | float | proportion (0-1) | Free throw percentage | NBA API |

### Per-game versions of counting stats

Computed by dividing season totals by games played. Used for archetype classification and fair player comparison.

| Column | Type | Units | Description |
|---|---|---|---|
| `points_pg` | float | points per game | Average points per game |
| `rebounds_pg` | float | rebounds per game | Average rebounds per game |
| `assists_pg` | float | assists per game | Average assists per game |
| `steals_pg` | float | steals per game | Average steals per game |
| `blocks_pg` | float | blocks per game | Average blocks per game |
| `fg3a_pg` | float | attempts per game | Average three-point attempts per game |
| `minutes_pg` | float | minutes per game | Average minutes per game |

### Advanced metrics

| Column | Type | Units | Description | Source |
|---|---|---|---|---|
| `off_rating` | float | points per 100 possessions | Team offensive rating while player is on the court | NBA API |
| `def_rating` | float | points per 100 possessions | Team defensive rating while player is on the court (lower is better) | NBA API |
| `net_rating` | float | points per 100 possessions | `off_rating` minus `def_rating` | NBA API |
| `usage_pct` | float | proportion (0-1) | Share of team possessions used by the player while on court | NBA API |
| `true_shooting_pct` | float | proportion (0-1) | Shooting efficiency adjusted for 2PT/3PT/FT | NBA API |
| `pie` | float | proportion (0-1) | Player Impact Estimate — NBA's all-in-one production metric | NBA API |
| `ast_pct` | float | proportion (0-1) | Percentage of teammate field goals assisted | NBA API |
| `reb_pct` | float | proportion (0-1) | Percentage of available rebounds collected | NBA API |
| `pie_x100` | float | scaled (0-100) | PIE multiplied by 100 for readability in the EtD ratio | Derived |

### Contract / financial data

| Column | Type | Units | Description | Source |
|---|---|---|---|---|
| `salary` | float | USD | Player's salary for the 2025-26 season | Basketball Reference |
| `guaranteed` | float | USD | Total guaranteed money on player's current contract | Basketball Reference |
| `salary_millions` | float | USD millions | `salary` divided by 1,000,000 | Derived |

### Derived analytical variables

| Column | Type | Units | Description |
|---|---|---|---|
| `production_score` | float | composite score | Legacy production composite: `points + 1.2*rebounds + 1.5*assists + 2.0*steals + 2.0*blocks`. Retained for reference; analysis uses PIE instead. |
| `etd_ratio` | float | composite per million | Legacy EtD ratio: `production_score / salary_millions` |
| `etd_pie` | float | PIE×100 per million | **Primary analytical metric:** `pie_x100 / salary_millions`. Higher = better value. |
| `archetype` | string (categorical) | — | Player archetype assignment (see Archetype Definitions below) |

## Archetype Definitions

Archetypes are assigned by `scripts/assign_archetypes.py` using rules applied in priority order (first match wins). Eight categories total.

| Archetype | Definition |
|---|---|
| **Rookie Contributor** | Age ≤ 22 (rookie scale eligibility window) |
| **Veteran Star** | Age ≥ 28, ≥ 28 minutes per game, salary ≥ $20M |
| **Prime Star** | Age 23-27, ≥ 28 minutes per game, salary ≥ $15M |
| **3-and-D Wing** | ≥ 3.5 three-point attempts per game, ≥ 35% from three, defensive rating below league median, usage rate < 20% |
| **High-Volume Scorer** | Usage rate ≥ 25%, ≥ 18 points per game (and didn't fit any star bucket above) |
| **Sixth Man** | Usage rate ≥ 20%, ≥ 12 points per game, < 28 minutes per game |
| **Defensive Specialist** | Defensive rating in league top 25%, usage rate < 18%, ≥ 15 minutes per game |
| **Role Player** | Catch-all for any player not matching the above rules |

## Other Output Files

### `nba_merged.csv`
Pre-archetype version of the merged dataset. 411 rows. Same schema as above minus the `archetype`, `pie_x100`, and `etd_pie` columns.

### `nba_player_stats_cleaned.csv`
Cleaned per-player NBA stats before integration with contracts. 520 rows × 32 columns.

### `nba_contracts_cleaned.csv`
Cleaned and deduplicated contract data. 487 rows × 5 columns: `player_name`, `team`, `salary`, `guaranteed`, `season`.

### `archetype_summary.csv`
Aggregate statistics per archetype. 8 rows (one per archetype) × 11 columns: `n_players`, `avg_age`, `avg_minutes_pg`, `avg_points_pg`, `avg_usage_pct`, `avg_pie`, `avg_def_rating`, `avg_salary`, `median_salary`, `avg_etd_pie`, `median_etd_pie`.

### `unmatched_players.csv`
Audit trail of stats and contracts rows that did not match during integration. 109 unmatched stats players + 76 unmatched contracts players. Used for documenting integration coverage in the Data Quality section.

## Notes on units

- All proportions (percentages, rates) are stored as decimals between 0 and 1, not percentages between 0 and 100. For example, a 35% three-point shooter has `fg3_pct = 0.35`.
- Salary values are in raw US dollars unless suffixed with `_millions`.
- Time-based stats (minutes, games) reflect regular season totals only; playoff data is not included.