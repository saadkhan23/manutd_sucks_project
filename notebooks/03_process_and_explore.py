"""
Manchester United Performance Analysis (2000-2025)
===================================================

This notebook processes the scraped FBRef data and analyzes Manchester United's
performance decline over the past 10+ years.

Author: Data-driven analysis of Man Utd's struggles
Date: 2025-10-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import warnings

warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("=" * 80)
print("MANCHESTER UNITED PERFORMANCE ANALYSIS")
print("=" * 80)

# ============================================================================
# 1. LOAD AND COMBINE SQUAD STANDARD STATS (Available for all seasons)
# ============================================================================

print("\n[1/5] Loading squad standard statistics...")

data_dir = Path("data/raw")
standard_files = sorted(glob.glob(str(data_dir / "fbref_squad_standard_*.csv")))

print(f"Found {len(standard_files)} squad standard stat files")

# Load all files into a list
dfs = []
for file in standard_files:
    try:
        df = pd.read_csv(file, header=[0, 1])

        # Flatten multi-level columns
        new_cols = []
        for col in df.columns.values:
            # If second level is unnamed, use first level only
            if 'Unnamed' in str(col[1]):
                new_cols.append(col[0])
            # If first level is unnamed, use second level only
            elif 'Unnamed' in str(col[0]):
                new_cols.append(col[1])
            # If both have values, combine them
            elif col[1] != '' and col[1] != col[0]:
                new_cols.append(f"{col[0]}_{col[1]}")
            # Otherwise just use first level
            else:
                new_cols.append(col[0])

        df.columns = new_cols

        # Clean column names
        df.columns = (df.columns
                      .str.replace(r'Unnamed: \d+_level_0', '', regex=True)
                      .str.strip('_')
                      .str.lower()
                      .str.replace(' ', '_')
                      .str.replace('-', '_')
                      .str.replace('+', '_')
                      .str.replace('/', '_'))

        dfs.append(df)
    except Exception as e:
        print(f"Error loading {file}: {e}")

# Combine all dataframes
df_combined = pd.concat(dfs, ignore_index=True)

print(f"Total rows loaded: {len(df_combined)}")
print(f"Seasons covered: {df_combined['season'].nunique()}")
print(f"Teams in dataset: {df_combined['squad'].nunique()}")

# ============================================================================
# 2. CLEAN AND STANDARDIZE DATA
# ============================================================================

print("\n[2/5] Cleaning and standardizing data...")

# Remove rows with missing squad names
df_combined = df_combined.dropna(subset=['squad'])

# Standardize team names (optional - FBRef is already pretty consistent)
team_name_map = {
    'Manchester Utd': 'Manchester United',
    'Manchester City': 'Manchester City',
    'Tottenham': 'Tottenham Hotspur',
}

df_combined['squad_clean'] = df_combined['squad'].replace(team_name_map)

# Convert numeric columns
numeric_cols = ['playing_time_mp', 'playing_time_90s',
                'performance_gls', 'performance_ast', 'performance_g_a',
                'performance_g_pk', 'performance_pk', 'performance_pkatt',
                'performance_crdy', 'performance_crdr']

for col in numeric_cols:
    if col in df_combined.columns:
        df_combined[col] = pd.to_numeric(df_combined[col], errors='coerce')

# Create season start year for easier plotting
df_combined['season_start_year'] = df_combined['season'].str[:4].astype(int)

print("Data cleaning complete!")
print(f"Columns available: {len(df_combined.columns)}")

# ============================================================================
# 3. FOCUS ON MANCHESTER UNITED
# ============================================================================

print("\n[3/5] Filtering for Manchester United...")

# Filter for Man Utd
man_utd = df_combined[df_combined['squad'].str.contains('Manchester Utd', case=False)].copy()
man_utd = man_utd.sort_values('season_start_year')

print(f"Manchester United seasons found: {len(man_utd)}")
print(f"Season range: {man_utd['season'].min()} to {man_utd['season'].max()}")

# Display key stats
print("\nKey statistics overview:")
print(man_utd[['season', 'performance_gls', 'performance_ast',
               'performance_crdy', 'performance_crdr']].head(10))

# ============================================================================
# 4. CALCULATE KEY METRICS FOR ANALYSIS
# ============================================================================

print("\n[4/5] Calculating key metrics...")

# Goals per game
if 'playing_time_mp' in man_utd.columns and 'performance_gls' in man_utd.columns:
    man_utd['goals_per_game'] = man_utd['performance_gls'] / man_utd['playing_time_mp']

# Assists per game
if 'playing_time_mp' in man_utd.columns and 'performance_ast' in man_utd.columns:
    man_utd['assists_per_game'] = man_utd['performance_ast'] / man_utd['playing_time_mp']

# Goal contribution (G+A) per game
if 'playing_time_mp' in man_utd.columns and 'performance_g_a' in man_utd.columns:
    man_utd['goal_contribution_per_game'] = man_utd['performance_g_a'] / man_utd['playing_time_mp']

# Cards per game
if 'playing_time_mp' in man_utd.columns and 'performance_crdy' in man_utd.columns:
    man_utd['yellow_cards_per_game'] = man_utd['performance_crdy'] / man_utd['playing_time_mp']

# Define key periods
man_utd['period'] = man_utd['season_start_year'].apply(
    lambda x: 'Ferguson Era (2000-2013)' if x <= 2013
    else 'Post-Ferguson (2013-2020)' if x <= 2020
    else 'Recent Years (2020+)'
)

print("Metrics calculated successfully!")

# ============================================================================
# 5. EXPLORATORY ANALYSIS & VISUALIZATION
# ============================================================================

print("\n[5/5] Creating visualizations...")

# Create output directory for plots
output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# ---- Plot 1: Goals Scored Over Time ----
fig, ax = plt.subplots(figsize=(14, 8))

if 'performance_gls' in man_utd.columns:
    ax.plot(man_utd['season_start_year'], man_utd['performance_gls'],
            marker='o', linewidth=2, markersize=8, color='#DA291C', label='Total Goals')

    # Add Ferguson retirement line
    ax.axvline(x=2013, color='black', linestyle='--', linewidth=2, alpha=0.7,
               label='Ferguson Retirement (2013)')

    ax.set_xlabel('Season', fontsize=12, fontweight='bold')
    ax.set_ylabel('Goals Scored', fontsize=12, fontweight='bold')
    ax.set_title('Manchester United: Goals Scored Per Season (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / '01_man_utd_goals_timeline.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / '01_man_utd_goals_timeline.png'}")

# ---- Plot 2: Goals Per Game Over Time ----
fig, ax = plt.subplots(figsize=(14, 8))

if 'goals_per_game' in man_utd.columns:
    ax.plot(man_utd['season_start_year'], man_utd['goals_per_game'],
            marker='o', linewidth=2, markersize=8, color='#DA291C', label='Goals per Game')

    # Add Ferguson retirement line
    ax.axvline(x=2013, color='black', linestyle='--', linewidth=2, alpha=0.7,
               label='Ferguson Retirement (2013)')

    # Add mean line
    overall_mean = man_utd['goals_per_game'].mean()
    ax.axhline(y=overall_mean, color='gray', linestyle=':', linewidth=2, alpha=0.5,
               label=f'Overall Average ({overall_mean:.2f})')

    ax.set_xlabel('Season', fontsize=12, fontweight='bold')
    ax.set_ylabel('Goals Per Game', fontsize=12, fontweight='bold')
    ax.set_title('Manchester United: Goals Per Game (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / '02_man_utd_goals_per_game.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / '02_man_utd_goals_per_game.png'}")

# ---- Plot 3: Disciplinary Record (Cards) ----
fig, ax = plt.subplots(figsize=(14, 8))

if 'performance_crdy' in man_utd.columns:
    ax.bar(man_utd['season_start_year'], man_utd['performance_crdy'],
           color='#FDB913', alpha=0.7, label='Yellow Cards')

    if 'performance_crdr' in man_utd.columns:
        ax.bar(man_utd['season_start_year'], man_utd['performance_crdr'],
               bottom=man_utd['performance_crdy'], color='#DA291C', alpha=0.9, label='Red Cards')

    ax.axvline(x=2013, color='black', linestyle='--', linewidth=2, alpha=0.7,
               label='Ferguson Retirement (2013)')

    ax.set_xlabel('Season', fontsize=12, fontweight='bold')
    ax.set_ylabel('Number of Cards', fontsize=12, fontweight='bold')
    ax.set_title('Manchester United: Disciplinary Record (2000-2025)',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(output_dir / '03_man_utd_cards.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / '03_man_utd_cards.png'}")

# ---- Plot 4: Comparative Periods Analysis ----
if 'goals_per_game' in man_utd.columns:
    period_stats = man_utd.groupby('period').agg({
        'goals_per_game': 'mean',
        'assists_per_game': 'mean',
        'goal_contribution_per_game': 'mean'
    }).round(3)

    fig, ax = plt.subplots(figsize=(12, 7))
    period_stats.plot(kind='bar', ax=ax, color=['#DA291C', '#FDB913', '#000000'])

    ax.set_xlabel('Period', fontsize=12, fontweight='bold')
    ax.set_ylabel('Per Game Average', fontsize=12, fontweight='bold')
    ax.set_title('Manchester United: Performance by Era',
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(['Goals/Game', 'Assists/Game', 'Goal Contribution/Game'], fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig(output_dir / '04_man_utd_period_comparison.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / '04_man_utd_period_comparison.png'}")

# ============================================================================
# 6. SUMMARY STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)

# Compare Ferguson Era vs Post-Ferguson
ferguson_era = man_utd[man_utd['season_start_year'] <= 2013]
post_ferguson = man_utd[man_utd['season_start_year'] > 2013]

print("\nFERGUSON ERA (2000-2013):")
print(f"  Average Goals per Game: {ferguson_era['goals_per_game'].mean():.3f}")
if 'assists_per_game' in ferguson_era.columns:
    print(f"  Average Assists per Game: {ferguson_era['assists_per_game'].mean():.3f}")
if 'goal_contribution_per_game' in ferguson_era.columns:
    print(f"  Average Goal Contribution per Game: {ferguson_era['goal_contribution_per_game'].mean():.3f}")

print("\nPOST-FERGUSON ERA (2014-2025):")
print(f"  Average Goals per Game: {post_ferguson['goals_per_game'].mean():.3f}")
if 'assists_per_game' in post_ferguson.columns:
    print(f"  Average Assists per Game: {post_ferguson['assists_per_game'].mean():.3f}")
if 'goal_contribution_per_game' in post_ferguson.columns:
    print(f"  Average Goal Contribution per Game: {post_ferguson['goal_contribution_per_game'].mean():.3f}")

print("\nCHANGE:")
goals_change = ((post_ferguson['goals_per_game'].mean() / ferguson_era['goals_per_game'].mean()) - 1) * 100
print(f"  Goals per Game: {goals_change:+.1f}%")

# ============================================================================
# 7. SAVE PROCESSED DATA
# ============================================================================

print("\n" + "=" * 80)
print("SAVING PROCESSED DATA")
print("=" * 80)

# Save Man Utd data
man_utd.to_csv('data/processed/man_utd_standard_stats.csv', index=False)
print("Saved: data/processed/man_utd_standard_stats.csv")

# Save full combined data
df_combined.to_csv('data/processed/all_teams_standard_stats.csv', index=False)
print("Saved: data/processed/all_teams_standard_stats.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nNext steps:")
print("1. Review the generated plots in data/processed/plots/")
print("2. Analyze additional stat types (defensive, possession, passing, etc.)")
print("3. Compare Man Utd to other top teams (Man City, Liverpool, Arsenal)")
print("4. Investigate specific problem areas (attack, defense, midfield)")
