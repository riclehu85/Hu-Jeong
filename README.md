# Final Project Report: ROI of Current NBA Players ('23-'25)

## Contributors: Alexander Jeong (ajeong4) & Rick Hu (rickhu2)

### Summary
Our goal for this project was to do an analysis on the statistics of NBA players to try and find if there was a way to quantify Return on Investment (ROI) for NBA players. In the modern era of the NBA, the implementation of a rigorous salary cap, further complicated by the recent introduction of the "second apron" luxury tax tiers, has transformed roster construction from just having high value players to having to balance value and efficiency for financial optimization. 

This project seeks to quantify this phenomenon by calculating the ROI for NBA players, determining which specific player archetypes and skill sets provide the most efficient path to creating overall value for teams. A team’s success depends not just on pure raw talent or skill, but also on identifying valuable players (i.e. players whose statistical contributions exceed their contract cost). Our analysis specifically focuses on the 2023-2024 and 2024-2025 seasons, providing a snapshot of the league’s current players and conditions. The motivation behind this research stems from the disparity between perceived market value and actual statistical impact, with discourse surrounding NBA stars such as Anthony Davis and Zion Williamson.  

Research Questions: 
1. Which player archetypes provide the highest ROI in terms of production per dollar of salary? 
2. Which advanced metrics correlate most strongly with salary, and where are the largest deviations between expected and actual pay?
3. Do certain archetypes consistently provide better ROI than others in the current era? 

We synthesize traditional box score data from the official NBA API with contract data from Basketball Reference, then enrich with NBA-API advanced metrics including Player Impact Estimate (PIE), Usage Rate, True Shooting Percentage, and Defensive Rating. We define an "Efficiency-to-Dollar" (EtD) ratio computed as PIE × 100 divided by salary in millions, providing a single number that measures production per dollar. 

We assigned each player to one of eight archetypes based on age, minutes, salary, and statistical profile: Rookie Contributor, Veteran Star, Prime Star, 3-and-D Wing, High-Volume Scorer, Sixth Man, Defensive Specialist, and Role Player. We then computed archetype-level summary statistics to compare ROI across player types. 

Our analysis of 387 players reveals a substantial premium that NBA teams pay for star-tier production. **Rookie Contributors and Role Players produce roughly 10 times the PIE per dollar of Veteran Stars and Prime Stars** (avg EtD ~3.4-3.7 vs. ~0.35). Despite a 6-year average age difference, Prime Stars and Veteran Stars show statistically indistinguishable EtD ratios (0.381 vs. 0.346), suggesting the league's salary structure does not meaningfully discount aging stars relative to their younger counterparts within the high-salary tier. Sixth Men emerged as a notable value archetype (avg EtD 1.35), producing roughly 3.5x the PIE per dollar of Prime Stars while contributing meaningful scoring off the bench.

### Data Profile

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


### Data Quality

### Data Cleaning

### Findings

Our analysis of 387 NBA players across the 2024-25 regular season reveals a substantial premium that the league pays for star-tier production, alongside several pockets of meaningful market inefficiency. We summarize findings using the Efficiency-to-Dollar (EtD) metric, computed as PIE × 100 divided by salary in millions. 

### The “star tax” is large and consistent

One of the clearest findings is the cost gap between top and bottom archetypes. Average EtD by archetype, sorted from best to worst value:

| Archetype | n | Avg EtD | Median Salary | |---|---|---|---| | Role Player | 164 | 3.74 | $3.65M | | Rookie Contributor | 73 | 3.40 | $4.68M | | 3-and-D Wing | 21 | 1.98 | $10.04M | | High-Volume Scorer | 3 | 1.48 | $6.84M | | Defensive Specialist | 24 | 1.39 | $9.61M | | Sixth Man | 16 | 1.35 | $11.53M | | Prime Star | 40 | 0.38 | $36.91M | | Veteran Star | 46 | 0.35 | $34.97M | 

Role Players and Rookie Contributors produce roughly **10 times the PIE per dollar** of Prime Stars and Veteran Stars. While stars deliver substantially more raw production (avg PIE ~0.12 vs ~0.09), the salary gap is far larger than the production gap, creating a large efficiency penalty for star-tier contracts. This pattern is visible in: <img width="1968" height="1168" alt="image" src="https://github.com/user-attachments/assets/06df6185-3120-423f-88a0-9cf09d5828ac" />

### Aging stars are not discounted
Despite a 6-year average age difference (25 vs. 31), Prime Stars and Veteran Stars have nearly identical EtD ratios (0.381 vs. 0.346). This suggests the NBA's salary structure does not meaningfully discount aging stars relative to their younger counterparts within the high-salary tier. Once a player crosses the ~$20M threshold, market pricing appears largely insensitive to age. The salary distribution by archetype graph shows the two groups occupying overlapping salary ranges despite their different career stages. 
<img width="2168" height="1167" alt="image" src="https://github.com/user-attachments/assets/ace14cce-59b4-4805-894f-e953f3dc8b5c" />

### Future Works

### Challenges

### Reproducing

### References
