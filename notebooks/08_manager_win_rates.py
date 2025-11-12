"""
Manchester United Manager Performance Analysis
===============================================

Comprehensive manager comparison including:
- Win rates
- Points per season
- League positions
- Tenure periods (exact dates)
- Performance metrics

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

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (18, 10)

print("=" * 80)
print("MANCHESTER UNITED MANAGER PERFORMANCE ANALYSIS")
print("=" * 80)

# ============================================================================
# 1. HISTORICAL RESULTS DATA (Public Record)
# ============================================================================

print("\n[1/4] Loading historical results data...")

# Man Utd Premier League results by season (public historical data)
season_results = [
    # Ferguson Era
    {'season': '2000-01', 'wins': 24, 'draws': 8, 'losses': 6, 'points': 80, 'position': 1},
    {'season': '2001-02', 'wins': 24, 'draws': 5, 'losses': 9, 'points': 77, 'position': 3},
    {'season': '2002-03', 'wins': 25, 'draws': 8, 'losses': 5, 'points': 83, 'position': 1},
    {'season': '2003-04', 'wins': 23, 'draws': 6, 'losses': 9, 'points': 75, 'position': 3},
    {'season': '2004-05', 'wins': 22, 'draws': 11, 'losses': 5, 'points': 77, 'position': 3},
    {'season': '2005-06', 'wins': 25, 'draws': 8, 'losses': 5, 'points': 83, 'position': 2},
    {'season': '2006-07', 'wins': 28, 'draws': 5, 'losses': 5, 'points': 89, 'position': 1},
    {'season': '2007-08', 'wins': 27, 'draws': 6, 'losses': 5, 'points': 87, 'position': 1},
    {'season': '2008-09', 'wins': 28, 'draws': 6, 'losses': 4, 'points': 90, 'position': 1},
    {'season': '2009-10', 'wins': 27, 'draws': 4, 'losses': 7, 'points': 85, 'position': 2},
    {'season': '2010-11', 'wins': 23, 'draws': 11, 'losses': 4, 'points': 80, 'position': 1},
    {'season': '2011-12', 'wins': 28, 'draws': 5, 'losses': 5, 'points': 89, 'position': 2},
    {'season': '2012-13', 'wins': 28, 'draws': 5, 'losses': 5, 'points': 89, 'position': 1},

    # Post-Ferguson
    {'season': '2013-14', 'wins': 19, 'draws': 7, 'losses': 12, 'points': 64, 'position': 7},  # Moyes
    {'season': '2014-15', 'wins': 20, 'draws': 10, 'losses': 8, 'points': 70, 'position': 4},  # Van Gaal
    {'season': '2015-16', 'wins': 19, 'draws': 9, 'losses': 10, 'points': 66, 'position': 5},  # Van Gaal
    {'season': '2016-17', 'wins': 18, 'draws': 15, 'losses': 5, 'points': 69, 'position': 6},  # Mourinho
    {'season': '2017-18', 'wins': 25, 'draws': 6, 'losses': 7, 'points': 81, 'position': 2},  # Mourinho
    {'season': '2018-19', 'wins': 19, 'draws': 9, 'losses': 10, 'points': 66, 'position': 6},  # Mourinho/Solskjaer
    {'season': '2019-20', 'wins': 18, 'draws': 12, 'losses': 8, 'points': 66, 'position': 3},  # Solskjaer
    {'season': '2020-21', 'wins': 21, 'draws': 11, 'losses': 6, 'points': 74, 'position': 2},  # Solskjaer
    {'season': '2021-22', 'wins': 16, 'draws': 10, 'losses': 12, 'points': 58, 'position': 6},  # Solskjaer/Rangnick
    {'season': '2022-23', 'wins': 23, 'draws': 6, 'losses': 9, 'points': 75, 'position': 3},  # Ten Hag
    {'season': '2023-24', 'wins': 18, 'draws': 6, 'losses': 14, 'points': 60, 'position': 8},  # Ten Hag
    {'season': '2024-25', 'wins': 10, 'draws': 8, 'losses': 20, 'points': 38, 'position': 14}, # Amorim (estimated current)
]

df_results = pd.DataFrame(season_results)
df_results['matches'] = 38
df_results['win_rate'] = (df_results['wins'] / df_results['matches'] * 100).round(2)
df_results['points_per_game'] = (df_results['points'] / df_results['matches']).round(3)
df_results['season_start_year'] = df_results['season'].str[:4].astype(int)

print(f"Loaded {len(df_results)} seasons of results data")

# ============================================================================
# 2. MANAGER ASSIGNMENTS WITH EXACT TENURE
# ============================================================================

print("\n[2/4] Mapping managers to seasons...")

manager_info = {
    'Ferguson': {
        'years': '1986-2013',
        'tenure': '27 years',
        'seasons': [f'{y}-{str(y+1)[-2:]}' for y in range(2000, 2014)]
    },
    'Moyes': {
        'years': 'Jul 2013 - Apr 2014',
        'tenure': '10 months',
        'seasons': ['2013-14']
    },
    'Van Gaal': {
        'years': 'Jul 2014 - May 2016',
        'tenure': '2 years',
        'seasons': ['2014-15', '2015-16']
    },
    'Mourinho': {
        'years': 'Jul 2016 - Dec 2018',
        'tenure': '2.5 years',
        'seasons': ['2016-17', '2017-18', '2018-19']  # Partially 2018-19
    },
    'Solskjær': {
        'years': 'Dec 2018 - Nov 2021',
        'tenure': '3 years',
        'seasons': ['2018-19', '2019-20', '2020-21', '2021-22']  # Partially 2018-19 & 2021-22
    },
    'Rangnick': {
        'years': 'Dec 2021 - May 2022',
        'tenure': '6 months (interim)',
        'seasons': ['2021-22']  # Partially
    },
    'Ten Hag': {
        'years': 'Jul 2022 - Nov 2024',
        'tenure': '2.4 years',
        'seasons': ['2022-23', '2023-24', '2024-25']  # Partially 2024-25
    },
    'Amorim': {
        'years': 'Nov 2024 - Present',
        'tenure': '2 months',
        'seasons': ['2024-25']  # Partially
    }
}

# Simplified mapping for full season analysis
manager_map = {
    2000: 'Ferguson', 2001: 'Ferguson', 2002: 'Ferguson', 2003: 'Ferguson',
    2004: 'Ferguson', 2005: 'Ferguson', 2006: 'Ferguson', 2007: 'Ferguson',
    2008: 'Ferguson', 2009: 'Ferguson', 2010: 'Ferguson', 2011: 'Ferguson',
    2012: 'Ferguson', 2013: 'Ferguson',
    2014: 'Moyes',
    2015: 'Van Gaal', 2016: 'Van Gaal',
    2017: 'Mourinho', 2018: 'Mourinho', 2019: 'Mourinho',
    2020: 'Solskjær', 2021: 'Solskjær', 2022: 'Solskjær/Rangnick',
    2023: 'Ten Hag', 2024: 'Ten Hag/Amorim', 2025: 'Amorim'
}

df_results['manager'] = df_results['season_start_year'].map(manager_map)

print("Manager assignments complete")

# ============================================================================
# 3. CALCULATE MANAGER STATISTICS
# ============================================================================

print("\n[3/4] Calculating manager performance metrics...")

# For cleaner aggregation, let's assign primary manager per season
primary_manager = {
    2000: 'Ferguson', 2001: 'Ferguson', 2002: 'Ferguson', 2003: 'Ferguson',
    2004: 'Ferguson', 2005: 'Ferguson', 2006: 'Ferguson', 2007: 'Ferguson',
    2008: 'Ferguson', 2009: 'Ferguson', 2010: 'Ferguson', 2011: 'Ferguson',
    2012: 'Ferguson', 2013: 'Ferguson',
    2014: 'Moyes',
    2015: 'Van Gaal', 2016: 'Van Gaal',
    2017: 'Mourinho', 2018: 'Mourinho', 2019: 'Solskjær',
    2020: 'Solskjær', 2021: 'Solskjær', 2022: 'Rangnick',
    2023: 'Ten Hag', 2024: 'Ten Hag', 2025: 'Amorim'
}

df_results['primary_manager'] = df_results['season_start_year'].map(primary_manager)

# Aggregate by primary manager
manager_stats = df_results.groupby('primary_manager').agg({
    'wins': 'sum',
    'draws': 'sum',
    'losses': 'sum',
    'points': 'sum',
    'matches': 'sum',
    'win_rate': 'mean',
    'points_per_game': 'mean',
    'position': 'mean',
    'season': 'count'
}).rename(columns={'season': 'seasons'})

manager_stats['total_win_rate'] = (manager_stats['wins'] / manager_stats['matches'] * 100).round(2)
manager_stats['avg_position'] = manager_stats['position'].round(1)

# Add tenure info
manager_stats['tenure'] = manager_stats.index.map(lambda x: manager_info[x]['tenure'])
manager_stats['years'] = manager_stats.index.map(lambda x: manager_info[x]['years'])

# Sort by win rate
manager_stats = manager_stats.sort_values('total_win_rate', ascending=False)

print("Manager statistics calculated")

# ============================================================================
# 4. CREATE VISUALIZATIONS
# ============================================================================

print("\n[4/4] Creating visualizations...")

output_dir = Path("data/processed/plots")
output_dir.mkdir(parents=True, exist_ok=True)

# ---- PLOT 1: Win Rate Comparison ----
fig, ax = plt.subplots(figsize=(16, 9))

managers = manager_stats.index
win_rates = manager_stats['total_win_rate']

colors = ['#228B22' if m == 'Ferguson' else '#DA291C' for m in managers]
bars = ax.barh(range(len(managers)), win_rates, color=colors, alpha=0.85, edgecolor='black', linewidth=2)

# Add Ferguson benchmark line
ferguson_wr = manager_stats.loc['Ferguson', 'total_win_rate']
ax.axvline(x=ferguson_wr, color='#228B22', linestyle='--', linewidth=2.5, alpha=0.7,
           label=f'Ferguson Standard ({ferguson_wr}%)')

# Add 50% line (break-even)
ax.axvline(x=50, color='gray', linestyle=':', linewidth=2, alpha=0.5, label='50% (Break-even)')

ax.set_yticks(range(len(managers)))
ax.set_yticklabels([f"{m}\n({manager_stats.loc[m, 'years']})" for m in managers], fontsize=11)
ax.set_xlabel('Win Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('Manchester United: Manager Win Rates (Post-Ferguson vs Ferguson)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='lower right')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()

# Add value labels
for i, (manager, value) in enumerate(zip(managers, win_rates)):
    ax.text(value + 1, i, f'{value}%', va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '20_manager_win_rates.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '20_manager_win_rates.png'}")

# ---- PLOT 2: Points Per Season Timeline ----
fig, ax = plt.subplots(figsize=(20, 10))

# Color code by manager
manager_colors = {
    'Ferguson': '#228B22',
    'Moyes': '#8B4513',
    'Van Gaal': '#FF8C00',
    'Mourinho': '#4169E1',
    'Solskjær': '#DC143C',
    'Rangnick': '#DC143C',
    'Ten Hag': '#9932CC',
    'Amorim': '#FFD700'
}

for manager in df_results['primary_manager'].unique():
    manager_data = df_results[df_results['primary_manager'] == manager]
    ax.plot(manager_data['season_start_year'], manager_data['points'],
            marker='o', linewidth=3, markersize=10,
            color=manager_colors.get(manager, '#999999'),
            label=manager)

# Add Ferguson retirement line
ax.axvline(x=2013, color='black', linestyle='--', linewidth=2.5, alpha=0.6,
           label='Ferguson Retirement')

# Add benchmark lines
ax.axhline(y=90, color='gold', linestyle=':', linewidth=2, alpha=0.5, label='Title Contention (~90 pts)')
ax.axhline(y=75, color='silver', linestyle=':', linewidth=2, alpha=0.5, label='Top 4 (~75 pts)')

ax.set_xlabel('Season', fontsize=14, fontweight='bold')
ax.set_ylabel('Points', fontsize=14, fontweight='bold')
ax.set_title('Manchester United: Points Per Season by Manager (2000-2025)',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='best', ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xlim(1999.5, 2025.5)

plt.tight_layout()
plt.savefig(output_dir / '21_manager_points_timeline.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '21_manager_points_timeline.png'}")

# ---- PLOT 3: League Position by Manager ----
fig, ax = plt.subplots(figsize=(16, 9))

managers_post = [m for m in manager_stats.index if m != 'Ferguson']
positions = [manager_stats.loc[m, 'avg_position'] for m in managers_post]
colors_post = [manager_colors.get(m, '#999999') for m in managers_post]

bars = ax.barh(range(len(managers_post)), positions, color=colors_post, alpha=0.85,
               edgecolor='black', linewidth=2)

# Add Ferguson average line
ferguson_pos = manager_stats.loc['Ferguson', 'avg_position']
ax.axvline(x=ferguson_pos, color='#228B22', linestyle='--', linewidth=2.5, alpha=0.7,
           label=f'Ferguson Average (#{ferguson_pos:.1f})')

ax.set_yticks(range(len(managers_post)))
ax.set_yticklabels([f"{m}\n({manager_stats.loc[m, 'seasons']} seasons)" for m in managers_post], fontsize=11)
ax.set_xlabel('Average League Position', fontsize=14, fontweight='bold')
ax.set_title('Post-Ferguson Managers: Average League Position',
             fontsize=18, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='lower right')
ax.grid(True, alpha=0.3, axis='x')
ax.invert_yaxis()
ax.invert_xaxis()  # Lower position number = better

# Add value labels
for i, (manager, value) in enumerate(zip(managers_post, positions)):
    ax.text(value - 0.3, i, f'#{value:.1f}', va='center', ha='right', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig(output_dir / '22_manager_league_positions.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '22_manager_league_positions.png'}")

# ---- PLOT 4: Comprehensive Manager Dashboard ----
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

# Win Rate
ax1 = fig.add_subplot(gs[0, 0])
bars = ax1.barh(range(len(manager_stats)), manager_stats['total_win_rate'],
                color=['#228B22' if m == 'Ferguson' else '#DA291C' for m in manager_stats.index],
                alpha=0.85)
ax1.set_yticks(range(len(manager_stats)))
ax1.set_yticklabels(manager_stats.index, fontsize=11)
ax1.set_xlabel('Win Rate (%)', fontsize=12, fontweight='bold')
ax1.set_title('Win Rate', fontsize=14, fontweight='bold')
ax1.invert_yaxis()
ax1.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(manager_stats['total_win_rate']):
    ax1.text(v + 1, i, f'{v}%', va='center', fontsize=10, fontweight='bold')

# Points Per Game
ax2 = fig.add_subplot(gs[0, 1])
bars = ax2.barh(range(len(manager_stats)), manager_stats['points_per_game'],
                color=['#228B22' if m == 'Ferguson' else '#DA291C' for m in manager_stats.index],
                alpha=0.85)
ax2.set_yticks(range(len(manager_stats)))
ax2.set_yticklabels(manager_stats.index, fontsize=11)
ax2.set_xlabel('Points Per Game', fontsize=12, fontweight='bold')
ax2.set_title('Points Per Game', fontsize=14, fontweight='bold')
ax2.invert_yaxis()
ax2.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(manager_stats['points_per_game']):
    ax2.text(v + 0.03, i, f'{v:.2f}', va='center', fontsize=10, fontweight='bold')

# Average Position
ax3 = fig.add_subplot(gs[1, 0])
bars = ax3.barh(range(len(manager_stats)), manager_stats['avg_position'],
                color=['#228B22' if m == 'Ferguson' else '#DA291C' for m in manager_stats.index],
                alpha=0.85)
ax3.set_yticks(range(len(manager_stats)))
ax3.set_yticklabels(manager_stats.index, fontsize=11)
ax3.set_xlabel('Average Position', fontsize=12, fontweight='bold')
ax3.set_title('Average League Position', fontsize=14, fontweight='bold')
ax3.invert_yaxis()
ax3.invert_xaxis()
ax3.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(manager_stats['avg_position']):
    ax3.text(v - 0.3, i, f'#{v:.1f}', va='center', ha='right', fontsize=10, fontweight='bold')

# Total Points
ax4 = fig.add_subplot(gs[1, 1])
bars = ax4.barh(range(len(manager_stats)), manager_stats['points'],
                color=['#228B22' if m == 'Ferguson' else '#DA291C' for m in manager_stats.index],
                alpha=0.85)
ax4.set_yticks(range(len(manager_stats)))
ax4.set_yticklabels(manager_stats.index, fontsize=11)
ax4.set_xlabel('Total Points', fontsize=12, fontweight='bold')
ax4.set_title('Total Points Accumulated', fontsize=14, fontweight='bold')
ax4.invert_yaxis()
ax4.grid(True, alpha=0.3, axis='x')
for i, v in enumerate(manager_stats['points']):
    ax4.text(v + 5, i, f'{int(v)}', va='center', fontsize=10, fontweight='bold')

plt.suptitle('Manchester United: Comprehensive Manager Performance Dashboard',
             fontsize=20, fontweight='bold', y=0.98)
plt.savefig(output_dir / '23_manager_dashboard.png', dpi=300, bbox_inches='tight')
print(f"Saved: {output_dir / '23_manager_dashboard.png'}")

# ============================================================================
# 5. PRINT DETAILED STATISTICS
# ============================================================================

print("\n" + "=" * 80)
print("MANAGER PERFORMANCE SUMMARY")
print("=" * 80)

for manager in manager_stats.index:
    print(f"\n{manager} ({manager_stats.loc[manager, 'years']})")
    print(f"  Tenure: {manager_stats.loc[manager, 'tenure']}")
    print(f"  Seasons: {int(manager_stats.loc[manager, 'seasons'])}")
    print(f"  Win Rate: {manager_stats.loc[manager, 'total_win_rate']}%")
    print(f"  Points Per Game: {manager_stats.loc[manager, 'points_per_game']:.3f}")
    print(f"  Average Position: #{manager_stats.loc[manager, 'avg_position']:.1f}")
    print(f"  Total Points: {int(manager_stats.loc[manager, 'points'])}")
    print(f"  Record: {int(manager_stats.loc[manager, 'wins'])}W-"
          f"{int(manager_stats.loc[manager, 'draws'])}D-"
          f"{int(manager_stats.loc[manager, 'losses'])}L")

print("\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print(f"• Ferguson Win Rate: {manager_stats.loc['Ferguson', 'total_win_rate']}%")
print(f"• Best Post-Ferguson: {manager_stats.index[1]} ({manager_stats.iloc[1]['total_win_rate']}%)")
print(f"• Worst Post-Ferguson: {manager_stats.index[-1]} ({manager_stats.iloc[-1]['total_win_rate']}%)")
print(f"• Ferguson avg position: #{manager_stats.loc['Ferguson', 'avg_position']:.1f}")
print(f"• Post-Ferguson avg position: #{manager_stats.iloc[1:]['avg_position'].mean():.1f}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
