# Manchester United Analysis Project - AI Context Document

## 1. What the Project Does

**"Why Has Man Utd Struggled for 10+ Years?"** is a data analysis and web scraping project that systematically collects and analyzes Premier League football statistics to understand Manchester United's dramatic decline since Sir Alex Ferguson's retirement in 2013.

The project scrapes comprehensive squad-level statistics from FBRef (an authoritative sports reference database) covering 26 seasons (2000-2025) and performs comparative analysis against rival teams (Man City, Liverpool, Arsenal, Chelsea).

**Key Question:** How much has Man Utd actually declined, and why?

**Key Finding:** 23% decline in goals per game since Ferguson, while rivals improved. Seven different managers with no clear philosophy.

---

## 2. Architecture

### Overall Pipeline
```
FBRef Website (fbref.com)
  ↓
  ├─ Season 2000-2025 (26 seasons)
  ├─ 11 stat types per season (squad standard, shooting, passing, defense, etc.)
  └─ ~2,860 total table requests
  ↓
Scraper (02_scrape_fbref_all_seasons.py)
  ├─ BeautifulSoup4 (HTML parsing)
  ├─ requests with retry logic (HTTP)
  ├─ Rate limiting (avoid blocks)
  └─ Logs progress to fbref_scrape_log.csv
  ↓
data/raw/ (140+ CSV files)
  ├─ fbref_squad_standard_2024-25.csv
  ├─ fbref_squad_shooting_2024-25.csv
  ├─ fbref_squad_defensive_2017-18.csv
  └─ ... (one file per table per season)
  ↓
Analysis Notebooks (03-09)
  ├─ Load CSVs into Pandas dataframes
  ├─ Clean and transform data
  ├─ Calculate metrics (goals/game, win rates, etc.)
  ├─ Compare across seasons and teams
  ├─ Generate visualizations
  └─ Export findings
  ↓
Output
  ├─ ANALYSIS_SUMMARY.md (key findings)
  ├─ PNG charts (Matplotlib, Plotly)
  ├─ Data insights (manager performance, tactical breakdown)
  └─ Portfolio integration (displayed on portfolio site)
```

### Directory Structure
```
manutd_sucks_project/
├── notebooks/                        # Analysis and scraping scripts
│   ├── 01_clean_fbref_data.py       # Single season scraper (starter)
│   ├── 02_scrape_fbref_all_seasons.py # Production scraper (26 seasons)
│   ├── 03_process_and_explore.py    # Load and clean all data
│   ├── 04_enhanced_visualizations.py # Create charts
│   ├── 05_rival_comparison.py       # Compare vs City, Liverpool, Arsenal
│   ├── 06_tactical_analysis.py      # Possession, passing, defense stats
│   ├── 07_improved_rival_comparison.py # Advanced analysis
│   ├── 08_manager_win_rates.py      # Manager-by-manager breakdown (Nov 2025)
│   └── 09_attacking_defensive_transfer_analysis.py # Transfer analysis
│
├── data/
│   ├── raw/                         # All scraped CSV files
│   │   ├── fbref_squad_standard_2024-25.csv
│   │   ├── fbref_squad_shooting_2024-25.csv
│   │   ├── fbref_squad_defensive_2017-18.csv
│   │   └── ... (140+ files, named pattern: fbref_[type]_[season].csv)
│   │
│   ├── processed/                   # Cleaned/transformed data
│   │   ├── man_utd_timeseries.csv
│   │   └── rival_comparison.csv
│   │
│   ├── fbref_scrape_log.csv        # Tracks scraping progress
│   │   └── Columns: table_type, season, status (yes/missing/error)
│   │
│   └── [other processed outputs]
│
├── app/                            # Placeholder for future web app
│   └── components/                 # (empty, for future Streamlit/Plotly Dash)
│
├── assets/                         # Static assets
│   └── team_logos/                 # Team logo images for charts
│
├── scripts/                        # Deprecated
│   └── scrape_fbref.py            # (old version, replaced by notebooks/02)
│
├── config.yaml                    # Configuration file (empty, future use)
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview
├── CLAUDE.md                      # Claude AI guidance and architecture
├── ANALYSIS_SUMMARY.md            # Key findings and insights
├── SUPPLEMENTARY_DATA_GUIDE.md    # Data reference
└── venv/                          # Python virtual environment
    ├── bin/
    └── lib/python3.13/site-packages/
```

