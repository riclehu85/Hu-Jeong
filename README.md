# Final Project Report: ROI of Current NBA Players ('25-'26)

#### Contributors: Alexander Jeong (ajeong4) & Rick Hu (rickhu2)

## Summary
Our goal for this project was to do an analysis on the statistics of NBA players to try and find if there was a way to quantify Return on Investment (ROI) for NBA players. In the modern era of the NBA, the implementation of a rigorous salary cap, further complicated by the recent introduction of the "second apron" luxury tax tiers, has transformed roster construction from just having high value players to having to balance value and efficiency for financial optimization. 

This project seeks to quantify this phenomenon by calculating the ROI for NBA players, determining which specific player archetypes and skill sets provide the most efficient path to creating overall value for teams. A team’s success depends not just on pure raw talent or skill, but also on identifying valuable players (i.e. players whose statistical contributions exceed their contract cost). Our analysis specifically focuses on the 2023-2024 and 2024-2025 seasons, providing a snapshot of the league’s current players and conditions. The motivation behind this research stems from the disparity between perceived market value and actual statistical impact, with discourse surrounding NBA stars such as Anthony Davis and Zion Williamson.  

Research Questions: 
1. Which player archetypes provide the highest ROI in terms of production per dollar of salary? 
2. Which advanced metrics correlate most strongly with salary, and where are the largest deviations between expected and actual pay?
3. Do certain archetypes consistently provide better ROI than others in the current era? 

We synthesize traditional box score data from the official NBA API with contract data from Basketball Reference, then enrich with NBA-API advanced metrics including Player Impact Estimate (PIE), Usage Rate, True Shooting Percentage, and Defensive Rating. We define an "Efficiency-to-Dollar" (EtD) ratio computed as PIE × 100 divided by salary in millions, providing a single number that measures production per dollar. 

We assigned each player to one of eight archetypes based on age, minutes, salary, and statistical profile: Rookie Contributor, Veteran Star, Prime Star, 3-and-D Wing, High-Volume Scorer, Sixth Man, Defensive Specialist, and Role Player. We then computed archetype-level summary statistics to compare ROI across player types. 

Our analysis of 387 players reveals a substantial premium that NBA teams pay for star-tier production. **Rookie Contributors and Role Players produce roughly 10 times the PIE per dollar of Veteran Stars and Prime Stars** (avg EtD ~3.4-3.7 vs. ~0.35). Despite a 6-year average age difference, Prime Stars and Veteran Stars show statistically indistinguishable EtD ratios (0.381 vs. 0.346), suggesting the league's salary structure does not meaningfully discount aging stars relative to their younger counterparts within the high-salary tier. Sixth Men emerged as a notable value archetype (avg EtD 1.35), producing roughly 3.5x the PIE per dollar of Prime Stars while contributing meaningful scoring off the bench.

## Data Profile

### Dataset 1: NBA player statistics (traditional and advanced)
**Source:** API Client for official NBA

**Format:** JSON response objects converted to CSV. Two views are pulled: "Base" (traditional box score) and "Advanced" (efficiency and on/off metrics). 

**Repository location:** - `data/raw/nba_player_stats.csv` — base/traditional stats (569 rows, 75 columns) - `data/raw/nba_player_advanced.csv` — advanced metrics (569 rows, 76 columns) 

**Structure and content:** Each row corresponds to one player's full-season aggregated 2024-25 regular-season statistics. The base file contains traditional box score totals (PTS, REB, AST, STL, BLK, etc.), shooting percentages, and counting metrics. The advanced file contains efficiency and impact metrics including PIE (Player Impact Estimate), Offensive/Defensive/Net Rating, Usage Percentage, True Shooting Percentage, and Pace. 

**Characteristics:** This data is comprehensive and authoritative. It is the NBA’s records. Coverage includes every player who appeared in at least one game during the regular season. Data is updated nightly throughout the season and reflects final season values for completed seasons. 

