"""
Enhanced Manchester United Visualizations with Manager Annotations
====================================================================

This script creates improved visualizations showing manager impact on performance.

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
plt.rcParams['figure.figsize'] = (16, 9)

print("=" * 80)
print("ENHANCED MANCHESTER UNITED VISUALIZATIONS WITH MANAGER ANNOTATIONS")
print("=" * 80)

# ============================================================================
# 1. LOAD PROCESSED DATA
# ============================================================================

print("\n[1/3] Loading processed data...")

man_utd = pd.read_csv('data/processed/man_utd_standard_stats.csv')
print(f"Loaded {len(man_utd)} seasons of Man Utd data")

# ============================================================================
# 2. ADD MANAGER INFORMATION
# ============================================================================

print("\n[2/3] Adding manager information...")

# Manager mapping (season start year -> manager name)
manager_map = {
    # Ferguson Era
    2000: 'Ferguson', 2001: 'Ferguson', 2002: 'Ferguson', 2003: 'Ferguson',
    2004: 'Ferguson', 2005: 'Ferguson', 2006: 'Ferguson', 2007: 'Ferguson',
    2008: 'Ferguson', 2009: 'Ferguson', 2010: 'Ferguson', 2011: 'Ferguson',
    2012: 'Ferguson', 2013: 'Ferguson',

    # Post-Ferguson
    2014: 'Moyes',
    2015: 'Van Gaal', 2016: 'Van Gaal',
    2017: 'Mourinho', 2018: 'Mourinho', 2019: 'Mourinho',
    2020: 'Solskjær', 2021: 'Solskjær', 2022: 'Solskjær/Rangnick',
    2023: 'Ten Hag', 2024: 'Ten Hag', 2025: 'Amorim'
}

man_utd['manager'] = man_utd['season_start_year'].map(manager_map)

# Define manager colors for visualization
manager_colors = {
    'Ferguson': '#228B22',  # Forest Green
    'Moyes': '#8B4513',     # Brown
    'Van Gaal': '#FF8C00',  # Dark Orange
    'Mourinho': '#4169E1',  # Royal Blue
    'Solskjær': '#DC143C',  # Crimson
    'Solskjær/Rangnick': '#DC143C',
    'Ten Hag': '#9932CC',   # Purple
    'Amorim': '#FFD700'     # Gold
}

# Manager tenure periods (for shaded regions)
manager_periods = [
    {'name': 'Moyes', 'start': 2014, 'end': 2014.5},
    {'name': 'Van Gaal', 'start': 2015, 'end': 2016.5},
    {'name': 'Mourinho', 'start': 2017, 'end': 2019.5},
    {'name': 'Solskjær', 'start': 2020, 'end': 2022.5},
    {'name': 'Ten Hag', 'start': 2023, 'end': 2024.5},
    {'name': 'Amorim', 'start': 2025, 'end': 2025.5},
]

print(f"Managers mapped: {man_utd['manager'].nunique()} unique managers")

# ============================================================================
# 3. CREATE ENHANCED VISUALIZATIONS
# ============================================================================

print("\n[3/3] Creating enhanced visualizations...")

output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# ---- PLOT 1: Goals Per Game with Manager Annotations ----
fig, ax = plt.subplots(figsize=(18, 10))

# Plot the line
ax.plot(man_utd['season_start_year'], man_utd['goals_per_game'],
        marker='o', linewidth=3, markersize=10, color='#DA291C',
        label='Goals per Game', zorder=5)

# Add Ferguson retirement line
ax.axvline(x=2013, color='black', linestyle='--', linewidth=3, alpha=0.7,
           label='Ferguson Retirement', zorder=3)

# Add overall average line
overall_mean = man_utd['goals_per_game'].mean()
ax.axhline(y=overall_mean, color='gray', linestyle=':', linewidth=2, alpha=0.5,
           label=f'Overall Average ({overall_mean:.2f})', zorder=2)

# Shade manager periods (post-Ferguson only)
for period in manager_periods:
    color = manager_colors.get(period['name'], '#CCCCCC')
    ax.axvspan(period['start'], period['end'], alpha=0.15, color=color, zorder=1)

    # Add manager name at the top
    mid_point = (period['start'] + period['end']) / 2
    ax.text(mid_point, ax.get_ylim()[1] * 0.98, period['name'],
            ha='center', va='top', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=color, alpha=0.3))

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=14, fontweight='bold')
ax.set_title('Manchester United: Goals Per Game by Manager (2000-2025)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '05_man_utd_goals_with_managers.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '05_man_utd_goals_with_managers.png'}")

# ---- PLOT 2: Goal Contribution with Manager Annotations ----
fig, ax = plt.subplots(figsize=(18, 10))

# Plot goals and assists
ax.plot(man_utd['season_start_year'], man_utd['goals_per_game'],
        marker='o', linewidth=2.5, markersize=8, color='#DA291C',
        label='Goals/Game', zorder=5)
ax.plot(man_utd['season_start_year'], man_utd['assists_per_game'],
        marker='s', linewidth=2.5, markersize=8, color='#FDB913',
        label='Assists/Game', zorder=5)
ax.plot(man_utd['season_start_year'], man_utd['goal_contribution_per_game'],
        marker='D', linewidth=2.5, markersize=8, color='#000000',
        label='Total Contribution/Game', zorder=5)

# Add Ferguson retirement line
ax.axvline(x=2013, color='gray', linestyle='--', linewidth=3, alpha=0.7,
           label='Ferguson Retirement', zorder=3)

# Shade manager periods (post-Ferguson only)
for period in manager_periods:
    color = manager_colors.get(period['name'], '#CCCCCC')
    ax.axvspan(period['start'], period['end'], alpha=0.12, color=color, zorder=1)

    # Add manager name
    mid_point = (period['start'] + period['end']) / 2
    ax.text(mid_point, ax.get_ylim()[1] * 0.98, period['name'],
            ha='center', va='top', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor=color, alpha=0.3))

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Per Game Average', fontsize=14, fontweight='bold')
ax.set_title('Manchester United: Attacking Contribution by Manager (2000-2025)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '06_man_utd_attacking_with_managers.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '06_man_utd_attacking_with_managers.png'}")

# ---- PLOT 3: Manager Performance Comparison ----
# Calculate average performance by manager (post-Ferguson only)
post_ferguson = man_utd[man_utd['season_start_year'] >= 2014].copy()

manager_stats = post_ferguson.groupby('manager').agg({
    'goals_per_game': 'mean',
    'assists_per_game': 'mean',
    'goal_contribution_per_game': 'mean',
    'season': 'count'  # Number of seasons
}).round(3)

# Sort by goals per game
manager_stats = manager_stats.sort_values('goals_per_game', ascending=False)

fig, ax = plt.subplots(figsize=(14, 8))

x = np.arange(len(manager_stats))
width = 0.25

bars1 = ax.bar(x - width, manager_stats['goals_per_game'], width,
               label='Goals/Game', color='#DA291C', alpha=0.8)
bars2 = ax.bar(x, manager_stats['assists_per_game'], width,
               label='Assists/Game', color='#FDB913', alpha=0.8)
bars3 = ax.bar(x + width, manager_stats['goal_contribution_per_game'], width,
               label='Total Contribution/Game', color='#000000', alpha=0.8)

# Add Ferguson benchmark line
ferguson_goals = man_utd[man_utd['season_start_year'] <= 2013]['goals_per_game'].mean()
ax.axhline(y=ferguson_goals, color='#228B22', linestyle='--', linewidth=2.5,
           label=f'Ferguson Average ({ferguson_goals:.2f})', alpha=0.7)

# Add value labels on bars
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

# Add season count below manager names
labels_with_count = [f"{manager}\n({int(manager_stats.loc[manager, 'season'])} seasons)"
                     for manager in manager_stats.index]

ax.set_xlabel('Manager', fontsize=14, fontweight='bold')
ax.set_ylabel('Per Game Average', fontsize=14, fontweight='bold')
ax.set_title('Post-Ferguson Manager Performance Comparison',
             fontsize=18, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(labels_with_count, fontsize=11)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '07_manager_comparison.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '07_manager_comparison.png'}")

# ---- PLOT 4: Timeline with Manager Colors ----
fig, ax = plt.subplots(figsize=(18, 10))

# Plot each manager's data with their specific color
for manager in man_utd['manager'].unique():
    manager_data = man_utd[man_utd['manager'] == manager]
    color = manager_colors.get(manager, '#999999')

    if manager == 'Ferguson':
        ax.plot(manager_data['season_start_year'], manager_data['goals_per_game'],
                marker='o', linewidth=3, markersize=10, color=color,
                label=manager, zorder=5, alpha=0.9)
    else:
        ax.plot(manager_data['season_start_year'], manager_data['goals_per_game'],
                marker='o', linewidth=3, markersize=10, color=color,
                label=manager, zorder=5)

# Add Ferguson retirement line
ax.axvline(x=2013, color='black', linestyle='--', linewidth=3, alpha=0.5, zorder=3)

# Add overall average
overall_mean = man_utd['goals_per_game'].mean()
ax.axhline(y=overall_mean, color='gray', linestyle=':', linewidth=2, alpha=0.5,
           label=f'Overall Average ({overall_mean:.2f})', zorder=2)

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Goals Per Game', fontsize=14, fontweight='bold')
ax.set_title('Manchester United: Goals Per Game by Manager (Color-Coded)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=11, loc='upper right', ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '08_man_utd_goals_color_coded.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '08_man_utd_goals_color_coded.png'}")

# ============================================================================
# 4. PRINT MANAGER STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("MANAGER PERFORMANCE SUMMARY (Post-Ferguson)")
print("=" * 80)

for manager in manager_stats.index:
    print(f"\n{manager} ({int(manager_stats.loc[manager, 'season'])} seasons):")
    print(f"  Goals/Game: {manager_stats.loc[manager, 'goals_per_game']:.3f}")
    print(f"  Assists/Game: {manager_stats.loc[manager, 'assists_per_game']:.3f}")
    print(f"  Total Contribution/Game: {manager_stats.loc[manager, 'goal_contribution_per_game']:.3f}")

print(f"\nFerguson Era Baseline:")
print(f"  Goals/Game: {ferguson_goals:.3f}")

print("\n" + "=" * 80)
print("VISUALIZATION COMPLETE!")
print("=" * 80)