### Scraper Architecture (02_scrape_fbref_all_seasons.py)

#### Tables Configuration
```python
TABLES = {
    "squad_standard": "all_stats_squads_standard",
    "squad_shooting": "all_stats_squads_shooting",
    "squad_passing": "all_stats_squads_passing",
    "squad_goal_shot_creation": "all_stats_squads_gca",
    "squad_defensive": "all_stats_squads_defense",
    "squad_possession": "all_stats_squads_possession",
    "squad_playing_time": "all_stats_squads_playing_time",
    "squad_misc": "all_stats_squads_misc",
    "squad_goalkeeping": "all_stats_squads_goalkeeper",
    "squad_adv_goalkeeping": "all_stats_squads_goalkeeper_adv",
    "league_table": "all_comps_squads_league_table",
}
```
- **11 stat types per season**
- **26 seasons (2000-2025)** = 286 total tables to scrape

#### Two-Stage HTML Parsing
```python
# Stage 1: Find div container by ID
div = soup.find('div', {'id': DIV_ID_MAP[table_type]})

# Stage 2: Extract from comments (FBRef embeds tables in HTML comments)
for child in div.children:
    if isinstance(child, Comment):
        table = BeautifulSoup(str(child), 'html.parser').find('table')
        # Parse table to DataFrame
```
- FBRef puts tables in HTML comments to reduce page load
- Must recursively parse Comment nodes
- Pandas `.read_html()` wouldn't find commented tables

#### Rate Limiting & Error Handling
```python
Rate Limiting:
  - Initial wait: 10-20 seconds
  - Between tables: 4-7 seconds (random)
  - Between seasons: 5-10 seconds (random)
  - On error: 60-90 second backoff

Retry Logic:
  - Max retries: 3
  - Backoff factor: 10 (1s → 10s → 100s)
  - Total max wait: 111 seconds per error

User Agents:
  - Random rotation to appear human-like
  - "Mozilla/5.0 (Macintosh; Intel Mac OS X...)"
  - Honest identification as automated scraper
```

#### Data Coverage
- **2000-2017:** Limited stats (standard, shooting, playing_time, misc)
- **2017-2025:** Full stats (all 11 types)
- **Goalkeeping data:** Missing for all seasons
- **League table:** Tracked in separate scrapes

### Analysis Notebook Flow

#### 03_process_and_explore.py
1. Load all CSVs from `data/raw/`
2. Combine into single dataframes (one per stat type)
3. Clean data (rename columns, standardize team names)
4. Calculate derived metrics:
   - Goals per game = Goals / Matches
   - Pass completion % = Completed passes / Total passes
   - Win rate = Wins / Matches
5. Filter for Man Utd and rivals
6. Export to `data/processed/`

#### 04_enhanced_visualizations.py
1. Load processed data
2. Create charts:
   - Time series plots (goals/game over seasons)
   - Comparison bar charts (vs rivals)
   - Scatter plots (goals vs defense)
3. Export PNG/SVG for reports

#### 08_manager_win_rates.py
1. Map seasons to managers (Moyes, Van Gaal, Mourinho, Solskjær, Ten Hag, Amorim)
2. Filter data by manager tenure
3. Calculate win rates, goals/game
4. Rank managers by performance
5. Export to CSV/charts