**Relationship to research questions:** This dataset is the production half of the EtD ratio. The advanced metrics, particularly PIE, allow us to capture overall player impact in a single number that goes beyond simple counting stats. The advanced metrics also enable archetype assignment. For example, identifying 3-and-D Wings requires three-point attempt volume, three-point percentage, defensive rating, and usage rate, all of which come from this dataset. 

**Ethical and legal constraints:** Data on stats.nba.com is owned by the NBA. The `nba_api` client does not require authentication but accesses the underlying API which is technically a non-public endpoint. Use is permitted for non-commercial academic research. There are no privacy concerns as all player statistics are public performance data, not personal information. We accessed data with reasonable rate limits (one-second pauses between calls) to avoid impacting service availability. 

### Dataset 2: NBA Contract Data
**Source:** 2025-26 NBA Player Contracts | Basketball-Reference.com 

**Format:** HTML table parsed and saved as CSV

**Repository location:** - `data/raw/nba_contracts_raw.csv` (525 rows in raw form, 487 after cleaning and deduplication) 

**Structure and content:** Each row originally corresponds to one contract-year per player. The dataset contains player names, current team abbreviations, salary by year (2025-26 through 2030-31), and total guaranteed money. Our analysis uses the 2025-26 salary figure as our cost variable.

**Characteristics:** The data represents a financial snapshot of NBA contracts as listed on Basketball Reference at the time of acquisition. It is frequently updated to reflect trades, waivers, and contract restructuring. The data inherently lists multiple rows per player corresponding to future contract years; this required deduplication 
during cleaning (see Data Cleaning section). 

**Ethical and legal constraints:** Data is owned by Sports Reference LLC. Player salaries are a matter of public record. Use is permissible for non-commercial academic research under the source's terms of use. 

**Relationship to research questions:** This dataset is the cost half of the EtD ratio. Without precise salary figures, it would be impossible to quantify the cost of a unit of production. The salary data also enables archetype assignment. 

### Integration Challenge
The two datasets have no shared unique identifier. `nba_api` uses NBA's internal `PLAYER_ID` while Basketball Reference uses player names. This required a normalized-name matching approach combining exact and fuzzy matching, described in detail in the Data Cleaning and Challenges sections. Of the 520 players in our cleaned stats dataset, 411 (79%) were successfully matched to a contract row, with the remainder predominantly free agents, two-way contract players, and mid-season waivers/buyouts who do not appear in Basketball Reference's contract listings.


## Data Quality
After cleaning and deduplication, the contracts dataset contains 487 players with 5 columns. 19 of 487 rows (3.9%) are missing the ” guaranteed” amount, representing players on partial-guarantee deals where Basketball Reference does not list a specific guaranteed figure. Salaries range from $70,732 (10-day contract) to $59.6 Million (supermax contract), with a median of $5.7 Million. The presence of contracts below $500,000 is not a data quality issue. This reflects legitimate 10-day signings and waiver claims that pay prorated portions of the league minimum.

### Integration coverage
411 of 520 stats-side players (79%) successfully matched to a contract record. The 109 unmatched stats players were investigated manually. The overwhelming majority are players who do not appear on Basketball Reference's contracts page at all, including:
Free agents: waived or bought out during the season (e.g. Ben Simmons (waived by Clippers in Feb 2025))
Two-way contract players: signed to G-League/NBA dual contracts not listed in the standard contracts table
10-day contract players: signed late in the season
Mid-season replacements: who joined teams after Basketball Reference’s snapshot
This is a structural limitation of the source rather than a defect in our pipeline. Documented in the Findings section.

### Small-sample players
Players near the 8-game minimum threshold can produce extreme PIE values that don’t represent sustainable production. To address this, we added a 250-minute total minutes filter on top of the games filter. This reduced our final analyzed dataset to 387 players. Without this filter, players like Leonard Miller (PIE of 0.202 in limited minutes) would have ranked among the league’s most impactful by an advanced metric while having played too few games for that metric to be meaningful.

### Player name inconsistencies

