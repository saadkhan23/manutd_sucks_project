import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_league_table(season_url: str, season_label: str) -> pd.DataFrame:
    """
    Scrape the Premier League league table from a given FBRef season URL.
    
    Args:
        season_url (str): URL to the season's FBRef page.
        season_label (str): Label for the season, e.g., "2024-2025"
    
    Returns:
        pd.DataFrame: Cleaned league table for that season
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(season_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'lxml')

    # Locate the league table
    table = soup.find("table")
    if table is None:
        raise Exception("Couldn't find the league standings table on this page.")

    df = pd.read_html(str(table))[0]

    # Clean up columns
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "pct")
        .str.replace("/", "_")
    )

    # Add season label
    df["season"] = season_label

    # Standardize column names based on FBRef layout
    rename_map = {
        "rk": "rank",
        "squad": "team",
        "mp": "matches",
        "w": "wins",
        "d": "draws",
        "l": "losses",
        "gf": "goals_for",
        "ga": "goals_against",
        "gd": "goal_difference",
        "pts": "points",
        "xg": "expected_goals",
        "xga": "expected_goals_against",
        "xgd": "expected_goal_difference",
        "xgd_90": "xgd_per_90"
    }

    df = df.rename(columns=rename_map)

    # Keep only relevant columns, but check for existence to avoid KeyError
    cols_to_keep = [
        "rank", "team", "matches", "wins", "draws", "losses",
        "goals_for", "goals_against", "goal_difference",
        "points", "expected_goals", "expected_goals_against",
        "expected_goal_difference", "xgd_per_90", "season"
    ]
    available_cols = [col for col in cols_to_keep if col in df.columns]
    df_clean = df[available_cols].dropna()
    return df_clean


if __name__ == "__main__":
    url = "https://fbref.com/en/comps/9/2024-2025/2024-2025-Premier-League-Stats"
    season_label = "2024-2025"

    try:
        df = scrape_league_table(url, season_label)
        output_path = f"data/raw/fbref_league_table_{season_label}.csv"
        df.to_csv(output_path, index=False)
        print(f"✅ Scraped and saved league table to {output_path}")
        print(df.head())
    except Exception as e:
        print("❌ Error during scraping:", e)