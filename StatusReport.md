# Project Status Report

## 1. Task Updates

### Data Acquisition

- **Status:** Completed
- **Description:** Successfully collected both performance and contract datasets required for the project. Player performance data was obtained using the 'nba_api', while contract and salary data were collected from Basketball Reference and stored as a CSV file.
  
- **Progress:**
  - Pulled NBA player statistics using 'nba_api' (https://github.com/swar/nba_api) and converted output into a CSV file
  - Collected and structured contract data from Basketball Reference (https://www.basketball-reference.com/contracts/players.html) into raw CSV format
  - Stored both datasets for further processing

- **Artifacts:**
  - 'scripts/nba_API_RAW.py'
  - 'data/raw/nba_contracts_raw.csv'
  - 'data/raw/nba_player_stats.csv'
 
### Data Cleaning & Alignment

- **Status:** In Progress
- **Description:**   We implemented a data cleaning pipeline using Python (pandas) to prepare both datasets for integration and analysis. This involved reviewing missing values, standardizing formats, and filtering observations.

- **Progress:**
  - Inspected data sets for missing values using '.isnull().sum()'
  - Cleaned salary data by removing '$' and ',' symbols and converting to numeric format
  - Standardized column names and formats across datasets
  - Filtered out players with fewer than 8 games played
  - Renamed columns for consistency (e.g. 'PLAYER_NAME' -> 'player_name')
 
- **Artifacts:**
  - 'scripts/data_cleaning.py'
  - 'data/processed/nba_contracts_cleaned.csv'
  - 'data/processed/nba_player_stats_cleaned.csv'

## 2. Updated Timeline
- Data Cleaning and Alignment - 4/6 to 4/20
  - Look over datasets for any data quality issues or errors - Alex and Rick
    - This includes scanning for any null values, formatting differences, inconsistencies, or duplications
 - Clean the datasets through python by fixing any issues or errors that may still exist in the datasets - Rick
 - Standardize all data columns - Alex
 - - Making numerical values like salary or games played INT without any other symbols such as $ or %
 - - Making string values like name or NBA team into all lowercase to avoid confusion and make data more consistent

- Data Integration - 4/13 to 4/20
- - Create primary keys for dataset: player_name and season - Alex
- - Create new column for EtD ratio using other column variables - Rick

- Analysis of Integrated Data - 4/20 to 4/30
- - Organize the players into different archetypes previously mentioned - Rick
- - - Veteran stars, mid-level role players, rookies, and 3-and-D
- - Run a regression analysis model to chart the players to find if some positions bring more value than others or if certain skills translate into a player being better overall player - Alex and Rick
- - - Looks at salary as the dependent variable
- - - Skills like free-throw percentage, ppg, assists, rebounds, spg, etc. 

-  Documentation of Data - 4/20 to 4/30
- - Build a data dictionary that defines columns, such as defining EtD and explaining the math and reasoning behind our choices - Alex
- - Documenting the source URLs for datasets, API version numbers, and dates when data was accessed to account for any changes - Rick

- Finalize Project and Review - May 1st to May 5th (Final Project Submission)
- - Complete the project report with findings of our analysis - Alex and Rick
- - Verify end-to-end automated script to ensure that the code can be re-run with different data from a new season - Alex and Rick


## 3. Changes to Project Plan

- The original plan proposed using the site called Spotrac (https://www.spotrac.com/nba/contracts) as the primary source for contract data. However, we encountered limitations with exporting data. As a result, we switched to Basketball Reference (https://www.basketball-reference.com/contracts/players.html) as the primary source of contract data.
- We narrowed the scope of the project to focus specifically on the **2025-2026 NBA season**. This change simplifies data alignment and ensures better consistency across datasets.
- We are putting a larger emphasis on standardizing player names across datasets, as this is important for accurate data integration when there is no shared unique identifier. 

## 4. Challenges & Solutions

### Challenge 1: Data Type Inconsistencies
- **Issue:** Salary values were stored as strings with symbols (e.g., '$59,606,817')
- **Solution:** Removed formatting characters and converted the column into numeric data types

### Challenge 2: Lack of Unique Identifier
- **Issue:** No shared unique ID between the nba_player_stats_cleaned.csv and the nba_contracts_cleaned.csv.
- **Solution:** Will standardize player names and use a composite key, most likely ('player_name', 'season') for merging. 


## Team Member Contributions

### Rick Hu
- Collected contract data from Basketball Reference and structured it into a usable CSV format
- Developed and implemented data cleaning steps
- Implemented API data extraction from 'nba_api'
- Designed data cleaning pipeline
- Contributed to planning for data integration and modeling
