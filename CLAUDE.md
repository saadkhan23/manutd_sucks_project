# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project focused on scraping and analyzing Premier League football statistics from FBRef. The project collects comprehensive squad-level statistics across multiple seasons (2000-2025) including standard stats, shooting, passing, defensive actions, possession, and more.

## Development Environment

- **Python Version**: Python 3.13.2
- **Virtual Environment**: `venv/` (already set up)
- **Dependencies**: Install via `pip install -r requirements.txt`

### Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

## Project Structure

```
manutd_sucks_project/
├── notebooks/              # Analysis and scraping scripts
│   ├── 01_clean_fbref_data.py           # Single season scraper with cleaning
│   └── 02_scrape_fbref_all_seasons.py   # Batch scraper for all seasons (2000-2025)
├── scripts/               # Deprecated scripts (moved to notebooks/)
├── data/
│   ├── raw/              # Scraped CSV files (140+ files)
│   ├── processed/        # Cleaned/transformed data
│   └── fbref_scrape_log.csv  # Scraping status log
├── app/
│   └── components/       # Application components (empty placeholder)
├── assets/               # Static assets
├── config.yaml           # Configuration file (empty)
└── requirements.txt      # Python dependencies
```

## Key Scripts

### 1. Single Season Scraper (`notebooks/01_clean_fbref_data.py`)

Scrapes a single Premier League season from FBRef with data cleaning.

**Function**: `scrape_league_table(season_url: str, season_label: str) -> pd.DataFrame`

**Usage**:
```bash
python3 notebooks/01_clean_fbref_data.py
```

**What it does**:
- Fetches league table data from FBRef
- Cleans and standardizes column names (rank, team, matches, wins, goals_for, points, etc.)
- Adds season label to the dataframe
- Saves to `data/raw/fbref_league_table_{season}.csv`

### 2. Batch Scraper (`notebooks/02_scrape_fbref_all_seasons.py`)

Scrapes all seasons from 2000-2025 with rate limiting and retry logic.

**Usage**:
```bash
python3 notebooks/02_scrape_fbref_all_seasons.py
```

**What it scrapes** (11 table types per season):
- `squad_standard` - Squad Standard Stats
- `squad_shooting` - Squad Shooting
- `squad_passing` - Squad Pass Types
- `squad_goal_shot_creation` - Squad Goal and Shot Creation
- `squad_defensive` - Squad Defensive Actions
- `squad_possession` - Squad Possession
- `squad_playing_time` - Squad Playing Time
- `squad_misc` - Squad Miscellaneous Stats
- `squad_goalkeeping` - Squad Goalkeeping
- `squad_adv_goalkeeping` - Squad Advanced Goalkeeping
- `league_table` - Premier League Table

**Features**:
- Automatic retry logic with exponential backoff
- Rate limiting (4-7 seconds between tables, 5-10 seconds between seasons)
- Skips already-scraped seasons
- Logs scraping status to `data/fbref_scrape_log.csv`
- Rotates user agents to mimic human behavior
- Handles commented-out HTML tables (FBRef embeds some tables in comments)

**Data Coverage** (as of last scrape):
- 2000-2017: Limited stats (standard, shooting, playing_time, misc)
- 2017-2025: Full stats (all 11 table types)
- Goalkeeping and league table data are missing for all seasons

## Architecture Notes

### Web Scraping Approach

The scraper uses a two-stage approach:

1. **Find the div container**: Uses `DIV_ID_MAP` to locate specific stat tables by ID
2. **Extract from comments**: FBRef often embeds tables inside HTML comments to reduce initial page load. The scraper checks for `Comment` nodes and parses them as BeautifulSoup objects.

Example div IDs:
- Standard stats: `all_stats_squads_standard`
- Shooting: `all_stats_squads_shooting`
- Defensive: `all_stats_squads_defense`

### Rate Limiting Strategy

To avoid being blocked by FBRef:
- Initial wait of 10-20 seconds before starting
- 4-7 second delay between individual table scrapes
- 5-10 second delay between seasons
- 60-90 second backoff on errors
- Session with retry strategy (3 retries, backoff factor of 10)
- Random user agent rotation

### Data Naming Convention

All scraped files follow the pattern:
```
fbref_{table_type}_{season}.csv
```

Examples:
- `fbref_squad_standard_2024-25.csv`
- `fbref_squad_defensive_2017-18.csv`

Each CSV includes a `season` column for easy concatenation.

### Understanding the Scrape Log

The `data/fbref_scrape_log.csv` file tracks what was successfully scraped:
- `yes` = data exists
- `missing` = table not available on FBRef for that season
- `error` = scraping failed

This log is used to skip already-scraped data on subsequent runs.

## Common Development Workflows

### Scraping New Data

```bash
# Activate environment
source venv/bin/activate

# Run the batch scraper (it will skip already-scraped seasons)
python3 notebooks/02_scrape_fbref_all_seasons.py

# Check the log to see what was scraped
cat data/fbref_scrape_log.csv
```

### Working with Scraped Data

```python
import pandas as pd
import glob

# Load all standard stats across seasons
files = glob.glob("data/raw/fbref_squad_standard_*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Filter for a specific team
man_utd = df[df['Squad'].str.contains('Manchester Utd', case=False)]
```

## Notes for Future Development

- The `app/components/` directory is a placeholder for future visualization/dashboard work
- The `scripts/scrape_fbref.py` file is deprecated (code moved to notebooks)
- The `config.yaml` file is currently empty but may be used for centralizing scraper configuration
- Consider implementing incremental scraping logic to only fetch the current season's latest data
- The scraper currently doesn't handle player-level stats (only squad-level)
