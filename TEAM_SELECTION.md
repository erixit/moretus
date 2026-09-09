# Team Selection Rules

## Overview

The Moretus team selection system is based on a structured strength-based ranking system that ensures fair and competitive team composition while maintaining flexibility in player positioning.

## Rules

### 1. Strength List Foundation
- The club maintains a **Strength List (Sterktelijst)** of all registered players
- This list is ordered by **Strength List ELO** rating (highest to lowest)
- All team selection follows this established order

### 2. Team Composition
- Each round, **exactly 6 players** are selected for the team
- Selected players must be ranked according to their position in the Strength List
- The team's primary ranking is based on Strength List positions (1st strongest, 2nd strongest, etc.)

### 3. Board Placement Rules
- Each player can be placed at **maximum ±2 boards** from their Strength List ranking
- This means players have flexibility in position while maintaining competitive balance

**Example:**
- Player ranked **3rd** in the Strength List can be assigned to play on:
  - Board 1 (2 positions higher)
  - Board 2 (1 position higher)
  - **Board 3 (their base ranking)**
  - Board 4 (1 position lower)
  - Board 5 (2 positions lower)

### 4. Board Assignment Constraints
For a 6-player team:
- **1st (strongest)**: Can play on boards 1-3
- **2nd**: Can play on boards 1-4
- **3rd**: Can play on boards 1-5
- **4th**: Can play on boards 2-6
- **5th**: Can play on boards 3-6
- **6th (weakest)**: Can play on boards 4-6

## Implementation Phases

### Phase 1 (Current)
- ✅ Select 6 players from the available pool
- ✅ Display team sorted by Strength List ELO (descending)
- ✅ Show team statistics and export options

### Phase 2 (Planned)
- Allow flexible board assignment with ±2 board rule
- Visual interface for drag-and-drop board positioning
- Validation to ensure rules are followed

### Phase 3 (Planned)
- Team performance analysis
- Historical team comparisons
- Optimal team configurations suggestions

## Notes

- The Strength List is determined by the club and represents player skill levels
- The ±2 board flexibility allows tactical adjustments while maintaining competitive integrity
- All team compositions must comply with these rules for official matches
