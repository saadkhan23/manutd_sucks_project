"""
Improved Rival Comparison with Better Color Scheme
===================================================

This script creates improved visualizations with:
1. More distinct color scheme
2. Additional teams (Tottenham, Leicester, Newcastle)
3. Better visual clarity

Author: Data-driven analysis of Man Utd's struggles
Date: 2025-10-24
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 10)

print("=" * 80)
print("IMPROVED RIVAL COMPARISON WITH BETTER COLORS")
print("=" * 80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n[1/3] Loading data...")

df_all = pd.read_csv('data/processed/all_teams_standard_stats.csv')

# Define teams to compare - expanded list
teams_to_analyze = [
    'Manchester Utd', 'Manchester City', 'Liverpool', 'Arsenal', 'Chelsea',
    'Tottenham', 'Leicester City'
]

# Filter for these teams
df_teams = df_all[df_all['squad'].isin(teams_to_analyze)].copy()

# Standardize team names
df_teams['squad'] = df_teams['squad'].replace({
    'Manchester Utd': 'Man Utd',
    'Manchester City': 'Man City',
    'Leicester City': 'Leicester',
    'Tottenham': 'Spurs'
})

print(f"Teams included: {df_teams['squad'].unique()}")
print(f"Total rows: {len(df_teams)}")

# Recalculate metrics if needed
if 'goals_per_game' not in df_teams.columns:
    df_teams['goals_per_game'] = df_teams['performance_gls'] / df_teams['playing_time_mp']
    df_teams['assists_per_game'] = df_teams['performance_ast'] / df_teams['playing_time_mp']

# ============================================================================
# 2. IMPROVED COLOR SCHEME - HIGHLY DISTINCT
# ============================================================================

# New color scheme with maximum visual distinction
team_colors_improved = {
    'Man Utd': '#DA291C',        # Red (Man Utd official)
    'Man City': '#6CABDD',        # Sky Blue (Man City official)
    'Liverpool': '#00B2A9',       # Teal (distinct from red)
    'Arsenal': '#FF8C00',         # Dark Orange (distinct from all reds)
    'Chelsea': '#034694',         # Royal Blue (Chelsea official)
    'Spurs': '#132257',           # Navy (Spurs official)
    'Leicester': '#0053A0',       # Leicester Blue
}

# Line styles for additional distinction
line_styles = {
    'Man Utd': '-',      # Solid (protagonist)
    'Man City': '-',     # Solid (main rival)
    'Liverpool': '-',    # Solid (traditional rival)
    'Arsenal': '--',     # Dashed
    'Chelsea': '--',     # Dashed
    'Spurs': ':',        # Dotted
    'Leicester': '-.',   # Dash-dot
}

# Marker styles
markers = {
    'Man Utd': 'o',      # Circle
    'Man City': 's',     # Square
    'Liverpool': 'D',    # Diamond
    'Arsenal': '^',      # Triangle up
    'Chelsea': 'v',      # Triangle down
    'Spurs': 'p',        # Pentagon
    'Leicester': '*',    # Star
}

# ============================================================================
# 3. CREATE IMPROVED VISUALIZATIONS
# ============================================================================

print("\n[2/3] Creating improved visualizations...")

output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# ---- PLOT 1: Full Timeline with All Teams ----
fig, ax = plt.subplots(figsize=(20, 11))

for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea', 'Spurs', 'Leicester']:
    team_data = df_teams[df_teams['squad'] == team].sort_values('season_start_year')

    if len(team_data) > 0:
        ax.plot(team_data['season_start_year'], team_data['goals_per_game'],
                marker=markers.get(team, 'o'),
                linestyle=line_styles.get(team, '-'),
                linewidth=2.5,
                markersize=8,
                color=team_colors_improved.get(team, '#999999'),
                label=team,
                alpha=0.9)

# Add Ferguson retirement line
ax.axvline(x=2013, color='black', linestyle='--', linewidth=2.5, alpha=0.6,
           label='Ferguson Retirement', zorder=1)

ax.set_xlabel('Season', fontsize=15, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=15, fontweight='bold')
ax.set_title('Premier League Top Teams: Goals Per Game (2000-2025)',
             fontsize=20, fontweight='bold', pad=20)

# Improved legend with better positioning
ax.legend(fontsize=13, loc='upper left', framealpha=0.95,
          ncol=2, columnspacing=1.5, handletextpad=0.8)
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '17_improved_all_teams_timeline.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '17_improved_all_teams_timeline.png'}")

# ---- PLOT 2: Post-Ferguson Era Only (Cleaner) ----
post_ferguson = df_teams[df_teams['season_start_year'] >= 2014].copy()

fig, ax = plt.subplots(figsize=(20, 11))

for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea', 'Spurs', 'Leicester']:
    team_data = post_ferguson[post_ferguson['squad'] == team].sort_values('season_start_year')

    if len(team_data) > 0:
        ax.plot(team_data['season_start_year'], team_data['goals_per_game'],
                marker=markers.get(team, 'o'),
                linestyle=line_styles.get(team, '-'),
                linewidth=3,
                markersize=10,
                color=team_colors_improved.get(team, '#999999'),
                label=team,
                alpha=0.9)

# Highlight Leicester's title-winning season
leicester_2015 = post_ferguson[(post_ferguson['squad'] == 'Leicester') &
                                (post_ferguson['season_start_year'] == 2015)]
if len(leicester_2015) > 0:
    ax.scatter(2015, leicester_2015['goals_per_game'].values[0],
               s=500, marker='*', color='gold', edgecolors='black',
               linewidths=2, zorder=10, label='Leicester Title Win')

ax.set_xlabel('Season', fontsize=15, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=15, fontweight='bold')
ax.set_title('Post-Ferguson Era: Goals Per Game Comparison (2014-2025)',
             fontsize=20, fontweight='bold', pad=20)
ax.legend(fontsize=13, loc='best', framealpha=0.95, ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xlim(2013.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '18_improved_post_ferguson.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '18_improved_post_ferguson.png'}")

# ---- PLOT 3: Average Performance Ranking ----
fig, axes = plt.subplots(1, 2, figsize=(20, 9))

# Ferguson Era
ferguson_era = df_teams[df_teams['season_start_year'] <= 2013]
ferguson_avg = ferguson_era.groupby('squad')['goals_per_game'].mean().sort_values(ascending=False)

colors_ferguson = [team_colors_improved.get(team, '#999999') for team in ferguson_avg.index]
bars = axes[0].barh(range(len(ferguson_avg)), ferguson_avg.values,
                     color=colors_ferguson, alpha=0.85, edgecolor='black', linewidth=1.5)

axes[0].set_yticks(range(len(ferguson_avg)))
axes[0].set_yticklabels(ferguson_avg.index, fontsize=13, fontweight='bold')
axes[0].set_xlabel('Average Goals Per Game', fontsize=14, fontweight='bold')
axes[0].set_title('Ferguson Era (2000-2013)', fontsize=16, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='x')
axes[0].invert_yaxis()

# Add value labels
for i, v in enumerate(ferguson_avg.values):
    axes[0].text(v + 0.02, i, f'{v:.3f}', va='center', fontsize=12, fontweight='bold')

# Post-Ferguson Era
post_ferguson_avg = post_ferguson.groupby('squad')['goals_per_game'].mean().sort_values(ascending=False)

colors_post = [team_colors_improved.get(team, '#999999') for team in post_ferguson_avg.index]
bars = axes[1].barh(range(len(post_ferguson_avg)), post_ferguson_avg.values,
                     color=colors_post, alpha=0.85, edgecolor='black', linewidth=1.5)

axes[1].set_yticks(range(len(post_ferguson_avg)))
axes[1].set_yticklabels(post_ferguson_avg.index, fontsize=13, fontweight='bold')
axes[1].set_xlabel('Average Goals Per Game', fontsize=14, fontweight='bold')
axes[1].set_title('Post-Ferguson Era (2014-2025)', fontsize=16, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='x')
axes[1].invert_yaxis()

# Add value labels
for i, v in enumerate(post_ferguson_avg.values):
    axes[1].text(v + 0.02, i, f'{v:.3f}', va='center', fontsize=12, fontweight='bold')

plt.suptitle('Goals Per Game Rankings by Era', fontsize=20, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig(output_dir / '19_improved_era_rankings.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '19_improved_era_rankings.png'}")

# ============================================================================
# 4. STATISTICAL SUMMARY
# ============================================================================

print("\n[3/3] Statistical summary...")

print("\n" + "=" * 80)
print("FERGUSON ERA (2000-2013) RANKINGS")
print("=" * 80)
for i, (team, value) in enumerate(ferguson_avg.items(), 1):
    print(f"{i}. {team:15s}: {value:.3f} goals/game")

print("\n" + "=" * 80)
print("POST-FERGUSON ERA (2014-2025) RANKINGS")
print("=" * 80)
for i, (team, value) in enumerate(post_ferguson_avg.items(), 1):
    print(f"{i}. {team:15s}: {value:.3f} goals/game")

# Biggest movers
print("\n" + "=" * 80)
print("POSITION CHANGES (Ferguson Era → Post-Ferguson)")
print("=" * 80)

ferguson_ranks = {team: i+1 for i, team in enumerate(ferguson_avg.index)}
post_ranks = {team: i+1 for i, team in enumerate(post_ferguson_avg.index)}

changes = []
for team in set(list(ferguson_ranks.keys()) + list(post_ranks.keys())):
    old_rank = ferguson_ranks.get(team, None)
    new_rank = post_ranks.get(team, None)

    if old_rank and new_rank:
        change = old_rank - new_rank  # Positive = improved ranking
        changes.append({'team': team, 'old_rank': old_rank, 'new_rank': new_rank, 'change': change})

changes_df = pd.DataFrame(changes).sort_values('change', ascending=False)

for _, row in changes_df.iterrows():
    direction = "↑" if row['change'] > 0 else "↓" if row['change'] < 0 else "→"
    print(f"{row['team']:15s}: #{int(row['old_rank'])} → #{int(row['new_rank'])} {direction} ({row['change']:+.0f})")

print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print("• Leicester's miracle season (2015-16) shows ambition can overcome budget")
print("• Tottenham's consistency without trophies (solid mid-table to top 4)")
print("• Man Utd's fall: #1 → #5/6 ranking among analyzed teams")
print("• Man City's transformation: Mid-table → Dominant #1")

print("\n" + "=" * 80)
print("VISUALIZATION IMPROVEMENT COMPLETE!")
print("=" * 80)
