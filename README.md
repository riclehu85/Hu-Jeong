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

### Data Quality

### Data Cleaning

### Findings

### Future Works

### Challenges

### Reproducing

### References