### Data Flow
```
FBRef (Dynamic website)
  ↓ (Playwright or BeautifulSoup requests)
  ↓ (HTML → Dataframe conversion)
CSV files (data/raw/)
  ↓ (Pandas read_csv)
In-memory dataframes
  ↓ (Filtering, aggregation, calculation)
Processed data (data/processed/)
  ↓
Visualizations (charts, plots)
  ↓
Analysis report (ANALYSIS_SUMMARY.md)
  ↓
Portfolio integration (JSON export to portfolio/public/data/)
```

---

## 3. Known Risks / Fragilities

- **FBRef HTML structure dependency**: Scraper relies on specific div IDs and HTML comment pattern. Changes to this structure will break table extraction.
- **Goalkeeping data missing**: Not included in the table configuration (DIV_ID_MAP). No historical goalkeeping stats available for analysis.
- **Pre-2017 partial coverage**: Seasons before 2017 only include subset of stat types (standard, shooting, playing_time, misc). Cross-era comparisons must account for incomplete data.
- **FBRef terms of service**: Scraping depends on continued compliance with FBRef's ToS. Rate limiting, blocking, or policy changes could impact data collection.
- **Single-threaded scraping**: Current implementation is relatively slow; aggressive parallelization could increase risk of being rate-limited or blocked.
- **Manually mapped manager eras**: Manager-to-season mappings are hardcoded. Mid-season manager changes may create overlap or gaps in analysis.

---

## 4. Tech Stack

### Language & Environment
- **Python 3.13.2** - Data analysis language
- **Virtual Environment:** `venv/` (isolated package management)
- **Jupyter Notebooks:** Not used (using .py scripts instead)

### Web Scraping
- **requests 2.31.0+** - HTTP client
  - Session management (persistent connections)
  - Retry strategy (automatic backoff)
  - User-agent rotation
  - Request headers (identify as bot)
  
- **BeautifulSoup4 4.12.0+** - HTML/XML parsing
  - Find divs by ID
  - Extract tables from HTML comments
  - Parse table structure to lists
  
- **lxml 4.9.0+** - Fast C-based parser (used by BeautifulSoup)

### Data Processing
- **pandas 2.0.0+** - Data manipulation
  - Read CSV files
  - DataFrame operations (filter, group, aggregate)
  - Column calculations
  - Export to CSV
  
- **numpy** - Numerical computing (via pandas dependency)

### Data Visualization
- **plotly** - Interactive charts
  - Box plots (showing distribution)
  - Scatter plots (correlation analysis)
  - Bar charts (comparisons)
  - Line plots (trends)
  
- **matplotlib 3.7.0+** - Static plots
  - Time series visualization
  - Multi-panel figures
  - Export to PNG/PDF
  
- **seaborn 0.12.0+** - Enhanced statistical plots
  - Heatmaps
  - Distribution plots
  - Correlation matrices

### Build & Execution
- **Python interpreter** - Run .py scripts directly
- **Command line** - `python3 notebooks/02_scrape_fbref_all_seasons.py`
- **Virtual environment activation** - `source venv/bin/activate`

---

## 5. Data Status

### Current Data
- **CSV files:** 140+ files in `data/raw/`
- **Coverage:** 2000-2025 (26 seasons)
- **Status:** Partially complete (see fbref_scrape_log.csv)
- **Last Updated:** October 14, 2025 (from directory listing)

### CSV Naming Convention
```
fbref_[table_type]_[season].csv

Examples:
  fbref_squad_standard_2024-25.csv
  fbref_squad_shooting_2024-25.csv
  fbref_squad_defensive_2017-18.csv
```

### Sample Data Structure
```
CSV Columns:
  - Rank (int)
  - Squad (str) - Team name
  - Matches (int) - Games played
  - Wins (int)
  - Draws (int)
  - Losses (int)
  - Goals For (int)
  - Goals Against (int)
  - Goal Difference (int)
  - Points (int)
  - season (str) - Added by scraper
  
  + Additional columns by stat type:
    Standard: Goals, Assists, xG, xA
    Shooting: Shots, Shots on Target, Shot %
    Passing: Pass %, Progressive Passes, Assists
    Defensive: Tackles, Interceptions, Blocks
    Possession: Possession %, Touches per game
    Etc.
```

