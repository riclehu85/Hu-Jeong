# Final Project Report: ROI of Current NBA Players ('23-'25)

## Contributors: Alexander Jeong (ajeong4) & Rick Hu (rickhu2)

### Summary
Our goal for this project was to do an analysis on the statistics of NBA players to try and find if there was a way to quantify Return on Investment (ROI) for NBA players. In the modern era of the NBA, the implementation of a rigorous salary cap, further complicated by the recent introduction of the "second apron" luxury tax tiers, has transformed roster construction from just having high value players to having to balance value and efficiency for financial optimization. 

This project seeks to quantify this phenomenon by calculating the ROI for NBA players, determining which specific player archetypes and skill sets provide the most efficient path to creating overall value for teams. A team’s success depends not just on pure raw talent or skill, but also on identifying valuable players (i.e. players whose statistical contributions exceed their contract cost). Our analysis specifically focuses on the 2023-2024 and 2024-2025 seasons, providing a snapshot of the league’s current players and conditions. The motivation behind this research stems from the disparity between perceived market value and actual statistical impact, with discourse surrounding NBA stars such as Anthony Davis and Zion Williamson.  

Research Questions:

- Which player archetypes provide the highest ROI in terms of Wins Produced per million dollars?

- Which specific skills are currently the most valuable for a player to possess?

We are synthesizing traditional box score data with comprehensive financial spreadsheets and advanced "all-in" metrics. By utilizing Player Efficiency Rating (PER) and Win Shares, we can move past basic counting stats (like points per game) to capture a player’s holistic impact on winning. Focusing on player archetypes, we have divided the NBA players into four distinct categories to analyze.

- Veteran Stars: High-salary players on max or super-max contracts.

- Mid-level Role Players: Utility players typically signed via the Mid-Level Exception

- Rookie Scale Players: Young talent on fixed-cost, entry-level contracts.

- 3-and-D Specialists: Wing players prioritized for floor spacing and perimeter defense.

To standardize our findings, we have developed a new variable/metric called the Efficiency-to-Dollar ratio. This ratio will be applied across four distinct player archetypes. We then employed a regression model to isolate specific skill sets—such as rim protection, three-point shooting, and secondary playmaking—against their impact on the EtD ratio. This allows us to identify "market inefficiencies," revealing which attributes are currently overvalued or undervalued in the free-agent market. 