Manually investigation revealed that there were a couple of naming differences across datasets:
Punctuation differences (e.g. “P.J. Tucker” vs “PJ Tucker”)
Diacritic difference (e.g. “Luka Dončić” vs “Luka Doncic”)
Suffix Differences (e.g. “Tim Hardaway Jr.” vs  “Tim Hardaway”)
Our normalization function (‘scripts/data_integration.py’) handles all three Unicode decomposition, ASCII coercion, and regex-based suffix removal.

### Defensive metric limitations

The team-context DEF_RATING used to identify Defensive Specialists combines individual defensive ability with team defensive infrastructure. Player on an elite defensive team appears to have a strong DEF_RATING regardless of their personal contribution. Better identification would require player-traching data we do not have access to. 

### Duplicate contract rows

Iniital inspection of the merged dataset revealed 36 duplicate rows due to Basketball Reference’s contract table structure, which lists one row per future contract year. We resolved this by deduplicating on player_name. Retaining the row with the highest guaranteed amount. Documented in Data Cleaning section. 




## Data Cleaning
### Loads base stats and advanced stats from the API and merges them on PLAYER_ID into a single stats dataframe
- This process eliminates data fragmentation by utilizing the unique PLAYER_ID as a primary key rather than player names, which has had some inconsistencies 
- Ensures that the player’s base and advances stats are unified under a single and comprehensive profile


### Selects useful columns from both databases and filters out variables not used in this research
- By isolating high-value variables and discarding data irrelevant to our specific research questions, we reduce high-dimensionality noises


### Standardizes column names (snake_case)
- Snake case is a formatting style where spaces in phrases are replaced with underscores (_) and all letters are lowercase
- Standardizing all of our columns by implementing snake_case ensures consistency throughout the database and allows our analysis scripts to reference variables without errors

### Computes per-game versions of counting stats
- Corrects volume bias, allowing us to compare the efficiency of a player who played 70 games directly against one who played 50 through per-game statistics
- Values their per-minute impact rather than just their total seasonal accumulation


### Strips whitespace from player names
- Stripping the whitespace is a critical step to prevent failed record linkage
- This sanitization ensures that when we integrate the stats dataframe with the salary data to create nba_merged.csv, the player names match perfectly

### Converts salary strings ('$1,234,567') to numeric values
- Strips currency symbols from the salary and guaranteed columns to then convert from data type(str) to data type(int)
- Makes it easier to make calculations regarding our EtD ratio and regression analysis

### Drops rows missing critical fields
- Filtering out null values and incomplete entries ensures analytical completeness to prevent any errors
- Ensures that every player has a verified value for both their salary and their statistical output

### Filters out players with fewer than 8 games (MIN_GAMES_PLAYED)
- Mitigates the impact of statistical outliers by removing players with extremely small sample sizes (games played)
- Statistical outliers can skew the results of our analysis and removing these players improves our findings and accuracy

### Deduplicates contracts (Basketball Reference lists one row per future contract year per player)
- Basketball-Reference provides a longitudinal view by listing one row for every future year of a player's contract
- We remove these redundant rows to isolate only the salary for the current 2025–2026 season


## Findings

Our analysis of 387 NBA players across the 2024-25 regular season reveals a substantial premium that the league pays for star-tier production, alongside several pockets of meaningful market inefficiency. We summarize findings using the Efficiency-to-Dollar (EtD) metric, computed as PIE × 100 divided by salary in millions. 

### The “star tax” is large and consistent

One of the clearest findings is the cost gap between top and bottom archetypes. Average EtD by archetype, sorted from best to worst value:

| Archetype | n | Avg EtD | Median Salary | 
|---|---|---|---| 
| Role Player | 164 | 3.74 | $3.65M | 
| Rookie Contributor | 73 | 3.40 | $4.68M | 
| 3-and-D Wing | 21 | 1.98 | $10.04M | 
| High-Volume Scorer | 3 | 1.48 | $6.84M | 
| Defensive Specialist | 24 | 1.39 | $9.61M | 
| Sixth Man | 16 | 1.35 | $11.53M | 
| Prime Star | 40 | 0.38 | $36.91M | 
| Veteran Star | 46 | 0.35 | $34.97M | 