### Data Quality Issues
- **Goalkeeping stats:** Missing for all seasons (not in DIV_ID_MAP)
- **League table:** Incomplete for some seasons
- **2000-2017:** Only 4 stat types (limited coverage)
- **Scrape log:** Some seasons marked "missing" (data not available on FBRef)

### Scrape Log Status (fbref_scrape_log.csv)
```
Columns:
  - table_type (str)
  - season (str)
  - status (str) - "yes", "missing", "error"
  
Statuses:
  "yes" = successfully scraped and saved
  "missing" = table not available on FBRef for that season
  "error" = scraping failed (retry possible)
```

### Data Ready for Analysis
- **Man Utd stats:** Complete for 2000-2025
- **Rival teams:** Complete (Man City, Liverpool, Arsenal, Chelsea)
- **Manager-level analysis:** Can aggregate by date ranges
- **Tactical analysis:** Possession, passing, defense available from 2017+

---

## 6. Pending Tasks / Backlog

### High Priority (Critical for Insights)
- [ ] Re-scrape missing 2023-2024 season data (if incomplete)
- [ ] Investigate goalkeeping stats (add to DIV_ID_MAP or find alternative source)
- [ ] Fix any duplicate rows or data quality issues
- [ ] Validate Man Utd team names across seasons (name changes?)

### Medium Priority (Analysis & Reporting)
- [ ] Complete ANALYSIS_SUMMARY.md with all sections
- [ ] Create comprehensive manager performance visualization
- [ ] Add transfer data analysis (connecting to Transfermarkt?)
- [ ] Generate tactical breakdown for each era
- [ ] Create rival comparison PDF report

### Enhancement Features
- [ ] Build Streamlit web dashboard (interactive exploration)
- [ ] Create Plotly Dash app for drill-down analysis
- [ ] Add player-level stats (currently squad-level only)
- [ ] Implement time-series forecasting (predict next season)
- [ ] Connect to injury/suspension data for context

### Automation
- [ ] Schedule monthly scrapes (cron job or GitHub Actions)
- [ ] Automated weekly/monthly reports
- [ ] Email alerts for significant stats changes
- [ ] Real-time dashboard updates (if moving to web app)

### Technical Debt
- [ ] Refactor scraper into class-based design (OOP)
- [ ] Add logging instead of print statements
- [ ] Unit tests for data validation
- [ ] Error recovery and partial re-scraping
- [ ] Config file instead of hardcoded values

---

## 7. Design Principles

### Web Scraping Ethics
- **Transparency:** Identify as automated bot (User-Agent header)
- **Respect:** Rate limiting (random delays 2-7 seconds)
- **Moderation:** 286 tables over time, not mass harvesting
- **Legal:** Public data from public website, no authentication bypass
- **Terms:** Complies with FBRef's terms of service (review before scraping)

### Code Organization
- **Notebooks:** One analysis task per file (03, 04, 05, etc.)
- **Data:** Organized by processing stage (raw, processed)
- **Configuration:** Centralized in scraper (SEASONS, TABLES, URLS)
- **Naming:** snake_case for files, descriptive names
- **Comments:** Explain WHY, not WHAT

### Data Validation
- Check for null values in critical columns
- Validate team name consistency
- Ensure season ranges are correct
- Spot-check aggregations (hand-verify some calculations)

### Analysis Approach
- **Comparison:** Always compare vs rivals (context)
- **Time-series:** Show trend, not just one season
- **Aggregation:** Use median/percentile, not just average (outliers)
- **Manager era:** Separate analysis by tenure (Mourinho, Van Gaal, etc.)
- **Visualization:** Chart every insight (visual first)

