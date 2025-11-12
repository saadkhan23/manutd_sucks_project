"""
Manchester United vs Top Rivals Comparison
===========================================

This script compares Man Utd's performance against their traditional rivals
and the current top teams in the Premier League.

Rivals analyzed:
- Manchester City (current dominance)
- Liverpool (traditional rival + recent success)
- Arsenal (traditional rival)
- Chelsea (similar spending, variable success)

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
plt.rcParams['figure.figsize'] = (16, 10)

print("=" * 80)
print("MANCHESTER UNITED VS TOP RIVALS COMPARISON")
print("=" * 80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

print("\n[1/4] Loading all teams data...")

df_all = pd.read_csv('data/processed/all_teams_standard_stats.csv')

# Define the teams to compare
rivals = ['Manchester Utd', 'Manchester City', 'Liverpool', 'Arsenal', 'Chelsea']

# Filter for these teams
df_rivals = df_all[df_all['squad'].isin(rivals)].copy()

# Standardize team names for display
df_rivals['squad'] = df_rivals['squad'].replace({
    'Manchester Utd': 'Man Utd',
    'Manchester City': 'Man City'
})

print(f"Loaded data for {df_rivals['squad'].nunique()} teams")
print(f"Total rows: {len(df_rivals)}")
print(f"Season range: {df_rivals['season'].min()} to {df_rivals['season'].max()}")

# Recalculate key metrics
if 'goals_per_game' not in df_rivals.columns:
    df_rivals['goals_per_game'] = df_rivals['performance_gls'] / df_rivals['playing_time_mp']
    df_rivals['assists_per_game'] = df_rivals['performance_ast'] / df_rivals['playing_time_mp']
    df_rivals['goal_contribution_per_game'] = df_rivals['performance_g_a'] / df_rivals['playing_time_mp']

# ============================================================================
# 2. CREATE COMPARISON VISUALIZATIONS
# ============================================================================

print("\n[2/4] Creating comparison visualizations...")

output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# Define team colors
team_colors = {
    'Man Utd': '#DA291C',       # Red
    'Man City': '#6CABDD',       # Sky Blue
    'Liverpool': '#C8102E',      # Liverpool Red
    'Arsenal': '#EF0107',        # Arsenal Red
    'Chelsea': '#034694'         # Chelsea Blue
}

# ---- PLOT 1: Goals Per Game Timeline ----
fig, ax = plt.subplots(figsize=(18, 10))

for team in rivals:
    team_display = team.replace('Manchester ', 'Man ')
    team_data = df_rivals[df_rivals['squad'] == team_display].sort_values('season_start_year')

    ax.plot(team_data['season_start_year'], team_data['goals_per_game'],
            marker='o', linewidth=2.5, markersize=7,
            color=team_colors.get(team_display, '#999999'),
            label=team_display, alpha=0.85)

# Add Ferguson retirement line
ax.axvline(x=2013, color='black', linestyle='--', linewidth=2, alpha=0.5,
           label='Ferguson Retirement')

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=14, fontweight='bold')
ax.set_title('Top Teams: Goals Per Game Comparison (2000-2025)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '09_rivals_goals_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '09_rivals_goals_comparison.png'}")

# ---- PLOT 2: Post-Ferguson Era Comparison (2014-2025) ----
post_ferguson = df_rivals[df_rivals['season_start_year'] >= 2014].copy()

fig, ax = plt.subplots(figsize=(18, 10))

for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea']:
    team_data = post_ferguson[post_ferguson['squad'] == team].sort_values('season_start_year')

    ax.plot(team_data['season_start_year'], team_data['goals_per_game'],
            marker='o', linewidth=3, markersize=9,
            color=team_colors.get(team, '#999999'),
            label=team, alpha=0.9)

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=14, fontweight='bold')
ax.set_title('Post-Ferguson Era: Top Teams Goals Per Game (2014-2025)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=13, loc='best')
ax.grid(True, alpha=0.3)
ax.set_xlim(2013.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '10_rivals_post_ferguson.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '10_rivals_post_ferguson.png'}")

# ---- PLOT 3: Average Performance by Period ----
# Compare Ferguson Era vs Post-Ferguson for all teams

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

# Ferguson Era
ferguson_era = df_rivals[df_rivals['season_start_year'] <= 2013]
ferguson_avg = ferguson_era.groupby('squad')['goals_per_game'].mean().sort_values(ascending=False)

axes[0].bar(range(len(ferguson_avg)), ferguson_avg.values,
            color=[team_colors.get(team, '#999999') for team in ferguson_avg.index],
            alpha=0.8)
axes[0].set_xticks(range(len(ferguson_avg)))
axes[0].set_xticklabels(ferguson_avg.index, rotation=45, ha='right', fontsize=11)
axes[0].set_ylabel('Average Goals Per Game', fontsize=13, fontweight='bold')
axes[0].set_title('Ferguson Era (2000-2013)', fontsize=15, fontweight='bold')
axes[0].grid(True, alpha=0.3, axis='y')

# Add value labels
for i, v in enumerate(ferguson_avg.values):
    axes[0].text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Post-Ferguson Era
post_ferguson_avg = post_ferguson.groupby('squad')['goals_per_game'].mean().sort_values(ascending=False)

axes[1].bar(range(len(post_ferguson_avg)), post_ferguson_avg.values,
            color=[team_colors.get(team, '#999999') for team in post_ferguson_avg.index],
            alpha=0.8)
axes[1].set_xticks(range(len(post_ferguson_avg)))
axes[1].set_xticklabels(post_ferguson_avg.index, rotation=45, ha='right', fontsize=11)
axes[1].set_ylabel('Average Goals Per Game', fontsize=13, fontweight='bold')
axes[1].set_title('Post-Ferguson Era (2014-2025)', fontsize=15, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

# Add value labels
for i, v in enumerate(post_ferguson_avg.values):
    axes[1].text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.suptitle('Top Teams: Goals Per Game by Era', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(output_dir / '11_rivals_era_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '11_rivals_era_comparison.png'}")

# ---- PLOT 4: Change from Ferguson Era to Post-Ferguson ----
# Calculate percentage change for each team

fig, ax = plt.subplots(figsize=(14, 8))

changes = []
for team in ['Man Utd', 'Man City', 'Liverpool', 'Arsenal', 'Chelsea']:
    ferguson_avg_team = ferguson_era[ferguson_era['squad'] == team]['goals_per_game'].mean()
    post_ferguson_avg_team = post_ferguson[post_ferguson['squad'] == team]['goals_per_game'].mean()

    if not pd.isna(ferguson_avg_team) and not pd.isna(post_ferguson_avg_team):
        pct_change = ((post_ferguson_avg_team / ferguson_avg_team) - 1) * 100
        changes.append({'team': team, 'change': pct_change})

changes_df = pd.DataFrame(changes).sort_values('change')

colors = [team_colors.get(team, '#999999') for team in changes_df['team']]
bars = ax.barh(range(len(changes_df)), changes_df['change'], color=colors, alpha=0.8)

# Add zero line
ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.5)

ax.set_yticks(range(len(changes_df)))
ax.set_yticklabels(changes_df['team'], fontsize=12)
ax.set_xlabel('% Change in Goals Per Game', fontsize=13, fontweight='bold')
ax.set_title('Goals Per Game: % Change from Ferguson Era to Post-Ferguson',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (idx, row) in enumerate(changes_df.iterrows()):
    value = row['change']
    ax.text(value + (2 if value > 0 else -2), i, f'{value:+.1f}%',
            ha='left' if value > 0 else 'right', va='center',
            fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '12_rivals_percent_change.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '12_rivals_percent_change.png'}")

# ============================================================================
# 3. STATISTICAL SUMMARY
# ============================================================================

print("\n[3/4] Computing statistical summary...")

print("\n" + "=" * 80)
print("FERGUSON ERA (2000-2013) - Average Goals Per Game")
print("=" * 80)
for team in ferguson_avg.index:
    print(f"{team:15s}: {ferguson_avg[team]:.3f}")

print("\n" + "=" * 80)
print("POST-FERGUSON ERA (2014-2025) - Average Goals Per Game")
print("=" * 80)
for team in post_ferguson_avg.index:
    print(f"{team:15s}: {post_ferguson_avg[team]:.3f}")

print("\n" + "=" * 80)
print("PERCENTAGE CHANGE (Ferguson Era → Post-Ferguson)")
print("=" * 80)
for _, row in changes_df.iterrows():
    print(f"{row['team']:15s}: {row['change']:+.1f}%")

# ============================================================================
# 4. RECENT FORM (Last 5 seasons)
# ============================================================================

print("\n[4/4] Analyzing recent form (last 5 seasons)...")

recent = df_rivals[df_rivals['season_start_year'] >= 2020].copy()
recent_avg = recent.groupby('squad')['goals_per_game'].mean().sort_values(ascending=False)

print("\n" + "=" * 80)
print("RECENT FORM (2020-2025) - Average Goals Per Game")
print("=" * 80)
for team in recent_avg.index:
    print(f"{team:15s}: {recent_avg[team]:.3f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nKey Insights:")
print("1. Check how Man Utd ranks against rivals in both eras")
print("2. Identify which teams improved vs declined post-Ferguson")
print("3. Examine if Man Utd's decline is unique or part of a broader trend")
print("4. Assess competitive gap between Man Utd and current top teams")
