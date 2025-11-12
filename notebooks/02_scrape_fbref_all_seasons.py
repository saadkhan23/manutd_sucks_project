import os
import time
import pandas as pd
from bs4 import BeautifulSoup, Comment
import requests
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
print("🟢 Starting scrape of all seasons...")
# ---- Configuration ----
BASE_URL = "https://fbref.com"
COMPETITION_URL_TEMPLATE = BASE_URL + "/en/comps/9/{season_id}/{season_str}-Premier-League-Stats"
SEASONS = list(range(2000, 2026))  # 2000 to 2025
OUTPUT_DIR = "data/raw"
LOG_PATH = "data/fbref_scrape_log.csv"

# Tables we want to scrape
TABLES = {
    "squad_standard": "Squad Standard Stats",
    "squad_shooting": "Squad Shooting",
    "squad_passing": "Squad Pass Types",
    "squad_goal_shot_creation": "Squad Goal and Shot Creation",
    "squad_defensive": "Squad Defensive Actions",
    "squad_possession": "Squad Possession",
    "squad_playing_time": "Squad Playing Time",
    "squad_misc": "Squad Miscellaneous Stats",
    "squad_goalkeeping": "Squad Goalkeeping",
    "squad_adv_goalkeeping": "Squad Advanced Goalkeeping",
    "league_table": "Premier League Table",
}

DIV_ID_MAP = {
    "squad_standard": "all_stats_squads_standard",
    "squad_shooting": "all_stats_squads_shooting",
    "squad_passing": "all_stats_squads_passing",
    "squad_goal_shot_creation": "all_stats_squads_gca",
    "squad_defensive": "all_stats_squads_defense",
    "squad_possession": "all_stats_squads_possession",
    "squad_playing_time": "all_stats_squads_playing_time",
    "squad_misc": "all_stats_squads_misc",
    "squad_goalkeeping": "all_stats_keeper_squads",
    "squad_adv_goalkeeping": "all_stats_keeper_adv_squads",
    "league_table": "all_stats_league_table",
}

# ---- Ensure output dir exists ----
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---- Initialize logging ----
log_data = []

# ---- Setup session with retries and headers ----
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=10,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
]

session.headers.update({
    "User-Agent": random.choice(user_agents),
    "Referer": "https://fbref.com/en/comps/9/Premier-League-Stats",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
})

# ---- Scrape all available seasons ----
SEASONS = list(range(2000, 2026))  # 2000 to 2025

print("⏳ Waiting before starting scrape to mimic human behavior...")
time.sleep(random.uniform(10.0, 20.0))

# ---- Main scrape loop ----
for season in SEASONS:
    already_scraped = all(
        os.path.exists(f"{OUTPUT_DIR}/fbref_{key}_{season}-{(season + 1) % 100:02d}.csv")
        for key in TABLES
    )
    if already_scraped:
        print(f"⏭️ Skipping {season} (already scraped)")
        continue

    print(f"📅 Scraping {season}...")
    season_str = f"{season}-{(season + 1) % 100:02d}"
    season_id = f"{season}-{season + 1}"
    url = COMPETITION_URL_TEMPLATE.format(season_id=season_id, season_str=season_str)

    try:
        print(f"🔍 Fetching URL: {url}")
        response = session.get(url, timeout=15)
        response.raise_for_status()
        if response.status_code != 200:
            print(f"❌ HTTP Error {response.status_code} for {url}")
            log_data.append({**{"season": season_str}, **{k: "missing" for k in TABLES}})
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        season_log = {"season": season_str}

        for key, label in TABLES.items():
            found = False
            div_id = DIV_ID_MAP.get(key)
            if not div_id:
                print(f"⚠️ No div ID found for {key}")
                season_log[key] = "missing"
                continue

            table_div = soup.find("div", id=div_id)
            if not table_div:
                print(f"⚠️ Div not found: {div_id} for {key}")
                season_log[key] = "missing"
                continue

            comment = next((c for c in table_div.children if isinstance(c, Comment)), None)
            table_soup = BeautifulSoup(comment, "html.parser") if comment else table_div

            try:
                table = table_soup.find("table")
                if table:
                    df = pd.read_html(str(table))[0]
                    filename = f"{OUTPUT_DIR}/fbref_{key}_{season_str}.csv"
                    df["season"] = season_str
                    df.to_csv(filename, index=False)
                    found = True
            except Exception as e:
                print(f"⚠️ Error processing {key} ({label}) for {season_str}: {e}")

            if not found:
                print(f"⚠️ Table not found: {key} ({label}) in {season_str}")
            season_log[key] = "yes" if found else "missing"
            time.sleep(random.uniform(4.0, 7.0))

        log_data.append(season_log)
        print(f"✅ Done {season_str}")
        time.sleep(random.uniform(5.0, 10.0))  # Light pause after a season

    except Exception as e:
        print(f"🔥 Exception occurred for {season_str}: {e}")
        sys.stdout.flush()
        time.sleep(random.uniform(60.0, 90.0))  # back off harder on errors
        log_data.append({**{"season": season_str}, **{k: "error" for k in TABLES}})

# ---- Save log ----
log_df = pd.DataFrame(log_data)
log_df.to_csv(LOG_PATH, index=False)
print("📄 Log saved to:", LOG_PATH)