Overview:
The goal of this project is to quantify the Return on Investment (ROI) of NBA players by comparing their production on the court to their annual salary. In the modern era, with the “salary cap”, a team’s success depends not just on raw talent, but also on identifying “value” players. Players whose statistical contributions exceed their contract cost. 

Our project will focus primarily on the 2023-2024 and 2024-2025 seasons. We will be looking into these three things. First, we will integrate traditional box scores with financial data and advanced performance metrics (like Player Efficiency Rating and Win Shares). Second, we will create a new ratio called the “Efficiency-to-Dollar” ratio (EtD) for various archetypes: Veteran Stars, Mid-level role players, Rookie, and 3-and-D. Finally, we will use a regression analysis to identify which skills (e.g., 3-point shooting vs. rim protection) are currently “over” or “undervalued” in the NBA. Ultimately, this project will produce a “Cap Efficiency” leaderboard, giving us a data-driven ranking of nba management success in the modern “value-ball” era. 



Team Member Roles:
Alexander Jeong, ajeong4 - Role: Data Analyst
Responsibilities: Exploratory data analysis and modeling. Develop logic for EtD ratio, run regression models to determine feature importance.

Rick Hu:, rickhu2 - Role: Data Analyst: 
Responsibilities: Query the nba_api, scrape financial tables from Spotrac and the GitHub repo. Data cleaning and data integrity.


Question:
Which player archetypes provide the highest return on investment (ROI) in terms of “Wins Produced” per million dollars? 

Which advanced metrics (PER, Win Shares) has the strongest correlation with a player’s salary, and where are the biggest outliers?

Do certain positions consistently provide better EtD returns in the current era?


Datasets Used:
Official NBA Contract Dataset: 
https://www.spotrac.com/nba/contracts
HTML Table parsing
Dataset of player salaries, contract lengths, and “Cap Hit” percentages for each team by year.
This is our independent variable for ROI. Allows us to calculate the “Cost” side of our EtD ratio. Linking this to performance data is the primary challenge of the project due to lack of shared unique ID between the two sources

API Client for official NBA.com:
https://github.com/swar/nba_api
Format: JSON response objects
Contains game-by-game and season traditional and advanced statistics
This is our primary source. Allows us to filter for players who have played enough games.


Timeline:
Database Acquisition - milestone 2 deadline
Find databases relating to metrics of our question, such as annual salary data, contract information, and basketball statistics of NBA players - Rick
Look over any licensing or terms of use the databases have, such as if they are public domain, open data, etc. - Alex

Database storage and organization - 3/9 to 3/1
Data Models: Using a tabular model for the final analysis, but maintaining the semi-structured JSON for the raw performance metrics to preserve all metadata provided by the API - Alex

Data cleaning and alignment - 3/1 to 3/8
Make sure to review both financial and performance datasets to identify and remove any null values or other missing data values - Rick
Clean datasets and convert datatypes to standardize, such as making salary a INTEGER value if necessary or getting rid of additional symbols like $ and % - Rick
Filtering out players that could skew the data and analysis, such as players who have played less than 8 games in the current season - Alex

Data integration - Milestone 3 deadline
Create primary keys for dataset: player_name and season - Alex
Create new column for EtD ratio using other column variables - Alex

Data Analysis - week of and after milestone 3 deadline
Organize players into different archetypes: Veteran Stars, Mid-level role players, Rookie, and 3-and-D - Rick
Run a regression analysis model that look at salary as dependent variable, to look if some positions bring more value than others or if certain skills are more valuable for a player than others - Alex and Rick

Data documentation - week of and after milestone 3 deadline
Build a data dictionary that defines columns, such as defining EtD and explaining the math and reasoning behind our choices - Alex
Documenting the source URLs for datasets, API version numbers, and dates when data was accessed to account for any changes - Rick

Finalize and review - Milestone 4 deadline
Complete the project report with findings of our analysis - Alex and Rick
Verify end-to-end automated script to ensure that the code can be re-run with different data from a new season - Alex and Rick


Constraints:
Data Completeness: The issue is primarily with injuries and “Load Management,” which can skew ROI. A highly-paid player who is injured provides 0 ROI, but this doesn’t necessarily mean the contract was a bad decision at the time of signing. Maybe we can use “Per-Game” salary metrics instead to avoid skewing the model.

Temporal Coverage: Salary data is public, but there are other bonuses (e.g., a bonus for making an All-Star team, All-NBA, etc.) that are usually not included in these public datasets

Technical Challenges: The nba_api could block IP addresses if too many requests are made in a short window.

Data quality and integration: some players could have naming inconsistencies which make integrating the data a challenge. For example, players like “P.J. Tucker” v “PJ Tucker”. This could be a potential cleaning challenge that could break our data integration.


Gaps:
Defensive Metrics: Defensive metrics (steals/blocks) have always been notoriously poor at capturing the true defensive impact of a player. Through advanced statistics, there are defensive ratings, however one will need to see where they get these values from. 

Inflation: Potentially will need to normalize the salaries relative to the total Salary Cap for each specific year. A $20M salary in 2024 is a smaller percentage of the cap than in 2020. 

Intangibles: Data cannot capture different intangible assets including “Locker Room Presence”, “Basketball IQ”, “Veteran Leadership”, etc. There are some players that are “overpaid” statistically but provide value in many different ways. For example, mentoring the younger players, which is an invaluable skill. 

Contract complexity: having data on the salary doesn’t account for other forms of income the player might make from the team, such as performance bonuses