Role Players and Rookie Contributors produce roughly **10 times the PIE per dollar** of Prime Stars and Veteran Stars. While stars deliver substantially more raw production (avg PIE ~0.12 vs ~0.09), the salary gap is far larger than the production gap, creating a large efficiency penalty for star-tier contracts. This pattern is visible in: <img width="1968" height="1168" alt="image" src="https://github.com/user-attachments/assets/06df6185-3120-423f-88a0-9cf09d5828ac" />

### Aging stars are not discounted
Despite a 6-year average age difference (25 vs. 31), Prime Stars and Veteran Stars have nearly identical EtD ratios (0.381 vs. 0.346). This suggests the NBA's salary structure does not meaningfully discount aging stars relative to their younger counterparts within the high-salary tier. Once a player crosses the ~$20M threshold, market pricing appears largely insensitive to age. The salary distribution by archetype graph shows the two groups occupying overlapping salary ranges despite their different career stages. 
<img width="2168" height="1167" alt="image" src="https://github.com/user-attachments/assets/ace14cce-59b4-4805-894f-e953f3dc8b5c" />

### Sixth men are the surprising value bucket
Sixth Men (defined as high-usage bench scorers averaging 12+ PPG in fewer than 28 minutes per game) average EtD of 1.35 — roughly 3.5x better than Prime Stars. This bucket includes players like Russell Westbrook (on a veteran minimum at $2.3M), Moritz Wagner ($5.0M, PIE 0.165), and Ty Jerome ($8.8M, PIE 0.134). These players deliver star-adjacent production at a fraction of the cost. Teams pursuing roster efficiency should look hard at this archetype. 

### Salary correlates with PIE but with high variance
Plotting salary against PIE (`outputs/figures/salary_vs_pie_scatter.png`) reveals a positive but loose relationship. The league's top producers (Nikola Jokić, Shai Gilgeous-Alexander, Giannis Antetokounmpo) cluster in the high-salary, high-PIE region as expected. However, several high-salary players produce well below their pay grade (Joel Embiid, Brandon Ingram, Paul George — all on injury-shortened seasons) while several minimum-contract players produce far above theirs. 
<img width="2138" height="1368" alt="image" src="https://github.com/user-attachments/assets/e483cd87-6bb9-4056-88cd-a9b85796ce73" />

### Top 20 cap-efficiency leaderboard
The top 20 players by EtD-PIE are dominated by Role Players and Rookie Contributors on minimum or near-minimum contracts. The leaderboard's ceiling — Jaden Springer at EtD 89, on a $70k 10-day contract — illustrates how raw EtD is dominated by contract-floor players. Within the high-salary tier (>$15M), Shai Gilgeous-Alexander stands out as the league's most efficient star at $38.3M with PIE 0.199 (EtD 0.519), substantially outperforming the Prime Star average of 0.381.
<img width="2169" height="1768" alt="image" src="https://github.com/user-attachments/assets/20abf59f-93d5-445f-96b6-cc073e383913" />

## Future Works

## Challenges

## Reproducing

### Prerequisites

- Python 3.11 or newer
- Git

### Steps

**Step 1. Clone the repository**

```bash
   git clone https://github.com/<your-username>/Hu-Jeong.git
   cd Hu-Jeong
```

**Step 2. Create and activate a virtual environment**

   On Windows (PowerShell):
```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
```

   On macOS/Linux:
```bash
   python -m venv .venv
   source .venv/bin/activate
```

**Step 3. Install dependencies**

```bash
   pip install -r requirements.txt
```

**Step 4. Verify input data is present**

   The raw input files are committed to the repository under `data/raw/`:
   - `nba_player_stats.csv` (NBA API base stats)
   - `nba_player_advanced.csv` (NBA API advanced stats)
   - `nba_contracts_raw.csv` (Basketball Reference contracts)

   No download step is required.

**Step 5. Run the full pipeline**

