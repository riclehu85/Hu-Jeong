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
