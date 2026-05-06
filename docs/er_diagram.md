# Entity-Relationship Diagram

This project integrates two source datasets into a single analytical dataset.

```mermaid
erDiagram
    NBA_PLAYER_STATS {
        int player_id PK
        string player_name
        string team
        float age
        int gp
        float minutes
        float pie
        float usage_pct
        float def_rating
        string season
    }

    NBA_CONTRACTS {
        string player_name
        string team
        float salary
        float guaranteed
        string season
    }

    NBA_MERGED {
        int player_id PK
        string player_name
        float pie
        float salary
        float etd_pie
        string archetype
    }

    NBA_PLAYER_STATS ||--o| NBA_MERGED : "joined via player_id"
    NBA_CONTRACTS ||--o| NBA_MERGED : "joined via normalized player_name"
```

## Notes

- The two source datasets have no shared unique identifier. Integration is performed via normalized player name matching (Unicode decomposition, ASCII coercion, suffix removal, lowercasing, punctuation removal).
- `player_id` is unique within `nba_player_stats` and is preserved as the primary key in the merged dataset.
- `player_name` in `nba_contracts` is treated as a candidate key for matching purposes only.
- Of 520 cleaned stats rows, 411 matched to contract rows; 109 stats rows had no contract match (predominantly free agents and two-way contract players).
