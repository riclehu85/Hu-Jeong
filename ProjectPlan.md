Overview:


Team Member Roles:
Alexander Jeong, ajeong4 - Role: Data Analyst
Responsibilities: Exploratory data analysis and modeling. Develop logic for EtD ratio, run regression models to determine feature importance.

Rick Hu:, rickhu2 - Role: Data Analyst: 
Responsibilities: Query the nba_api, scrape financial tables from Spotrac and the GitHub repo. Data cleaning and data integrity.


Question:


Datasets Used:


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