### Error Handling
- **Retry logic:** Automatic exponential backoff
- **Partial completion:** Save what succeeded, log what failed
- **Logging:** Track every request (fbref_scrape_log.csv)
- **Graceful degradation:** Skip missing tables, continue with others

### Documentation
- **CLAUDE.md:** Architecture and development guide
- **ANALYSIS_SUMMARY.md:** Key findings and insights
- **Code comments:** Explain complex logic (especially parsing)
- **README.md:** Overview and getting started

---

## 8. Current Findings Snapshot (as of 2025-11-14)

These findings are based on current scraping and analysis as of 2025-11-14. They may change as new season data arrives or methodology is refined.

### The Decline

- **Ferguson Era (roughly 2000–2013)**: Significantly higher goals per game than post-Ferguson period.
- **Post-Ferguson Decline**: Approximately **20–25% drop** in attacking output compared to Ferguson baseline.
- **Rival Improvement**: Manchester City and Liverpool have both improved meaningfully over the same window, widening the performance gap.

### Manager Performance (Ranked by Attacking Output)

- **Mourinho**: Strongest post-Ferguson attacking numbers, still approximately 10% below Ferguson era
- **Solskjær**: Second-strongest, notable improvement in attacking metrics
- **Moyes, Van Gaal, Ten Hag, Amorim**: All below the post-Ferguson average, with Amorim showing early concerning trends (very early sample size)

### Tactical & Rival Trends

- **Possession and Passing**: Man Utd metrics lag top rivals in recent seasons
- **Rivals (especially Man City)**: Improved across key attacking and progression stats
- **Defensive consistency**: Fluctuated; periods of improvement followed by decline

---

## 9. Questions for AI Helper

### Analysis Direction
1. **What other statistical metrics would strengthen the analysis?**
   - Expected Goals (xG) trends?
   - Player age/experience profile?
   - Injury impact on performance?

2. **Should I focus on tactical vs personnel analysis?**
   - Formation consistency across eras?
   - Defender quality vs striker quality?
   - Midfield balance and progression?

3. **How to handle management transitions?**
   - Should I analyze manager's first season vs steady state?
   - Or use full tenure average?
   - Impact of interim managers (Rangnick)?

### Data Enhancement
4. **Where to get complementary data?**
   - Transfer spending (Transfermarkt API)?
   - Player wages/salary cap?
   - Injury/suspension data?
   - Fixture difficulty ratings?

5. **Should I incorporate non-FBRef data?**
   - Player market values?
   - Fan sentiment from Reddit/Twitter?
   - Media analysis?
   - Injury reports?

### Presentation & Deployment
6. **Web dashboard vs static report?**
   - Should I build Streamlit app for exploration?
   - Or keep as notebook-based analysis?
   - Interactive filters vs static charts?

7. **How to make findings actionable?**
   - Recommendations for the club?
   - Comparison to other struggling teams?
   - Predictive model for next season?

8. **Should I publish this?**
   - Post on Medium or Substack?
   - Share on Reddit r/reddevils or soccer analytics communities?
   - Or keep as portfolio piece?

### Code Quality
9. **Should I refactor the scraper?**
   - Convert to class-based design?
   - Add unit tests?
   - Create configuration management?
   - Implement proper logging?

10. **Performance optimization?**
    - Parallelize scraping (async requests)?
    - Cache intermediate results?
    - Pre-compute common aggregations?
    - Database instead of CSVs?

---

## Setup & Development Guide

### Prerequisites
- Python 3.13 (already installed)
- Virtual environment `venv/` (already created)

### Installation & Setup
```bash
# Navigate to project
cd /Users/saadkhan/Documents/manutd_sucks_project

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas, beautifulsoup4, requests; print('OK')"
```

### Running Scrapers