```bash
   python run_all.py
```

   This executes all six stages of the analysis:
   1. Acquire NBA API data (skipped if raw files already exist)
   2. Clean both datasets
   3. Integrate them via normalized-name matching
   4. Assign archetypes and compute the EtD ratio
   5. Profile the data quality
   6. Generate the four visualizations

   To force a fresh API pull (overwriting the committed raw stats files):
```bash
   python run_all.py --refresh
```

### Outputs

After running, the following files will be produced or refreshed:

- `data/processed/nba_player_stats_cleaned.csv` — cleaned NBA stats
- `data/processed/nba_contracts_cleaned.csv` — cleaned and deduplicated contracts
- `data/processed/nba_merged.csv` — integrated dataset (411 players)
- `data/processed/nba_merged_with_archetypes.csv` — final analytical dataset (387 players after minimum-minutes filter, with archetype labels and EtD ratios)
- `data/processed/archetype_summary.csv` — per-archetype summary statistics
- `data/processed/data_quality_report.txt` — data profile and integration coverage report
- `data/processed/unmatched_players.csv` — audit trail of players that failed to match across datasets
- `outputs/figures/salary_vs_pie_scatter.png` — Salary vs. PIE colored by archetype
- `outputs/figures/avg_etd_by_archetype.png` — Bar chart of average EtD by archetype
- `outputs/figures/top_etd_leaderboard.png` — Top 20 NBA cap-efficiency leaderboard
- `outputs/figures/salary_by_archetype_box.png` — Salary distribution by archetype

### Running individual stages

If you want to run a single stage in order, all scripts are in `scripts/` and can be run directly in this order:

```bash
python scripts/nba_API_RAW.py
python scripts/data_cleaning.py
python scripts/data_integration.py
python scripts/assign_archetypes.py
python scripts/profile_data.py
python scripts/make_visualizations.py
```

Each script handles its own paths and can be re-run independently.

### Troubleshooting

- **`ModuleNotFoundError`**: Verify your virtual environment is activated. The prompt should display `(.venv)` at the start.
- **NBA API connection error**: The NBA API can rate-limit if called too frequently. Wait a few minutes and retry, or run without `--refresh` to use the committed raw files.
- **Unicode errors in terminal output**: Player names contain accented characters. Scripts use UTF-8 encoding for stdout, but if you see character encoding errors, your terminal may need to be set to UTF-8 (e.g., `chcp 65001` on Windows).


## References
### Datasets

National Basketball Association. (2025). *NBA player statistics, 2024-25 regular season* [Data set]. Retrieved via the `nba_api` Python client from https://stats.nba.com. Accessed November 2025.

Sports Reference LLC. (2025). *NBA player contracts* [Data set]. Basketball Reference. https://www.basketball-reference.com/contracts/players.html. Accessed November 2025.

### Software

Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90–95. https://doi.org/10.1109/MCSE.2007.55

McKinney, W. (2010). Data structures for statistical computing in Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 56–61). https://doi.org/10.25080/Majora-92bf1922-00a

Bachmann, M. (2024). *RapidFuzz: Rapid fuzzy string matching* (Version 3.x) [Computer software]. https://github.com/maxbachmann/RapidFuzz

Patel, S. (2024). *nba_api: An API client package to access the APIs for NBA.com* (Version 1.x) [Computer software]. https://github.com/swar/nba_api

Waskom, M. L. (2021). seaborn: Statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. https://doi.org/10.21105/joss.03021

Python Software Foundation. (2024). *Python language reference, version 3.11*. https://www.python.org

### Background and context

Lowe, Z. (2023). NBA's new CBA, the second apron, and the future of roster construction. *ESPN*. https://www.espn.com (Used as background context on the salary cap structure motivating the research question.)

NBA. (2025). *Player Impact Estimate (PIE) - Stat Glossary*. https://www.nba.com/stats/help/glossary

Oliver, D. (2004). *Basketball on paper: Rules and tools for performance analysis*. Brassey's, Inc. (Foundational work on advanced basketball metrics.)

