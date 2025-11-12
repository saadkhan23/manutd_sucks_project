"""
Comprehensive analysis of attacking prowess, defensive stability, and transfer efficiency.
Exports JSON for interactive React visualizations.
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

# ============================================================================
# LOAD DATA
# ============================================================================

output_dir = "/Users/saadkhan/Documents/manutd_sucks_project/data/processed"

print("Loading processed data...")
all_teams = pd.read_csv(f"{output_dir}/all_teams_standard_stats.csv")

print(f"Data shape: {all_teams.shape}")
print(f"Squads: {len(all_teams['squad'].unique())}")
print(f"Seasons: {sorted(all_teams['season'].unique())}")

# ============================================================================
# ATTACKING ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("ATTACKING EDGE ANALYSIS")
print("="*80)

# Get latest season for all teams (2024-25 or latest available)
latest_season = all_teams['season'].max()
print(f"\nAnalyzing latest season: {latest_season}")

latest_data = all_teams[all_teams['season'] == latest_season].copy()

# Prepare attacking data for React
attacking_data = {
    'attacking_edge': [],
    'performance_vs_expected': [],
    'man_utd_timeline': [],
    'rivals_comparison': []
}

# 1. ATTACKING EDGE: Progressive Carries vs Goals
print("\nAttacking Edge (Progressive Carries/90 vs Goals/90):")
for _, row in latest_data.iterrows():
    if pd.notna(row['progression_prgc']) and pd.notna(row['per_90_minutes_gls']):
        attacking_data['attacking_edge'].append({
            'squad': row['squad'],
            'season': str(row['season']),
            'progressive_carries': float(row['progression_prgc']),
            'goals_per_90': float(row['per_90_minutes_gls']),
            'is_man_utd': row['squad'] == 'Manchester Utd'
        })
        if row['squad'] == 'Manchester Utd':
            print(f"  {row['squad']}: {row['progression_prgc']:.1f} prog carries, {row['per_90_minutes_gls']:.2f} goals/90")

# 2. PERFORMANCE VS EXPECTED: xG/90 vs Actual Goals/90
print("\nPerformance vs Expected (xG/90 vs Actual Goals/90):")
for _, row in latest_data.iterrows():
    if pd.notna(row['per_90_minutes_xg']) and pd.notna(row['per_90_minutes_gls']):
        over_under = float(row['per_90_minutes_gls'] - row['per_90_minutes_xg'])
        attacking_data['performance_vs_expected'].append({
            'squad': row['squad'],
            'season': str(row['season']),
            'xg_per_90': float(row['per_90_minutes_xg']),
            'goals_per_90': float(row['per_90_minutes_gls']),
            'over_under_performance': over_under,
            'is_man_utd': row['squad'] == 'Manchester Utd'
        })
        if row['squad'] == 'Manchester Utd':
            perf = "overperforming" if over_under > 0 else "underperforming"
            print(f"  {row['squad']}: {row['per_90_minutes_xg']:.2f} xG/90, {row['per_90_minutes_gls']:.2f} actual ({perf} by {abs(over_under):.2f})")

# 3. MAN UTD TIMELINE: Goals and xG over time
print("\nMan Utd Timeline (2000-2025):")
man_utd_data = all_teams[all_teams['squad'] == 'Manchester Utd'].sort_values('season')
for _, row in man_utd_data.iterrows():
    if pd.notna(row['per_90_minutes_gls']):
        attacking_data['man_utd_timeline'].append({
            'season': str(row['season']),
            'goals_per_90': float(row['per_90_minutes_gls']),
            'xg_per_90': float(row['per_90_minutes_xg']) if pd.notna(row['per_90_minutes_xg']) else None,
            'xag_per_90': float(row['per_90_minutes_xag']) if pd.notna(row['per_90_minutes_xag']) else None
        })

print(f"  Extracted {len(attacking_data['man_utd_timeline'])} seasons")

# 4. RIVALS COMPARISON: Top 6 teams across all seasons
top_teams = ['Manchester Utd', 'Manchester City', 'Liverpool', 'Arsenal', 'Chelsea', 'Tottenham']
print("\nRivals Comparison (all seasons):")
for team in top_teams:
    team_data = all_teams[all_teams['squad'] == team].sort_values('season')
    if len(team_data) > 0:
        for _, row in team_data.iterrows():
            if pd.notna(row['per_90_minutes_gls']):
                attacking_data['rivals_comparison'].append({
                    'squad': row['squad'],
                    'season': str(row['season']),
                    'goals_per_90': float(row['per_90_minutes_gls']),
                    'xg_per_90': float(row['per_90_minutes_xg']) if pd.notna(row['per_90_minutes_xg']) else None
                })
        print(f"  {team}: {len(team_data)} seasons")

# Save attacking analysis
output_file = f"{output_dir}/attacking_analysis.json"
with open(output_file, 'w') as f:
    json.dump(attacking_data, f, indent=2)
print(f"\n✅ Attacking analysis saved to: {output_file}")
print(f"   - Attacking edge: {len(attacking_data['attacking_edge'])} teams")
print(f"   - Performance vs Expected: {len(attacking_data['performance_vs_expected'])} teams")
print(f"   - Man Utd timeline: {len(attacking_data['man_utd_timeline'])} seasons")
print(f"   - Rivals comparison: {len(attacking_data['rivals_comparison'])} data points")