#### Single Season Scraper (Starter)
```bash
python3 notebooks/01_clean_fbref_data.py
# Scrapes one season as example
# Output: data/raw/fbref_league_table_[season].csv
```

#### Full Batch Scraper (Production)
```bash
python3 notebooks/02_scrape_fbref_all_seasons.py
# Scrapes 2000-2025 (26 seasons, 11 tables each)
# Skips already-scraped data (reads fbref_scrape_log.csv)
# Progress logged to console
# Takes ~2-3 hours for full run
```

### Running Analysis

#### Data Processing
```bash
python3 notebooks/03_process_and_explore.py
# Loads all CSVs from data/raw/
# Cleans and transforms
# Exports to data/processed/
```

#### Visualizations
```bash
python3 notebooks/04_enhanced_visualizations.py
# Creates charts
# Exports PNG/SVG
```

#### Manager Analysis
```bash
python3 notebooks/08_manager_win_rates.py
# Analyzes performance by manager
# Exports manager_performance.csv
```

### Common Workflows

#### Update Data (New Season)
```bash
source venv/bin/activate
python3 notebooks/02_scrape_fbref_all_seasons.py  # Scrapes latest
python3 notebooks/03_process_and_explore.py       # Processes
python3 notebooks/04_enhanced_visualizations.py   # Visualizes
deactivate
```

#### Investigate a Specific Season
```python
# In notebook or interactive Python:
import pandas as pd
df = pd.read_csv('data/raw/fbref_squad_standard_2023-24.csv')
man_utd = df[df['Squad'].str.contains('Manchester Utd', case=False)]
print(man_utd[['Squad', 'Goals', 'xG', 'Points']])
```

#### Compare Two Eras
```python
import pandas as pd
from pandas.concat import concat

# Ferguson era (2000-2013)
ferguson = pd.read_csv('data/raw/fbref_squad_standard_2012-13.csv')
man_utd_ferguson = ferguson[ferguson['Squad'].str.contains('Manchester Utd')]

# Post-Ferguson (2014-2025)
post = pd.read_csv('data/raw/fbref_squad_standard_2024-25.csv')
man_utd_post = post[post['Squad'].str.contains('Manchester Utd')]

# Compare
print(f"Ferguson era goals/game: {man_utd_ferguson['Goals'].mean()}")
print(f"Post-Ferguson goals/game: {man_utd_post['Goals'].mean()}")
print(f"Decline: {((man_utd_post['Goals'].mean() - man_utd_ferguson['Goals'].mean()) / man_utd_ferguson['Goals'].mean() * 100):.1f}%")
```

---

## File Reference

| File | Purpose | When to Edit |
|------|---------|---|
| `02_scrape_fbref_all_seasons.py` | Production scraper | If changing FBRef structure or adding seasons |
| `03_process_and_explore.py` | Data processing | If cleaning rules need updates |
| `04_enhanced_visualizations.py` | Chart generation | When updating visualization style |
| `08_manager_win_rates.py` | Manager analysis | Adding new manager data |
| `config.yaml` | Configuration | When setting up defaults |
| `requirements.txt` | Dependencies | When adding new libraries |
| `data/fbref_scrape_log.csv` | Scrape status | Auto-generated (don't edit) |
| `ANALYSIS_SUMMARY.md` | Findings report | After each analysis update |

---

## Summary

This project demonstrates:
- **Web scraping at scale** (26 seasons, 11 stat types, 286 tables)
- **Data engineering** (HTML parsing, error handling, rate limiting)
- **Statistical analysis** (comparative metrics, trend analysis)
- **Visualization** (time series, scatter plots, comparisons)
- **Domain knowledge** (sports analytics, football metrics)

The main opportunity is transitioning from notebook-based analysis to an interactive web dashboard for exploration and storytelling.

---

## Changelog

- **2025-11-13** — Initialized Multi-AI Coordination Policy. Added Known Risks/Fragilities section and moved volatile findings to dated Current Findings Snapshot section.

