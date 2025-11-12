"""
Manchester United Tactical Analysis: Defense, Possession, Passing
==================================================================

This script analyzes Man Utd's performance across different tactical dimensions
to identify specific problem areas beyond just goal-scoring.

Stats analyzed:
- Defensive Actions (tackles, interceptions, blocks)
- Possession Stats (touches, carries, progressive carries)
- Passing Stats (completion %, progressive passes)

Note: These detailed stats are only available from 2017-2025 seasons.

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

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 10)

print("=" * 80)
print("MANCHESTER UNITED TACTICAL ANALYSIS")
print("=" * 80)

data_dir = Path("data/raw")
output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1. LOAD DEFENSIVE STATS
# ============================================================================

print("\n[1/4] Loading defensive stats (2017-2025)...")

defensive_files = sorted(glob.glob(str(data_dir / "fbref_squad_defensive_*.csv")))
print(f"Found {len(defensive_files)} defensive stat files")

dfs_def = []
for file in defensive_files:
    try:
        df = pd.read_csv(file, header=[0, 1])

        # Flatten columns
        new_cols = []
        for col in df.columns.values:
            if 'Unnamed' in str(col[1]):
                new_cols.append(col[0])
            elif 'Unnamed' in str(col[0]):
                new_cols.append(col[1])
            elif col[1] != '' and col[1] != col[0]:
                new_cols.append(f"{col[0]}_{col[1]}")
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

        dfs_def.append(df)
    except Exception as e:
        print(f"Error loading {file}: {e}")

df_defensive = pd.concat(dfs_def, ignore_index=True)
df_defensive['season_start_year'] = df_defensive['season'].str[:4].astype(int)

print(f"Loaded {len(df_defensive)} rows of defensive data")

# ============================================================================
# 2. LOAD POSSESSION STATS
# ============================================================================

print("\n[2/4] Loading possession stats (2017-2025)...")

possession_files = sorted(glob.glob(str(data_dir / "fbref_squad_possession_*.csv")))
print(f"Found {len(possession_files)} possession stat files")

dfs_poss = []
for file in possession_files:
    try:
        df = pd.read_csv(file, header=[0, 1])

        # Flatten columns (same logic as defensive)
        new_cols = []
        for col in df.columns.values:
            if 'Unnamed' in str(col[1]):
                new_cols.append(col[0])
            elif 'Unnamed' in str(col[0]):
                new_cols.append(col[1])
            elif col[1] != '' and col[1] != col[0]:
                new_cols.append(f"{col[0]}_{col[1]}")
            else:
                new_cols.append(col[0])

        df.columns = new_cols
        df.columns = (df.columns
                      .str.replace(r'Unnamed: \d+_level_0', '', regex=True)
                      .str.strip('_')
                      .str.lower()
                      .str.replace(' ', '_')
                      .str.replace('-', '_')
                      .str.replace('+', '_')
                      .str.replace('/', '_'))

        dfs_poss.append(df)
    except Exception as e:
        print(f"Error loading {file}: {e}")

df_possession = pd.concat(dfs_poss, ignore_index=True)
df_possession['season_start_year'] = df_possession['season'].str[:4].astype(int)

print(f"Loaded {len(df_possession)} rows of possession data")

# ============================================================================
# 3. FILTER FOR MAN UTD AND RIVALS
# ============================================================================

print("\n[3/4] Filtering for Man Utd and rivals...")

rivals = ['Manchester Utd', 'Manchester City', 'Liverpool', 'Arsenal', 'Chelsea']

man_utd_def = df_defensive[df_defensive['squad'].str.contains('Manchester Utd', case=False)].copy()
man_utd_poss = df_possession[df_possession['squad'].str.contains('Manchester Utd', case=False)].copy()

rivals_def = df_defensive[df_defensive['squad'].isin(rivals)].copy()
rivals_poss = df_possession[df_possession['squad'].isin(rivals)].copy()

# Standardize names
rivals_def['squad'] = rivals_def['squad'].replace({'Manchester Utd': 'Man Utd', 'Manchester City': 'Man City'})
rivals_poss['squad'] = rivals_poss['squad'].replace({'Manchester Utd': 'Man Utd', 'Manchester City': 'Man City'})

print(f"Man Utd defensive records: {len(man_utd_def)}")
print(f"Man Utd possession records: {len(man_utd_poss)}")

# ============================================================================
# 4. CREATE VISUALIZATIONS
# ============================================================================

print("\n[4/4] Creating tactical visualizations...")

team_colors = {
    'Man Utd': '#DA291C',
    'Man City': '#6CABDD',
    'Liverpool': '#C8102E',
    'Arsenal': '#EF0107',
    'Chelsea': '#034694'
}

# ---- PLOT 1: Tackles + Interceptions Over Time ----
fig, ax = plt.subplots(figsize=(16, 9))

for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea']:
    team_data = rivals_def[rivals_def['squad'] == team].sort_values('season_start_year')

    if 'tkl_int' in team_data.columns:
        # Normalize by 90s (games played)
        if '90s' in team_data.columns:
            team_data['tkl_int_per_90'] = pd.to_numeric(team_data['tkl_int'], errors='coerce') / pd.to_numeric(team_data['90s'], errors='coerce')
            ax.plot(team_data['season_start_year'], team_data['tkl_int_per_90'],
                    marker='o', linewidth=2.5, markersize=8,
                    color=team_colors.get(team, '#999999'),
                    label=team, alpha=0.85)

ax.set_xlabel('Season', fontsize=13, fontweight='bold')
ax.set_ylabel('Tackles + Interceptions per 90', fontsize=13, fontweight='bold')
ax.set_title('Defensive Actions: Tackles + Interceptions per 90 (2017-2025)',
             fontsize=17, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '13_defensive_actions.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '13_defensive_actions.png'}")

# ---- PLOT 2: Possession % Over Time ----
fig, ax = plt.subplots(figsize=(16, 9))

for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea']:
    team_data = rivals_poss[rivals_poss['squad'] == team].sort_values('season_start_year')

    if 'poss' in team_data.columns:
        team_data['poss_pct'] = pd.to_numeric(team_data['poss'], errors='coerce')
        ax.plot(team_data['season_start_year'], team_data['poss_pct'],
                marker='o', linewidth=2.5, markersize=8,
                color=team_colors.get(team, '#999999'),
                label=team, alpha=0.85)

ax.set_xlabel('Season', fontsize=13, fontweight='bold')
ax.set_ylabel('Possession %', fontsize=13, fontweight='bold')
ax.set_title('Possession % Over Time (2017-2025)',
             fontsize=17, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='best')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '14_possession.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '14_possession.png'}")

# ---- PLOT 3: Progressive Carries (if available) ----
if 'carries_prgc' in df_possession.columns:
    fig, ax = plt.subplots(figsize=(16, 9))

    for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea']:
        team_data = rivals_poss[rivals_poss['squad'] == team].sort_values('season_start_year')

        if 'carries_prgc' in team_data.columns and '90s' in team_data.columns:
            team_data['prgc_per_90'] = pd.to_numeric(team_data['carries_prgc'], errors='coerce') / pd.to_numeric(team_data['90s'], errors='coerce')
            ax.plot(team_data['season_start_year'], team_data['prgc_per_90'],
                    marker='o', linewidth=2.5, markersize=8,
                    color=team_colors.get(team, '#999999'),
                    label=team, alpha=0.85)

    ax.set_xlabel('Season', fontsize=13, fontweight='bold')
    ax.set_ylabel('Progressive Carries per 90', fontsize=13, fontweight='bold')
    ax.set_title('Progressive Carries per 90 (Ball progression upfield - 2017-2025)',
                 fontsize=17, fontweight='bold', pad=20)
    ax.legend(fontsize=12, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / '15_progressive_carries.png', dpi=300, bbox_inches='tight')
    print(f"Saved: {output_dir / '15_progressive_carries.png'}")

# ---- PLOT 4: Man Utd Tactical Dashboard ----
fig, axes = plt.subplots(2, 2, figsize=(18, 14))

# Defensive Actions
if 'tkl_int' in man_utd_def.columns and '90s' in man_utd_def.columns:
    man_utd_def['tkl_int_per_90'] = pd.to_numeric(man_utd_def['tkl_int'], errors='coerce') / pd.to_numeric(man_utd_def['90s'], errors='coerce')
    axes[0, 0].plot(man_utd_def['season_start_year'], man_utd_def['tkl_int_per_90'],
                    marker='o', linewidth=3, markersize=10, color='#DA291C')
    axes[0, 0].set_title('Tackles + Interceptions per 90', fontsize=14, fontweight='bold')
    axes[0, 0].set_ylabel('Per 90', fontsize=12, fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)

# Possession %
if 'poss' in man_utd_poss.columns:
    man_utd_poss['poss_pct'] = pd.to_numeric(man_utd_poss['poss'], errors='coerce')
    axes[0, 1].plot(man_utd_poss['season_start_year'], man_utd_poss['poss_pct'],
                    marker='o', linewidth=3, markersize=10, color='#DA291C')
    axes[0, 1].set_title('Possession %', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Possession %', fontsize=12, fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)

# Touches
if 'touches_touches' in man_utd_poss.columns and '90s' in man_utd_poss.columns:
    man_utd_poss['touches_per_90'] = pd.to_numeric(man_utd_poss['touches_touches'], errors='coerce') / pd.to_numeric(man_utd_poss['90s'], errors='coerce')
    axes[1, 0].plot(man_utd_poss['season_start_year'], man_utd_poss['touches_per_90'],
                    marker='o', linewidth=3, markersize=10, color='#DA291C')
    axes[1, 0].set_title('Touches per 90', fontsize=14, fontweight='bold')
    axes[1, 0].set_ylabel('Touches per 90', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Season', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)

# Progressive Carries
if 'carries_prgc' in man_utd_poss.columns and '90s' in man_utd_poss.columns:
    man_utd_poss['prgc_per_90'] = pd.to_numeric(man_utd_poss['carries_prgc'], errors='coerce') / pd.to_numeric(man_utd_poss['90s'], errors='coerce')
    axes[1, 1].plot(man_utd_poss['season_start_year'], man_utd_poss['prgc_per_90'],
                    marker='o', linewidth=3, markersize=10, color='#DA291C')
    axes[1, 1].set_title('Progressive Carries per 90', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Per 90', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Season', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Manchester United: Tactical Dashboard (2017-2025)',
             fontsize=18, fontweight='bold', y=0.995)
plt.tight_layout()
plt.savefig(output_dir / '16_man_utd_tactical_dashboard.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '16_man_utd_tactical_dashboard.png'}")

# ============================================================================
# 5. PRINT SUMMARY STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("TACTICAL SUMMARY")
print("=" * 80)

print("\nAvailable defensive stats columns:")
print([col for col in df_defensive.columns if 'tkl' in col or 'int' in col][:10])

print("\nAvailable possession stats columns:")
print([col for col in df_possession.columns if 'poss' in col or 'carries' in col or 'touches' in col][:10])

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nKey Insights to Look For:")
print("1. Has Man Utd's defensive intensity (tackles/interceptions) changed?")
print("2. How does Man Utd's possession compare to dominant teams?")
print("3. Are they progressing the ball effectively (progressive carries)?")
print("4. Combined with goal-scoring data, what's the tactical profile?")
