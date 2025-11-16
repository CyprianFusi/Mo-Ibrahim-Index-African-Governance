"""
Ibrahim Index of African Governance (IIAG) Analysis
Comprehensive analysis and visualization of African governance data (2014-2023)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for professional visualizations
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

# Load data
data_path = Path('data/csv-files')
composite_scores = pd.read_csv(data_path / '2024 IIAG_Composite Scores.csv', encoding='utf-8-sig')
ranks = pd.read_csv(data_path / '2024 IIAG_Ranks.csv', encoding='utf-8-sig')

# Clean data - replace '.' with NaN
composite_scores = composite_scores.replace('.', np.nan)
for col in composite_scores.columns[3:]:  # Skip Country_ISO, Country, Year
    composite_scores[col] = pd.to_numeric(composite_scores[col], errors='coerce')

print("="*80)
print("IBRAHIM INDEX OF AFRICAN GOVERNANCE (IIAG) - EXECUTIVE SUMMARY")
print("="*80)
print(f"\nDataset Coverage:")
print(f"  • Countries: {composite_scores['Country'].nunique()}")
print(f"  • Years: {composite_scores['Year'].min()} - {composite_scores['Year'].max()}")
print(f"  • Total Records: {len(composite_scores):,}")

# Define categories
main_categories = [
    'SECURITY & RULE OF LAW',
    'PARTICIPATION, RIGHTS & INCLUSION',
    'FOUNDATIONS FOR ECONOMIC OPPORTUNITY',
    'HUMAN DEVELOPMENT'
]

subcategories = {
    'SECURITY & RULE OF LAW': ['SECURITY & SAFETY', 'RULE OF LAW & JUSTICE', 'ACCOUNTABILITY & TRANSPARENCY', 'ANTI-CORRUPTION'],
    'PARTICIPATION, RIGHTS & INCLUSION': ['PARTICIPATION', 'RIGHTS', 'INCLUSION & EQUALITY', "WOMEN'S EQUALITY"],
    'FOUNDATIONS FOR ECONOMIC OPPORTUNITY': ['PUBLIC ADMINISTRATION', 'BUSINESS & LABOUR ENVIRONMENT', 'INFRASTRUCTURE', 'RURAL ECONOMY'],
    'HUMAN DEVELOPMENT': ['HEALTH', 'EDUCATION', 'SOCIAL PROTECTION & WELFARE', 'SUSTAINABLE ENVIRONMENT']
}

# Regional groupings
regional_groups = {
    'North Africa': ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Tunisia'],
    'West Africa': ['Benin', 'Burkina Faso', 'Cape Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana', 'Guinea',
                    'Guinea-Bissau', 'Liberia', 'Mali', 'Mauritania', 'Niger', 'Nigeria', 'Senegal',
                    'Sierra Leone', 'Togo'],
    'East Africa': ['Burundi', 'Comoros', 'Djibouti', 'Eritrea', 'Ethiopia', 'Kenya', 'Madagascar',
                    'Mauritius', 'Rwanda', 'Seychelles', 'Somalia', 'South Sudan', 'Sudan', 'Tanzania', 'Uganda'],
    'Central Africa': ['Cameroon', 'Central African Republic', 'Chad', 'Congo', 'DR Congo', 'Equatorial Guinea',
                       'Gabon', 'São Tomé and Príncipe'],
    'Southern Africa': ['Angola', 'Botswana', 'Eswatini', 'Lesotho', 'Malawi', 'Mozambique', 'Namibia',
                        'South Africa', 'Zambia', 'Zimbabwe']
}

# Add regional classification
def get_region(country):
    for region, countries in regional_groups.items():
        if country in countries:
            return region
    return 'Other'

composite_scores['Region'] = composite_scores['Country'].apply(get_region)

# ============================================================================
# 1. OVERALL GOVERNANCE LANDSCAPE
# ============================================================================

latest_year = composite_scores['Year'].max()
latest_data = composite_scores[composite_scores['Year'] == latest_year].copy()

print(f"\n{'='*80}")
print(f"KEY INSIGHTS - {latest_year}")
print(f"{'='*80}")

# Top and Bottom Performers
top_10 = latest_data.nlargest(10, 'OVERALL GOVERNANCE')[['Country', 'OVERALL GOVERNANCE']]
bottom_10 = latest_data.nsmallest(10, 'OVERALL GOVERNANCE')[['Country', 'OVERALL GOVERNANCE']]

print(f"\nTOP 10 PERFORMERS ({latest_year}):")
print("-" * 40)
for idx, row in top_10.iterrows():
    print(f"  {row['Country']:<25} {row['OVERALL GOVERNANCE']:.1f}")

print(f"\nBOTTOM 10 PERFORMERS ({latest_year}):")
print("-" * 40)
for idx, row in bottom_10.iterrows():
    print(f"  {row['Country']:<25} {row['OVERALL GOVERNANCE']:.1f}")

# Continental averages
print(f"\nCONTINENTAL STATISTICS ({latest_year}):")
print("-" * 40)
print(f"  Mean Overall Governance:      {latest_data['OVERALL GOVERNANCE'].mean():.1f}")
print(f"  Median Overall Governance:    {latest_data['OVERALL GOVERNANCE'].median():.1f}")
print(f"  Standard Deviation:           {latest_data['OVERALL GOVERNANCE'].std():.1f}")
print(f"  Highest Score:                {latest_data['OVERALL GOVERNANCE'].max():.1f}")
print(f"  Lowest Score:                 {latest_data['OVERALL GOVERNANCE'].min():.1f}")

# ============================================================================
# 2. TEMPORAL TRENDS ANALYSIS
# ============================================================================

print(f"\n{'='*80}")
print("TEMPORAL TRENDS (2014-2023)")
print(f"{'='*80}")

# Calculate year-over-year changes for all countries
def calculate_change(df, country, start_year, end_year):
    start_score = df[(df['Country'] == country) & (df['Year'] == start_year)]['OVERALL GOVERNANCE'].values
    end_score = df[(df['Country'] == country) & (df['Year'] == end_year)]['OVERALL GOVERNANCE'].values

    if len(start_score) > 0 and len(end_score) > 0:
        return end_score[0] - start_score[0]
    return np.nan

countries_list = composite_scores['Country'].unique()
changes = []
for country in countries_list:
    change = calculate_change(composite_scores, country, 2014, 2023)
    if not np.isnan(change):
        changes.append({'Country': country, 'Change': change})

changes_df = pd.DataFrame(changes).sort_values('Change', ascending=False)

print(f"\nTOP 10 IMPROVERS (2014-2023):")
print("-" * 40)
for idx, row in changes_df.head(10).iterrows():
    print(f"  {row['Country']:<25} +{row['Change']:.1f} points")

print(f"\nTOP 10 DECLINERS (2014-2023):")
print("-" * 40)
for idx, row in changes_df.tail(10).iterrows():
    print(f"  {row['Country']:<25} {row['Change']:.1f} points")

# ============================================================================
# 3. CATEGORY ANALYSIS
# ============================================================================

print(f"\n{'='*80}")
print(f"CATEGORY PERFORMANCE ({latest_year})")
print(f"{'='*80}")

category_stats = latest_data[main_categories].describe().loc[['mean', 'std', 'min', 'max']].T
print(f"\n{category_stats.round(1)}")

# Regional Analysis
print(f"\n{'='*80}")
print(f"REGIONAL ANALYSIS ({latest_year})")
print(f"{'='*80}")

regional_stats = latest_data.groupby('Region')['OVERALL GOVERNANCE'].agg(['mean', 'std', 'count']).round(1)
regional_stats = regional_stats.sort_values('mean', ascending=False)
print(f"\n{regional_stats}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print(f"\n{'='*80}")
print("GENERATING VISUALIZATIONS...")
print(f"{'='*80}")

# Create output directory
output_dir = Path('visualizations')
output_dir.mkdir(exist_ok=True)

# 1. Overall Governance Distribution (Latest Year)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
ax1.hist(latest_data['OVERALL GOVERNANCE'].dropna(), bins=20, edgecolor='black', alpha=0.7, color='#3498db')
ax1.axvline(latest_data['OVERALL GOVERNANCE'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {latest_data["OVERALL GOVERNANCE"].mean():.1f}')
ax1.axvline(latest_data['OVERALL GOVERNANCE'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {latest_data["OVERALL GOVERNANCE"].median():.1f}')
ax1.set_xlabel('Overall Governance Score')
ax1.set_ylabel('Number of Countries')
ax1.set_title(f'Distribution of Governance Scores ({latest_year})', fontweight='bold', fontsize=14)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Box plot by region
region_data = [latest_data[latest_data['Region'] == region]['OVERALL GOVERNANCE'].dropna()
               for region in regional_stats.index if region != 'Other']
ax2.boxplot(region_data, labels=[r for r in regional_stats.index if r != 'Other'], patch_artist=True)
ax2.set_ylabel('Overall Governance Score')
ax2.set_xlabel('Region')
ax2.set_title(f'Regional Governance Comparison ({latest_year})', fontweight='bold', fontsize=14)
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '01_governance_distribution.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 01_governance_distribution.png")
plt.close()

# 2. Top and Bottom 15 Countries
fig, ax = plt.subplots(figsize=(14, 10))

top_bottom = pd.concat([
    latest_data.nlargest(15, 'OVERALL GOVERNANCE'),
    latest_data.nsmallest(15, 'OVERALL GOVERNANCE')
]).sort_values('OVERALL GOVERNANCE')

colors = ['#e74c3c' if x < 50 else '#f39c12' if x < 60 else '#2ecc71' for x in top_bottom['OVERALL GOVERNANCE']]
bars = ax.barh(range(len(top_bottom)), top_bottom['OVERALL GOVERNANCE'], color=colors, edgecolor='black', linewidth=0.5)

ax.set_yticks(range(len(top_bottom)))
ax.set_yticklabels(top_bottom['Country'])
ax.set_xlabel('Overall Governance Score', fontweight='bold')
ax.set_title(f'Top and Bottom 15 Countries - Overall Governance ({latest_year})', fontweight='bold', fontsize=16, pad=20)
ax.grid(True, alpha=0.3, axis='x')
ax.axvline(50, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, top_bottom['OVERALL GOVERNANCE'])):
    ax.text(val + 1, i, f'{val:.1f}', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(output_dir / '02_top_bottom_countries.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 02_top_bottom_countries.png")
plt.close()

# 3. Temporal Trends - Continental Average
yearly_avg = composite_scores.groupby('Year')['OVERALL GOVERNANCE'].mean()
yearly_categories = composite_scores.groupby('Year')[main_categories].mean()

fig, ax = plt.subplots(figsize=(14, 8))

ax.plot(yearly_avg.index, yearly_avg.values, marker='o', linewidth=3, markersize=10, label='Overall Governance', color='#2c3e50')
for cat in main_categories:
    ax.plot(yearly_categories.index, yearly_categories[cat], marker='s', linewidth=2, markersize=6, label=cat, alpha=0.8)

ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Average Governance Score', fontweight='bold')
ax.set_title('Continental Governance Trends (2014-2023)', fontweight='bold', fontsize=16, pad=20)
ax.legend(loc='best', framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_ylim([40, 65])

plt.tight_layout()
plt.savefig(output_dir / '03_temporal_trends.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 03_temporal_trends.png")
plt.close()

# 4. Category Heatmap - Top 20 Countries
top20_data = latest_data.nlargest(20, 'OVERALL GOVERNANCE')
top20_countries = top20_data['Country'].values
heatmap_data = top20_data[['Country'] + main_categories].set_index('Country')
heatmap_data = heatmap_data.reindex(top20_countries)

fig, ax = plt.subplots(figsize=(12, 10))
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
            linewidths=0.5, cbar_kws={'label': 'Score'}, ax=ax, vmin=0, vmax=100)
ax.set_title(f'Category Performance - Top 20 Countries ({latest_year})', fontweight='bold', fontsize=14, pad=20)
ax.set_xlabel('')
ax.set_ylabel('Country', fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / '04_category_heatmap_top20.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 04_category_heatmap_top20.png")
plt.close()

# 5. Improvement vs Decline Analysis
fig, ax = plt.subplots(figsize=(14, 10))

colors_change = ['#27ae60' if x > 0 else '#e74c3c' for x in changes_df['Change']]
bars = ax.barh(range(len(changes_df)), changes_df['Change'], color=colors_change, edgecolor='black', linewidth=0.5)

ax.set_yticks(range(len(changes_df)))
ax.set_yticklabels(changes_df['Country'], fontsize=8)
ax.set_xlabel('Change in Overall Governance Score (2014-2023)', fontweight='bold')
ax.set_title('Governance Change: All Countries (2014-2023)', fontweight='bold', fontsize=16, pad=20)
ax.axvline(0, color='black', linewidth=2)
ax.grid(True, alpha=0.3, axis='x')

# Add value labels for top/bottom
for i in list(range(10)) + list(range(len(changes_df)-10, len(changes_df))):
    val = changes_df['Change'].iloc[i]
    ax.text(val + (0.5 if val > 0 else -0.5), i, f'{val:.1f}', va='center',
            ha='left' if val > 0 else 'right', fontweight='bold', fontsize=8)

plt.tight_layout()
plt.savefig(output_dir / '05_governance_change_all.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 05_governance_change_all.png")
plt.close()

# 6. Regional Performance Comparison
regional_means = latest_data.groupby('Region')[['OVERALL GOVERNANCE'] + main_categories].mean()
regional_means = regional_means[regional_means.index != 'Other'].sort_values('OVERALL GOVERNANCE', ascending=False)

fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(regional_means))
width = 0.15

colors_cat = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
for i, cat in enumerate(['OVERALL GOVERNANCE'] + main_categories):
    offset = width * (i - 2)
    ax.bar(x + offset, regional_means[cat], width, label=cat, color=colors_cat[i] if i < len(colors_cat) else None)

ax.set_xlabel('Region', fontweight='bold')
ax.set_ylabel('Average Score', fontweight='bold')
ax.set_title(f'Regional Performance Across Categories ({latest_year})', fontweight='bold', fontsize=16, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(regional_means.index, rotation=15, ha='right')
ax.legend(loc='best', framealpha=0.9, fontsize=9)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(output_dir / '06_regional_comparison.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 06_regional_comparison.png")
plt.close()

# 7. Scatter Plot - Category Correlation
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
axes = axes.flatten()

for idx, cat in enumerate(main_categories):
    ax = axes[idx]

    # Remove NaN values
    plot_data = latest_data[['OVERALL GOVERNANCE', cat]].dropna()

    ax.scatter(plot_data[cat], plot_data['OVERALL GOVERNANCE'], alpha=0.6, s=100, edgecolors='black', linewidth=0.5)

    # Add correlation line
    z = np.polyfit(plot_data[cat], plot_data['OVERALL GOVERNANCE'], 1)
    p = np.poly1d(z)
    ax.plot(plot_data[cat].sort_values(), p(plot_data[cat].sort_values()), "r--", linewidth=2, alpha=0.8)

    # Calculate correlation
    corr = plot_data[cat].corr(plot_data['OVERALL GOVERNANCE'])

    ax.set_xlabel(cat, fontweight='bold')
    ax.set_ylabel('Overall Governance Score', fontweight='bold')
    ax.set_title(f'{cat}\n(Correlation: {corr:.2f})', fontweight='bold', fontsize=11)
    ax.grid(True, alpha=0.3)

plt.suptitle(f'Category vs Overall Governance Correlation ({latest_year})', fontweight='bold', fontsize=16, y=1.00)
plt.tight_layout()
plt.savefig(output_dir / '07_category_correlation.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 07_category_correlation.png")
plt.close()

# 8. Time Series - Top 5 vs Bottom 5 Countries
top5 = latest_data.nlargest(5, 'OVERALL GOVERNANCE')['Country'].values
bottom5 = latest_data.nsmallest(5, 'OVERALL GOVERNANCE')['Country'].values

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# Top 5
for country in top5:
    country_data = composite_scores[composite_scores['Country'] == country]
    ax1.plot(country_data['Year'], country_data['OVERALL GOVERNANCE'], marker='o', linewidth=2, label=country, markersize=6)

ax1.set_xlabel('Year', fontweight='bold')
ax1.set_ylabel('Overall Governance Score', fontweight='bold')
ax1.set_title('Top 5 Performing Countries - Trends (2014-2023)', fontweight='bold', fontsize=14)
ax1.legend(loc='best', framealpha=0.9)
ax1.grid(True, alpha=0.3)

# Bottom 5
for country in bottom5:
    country_data = composite_scores[composite_scores['Country'] == country]
    ax2.plot(country_data['Year'], country_data['OVERALL GOVERNANCE'], marker='s', linewidth=2, label=country, markersize=6)

ax2.set_xlabel('Year', fontweight='bold')
ax2.set_ylabel('Overall Governance Score', fontweight='bold')
ax2.set_title('Bottom 5 Performing Countries - Trends (2014-2023)', fontweight='bold', fontsize=14)
ax2.legend(loc='best', framealpha=0.9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(output_dir / '08_top_bottom_trends.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 08_top_bottom_trends.png")
plt.close()

# 9. Subcategory Analysis - Radar Chart for Top 5
from math import pi

fig, axes = plt.subplots(2, 3, figsize=(18, 12), subplot_kw=dict(projection='polar'))
axes = axes.flatten()

# Get all subcategories
all_subcats = []
for cats in subcategories.values():
    all_subcats.extend(cats)

for idx, country in enumerate(top5):
    ax = axes[idx]

    country_data = latest_data[latest_data['Country'] == country]
    values = country_data[all_subcats].values.flatten().tolist()
    values = [v if not np.isnan(v) else 0 for v in values]

    # Number of variables
    categories_radar = all_subcats
    N = len(categories_radar)

    # Compute angle for each axis
    angles = [n / float(N) * 2 * pi for n in range(N)]
    values += values[:1]
    angles += angles[:1]

    # Plot
    ax.plot(angles, values, 'o-', linewidth=2, label=country)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories_radar, size=7)
    ax.set_ylim(0, 100)
    ax.set_title(country, fontweight='bold', size=12, pad=20)
    ax.grid(True)

# Hide the 6th subplot
axes[5].axis('off')

plt.suptitle(f'Subcategory Performance - Top 5 Countries ({latest_year})', fontweight='bold', fontsize=16, y=0.98)
plt.tight_layout()
plt.savefig(output_dir / '09_radar_top5.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 09_radar_top5.png")
plt.close()

# 10. Year-over-Year Change Heatmap
yoy_changes = []
for year in range(2015, 2024):
    for country in countries_list:
        prev_score = composite_scores[(composite_scores['Country'] == country) &
                                     (composite_scores['Year'] == year-1)]['OVERALL GOVERNANCE'].values
        curr_score = composite_scores[(composite_scores['Country'] == country) &
                                     (composite_scores['Year'] == year)]['OVERALL GOVERNANCE'].values

        if len(prev_score) > 0 and len(curr_score) > 0:
            change = curr_score[0] - prev_score[0]
            yoy_changes.append({'Country': country, 'Year': year, 'Change': change})

yoy_df = pd.DataFrame(yoy_changes)
yoy_pivot = yoy_df.pivot(index='Country', columns='Year', values='Change')

# Select top 25 countries by latest score for readability
top25_countries = latest_data.nlargest(25, 'OVERALL GOVERNANCE')['Country'].values
yoy_pivot_top25 = yoy_pivot.loc[yoy_pivot.index.isin(top25_countries)]

fig, ax = plt.subplots(figsize=(14, 12))
sns.heatmap(yoy_pivot_top25, annot=True, fmt='.1f', cmap='RdYlGn', center=0,
            linewidths=0.5, cbar_kws={'label': 'YoY Change'}, ax=ax, vmin=-5, vmax=5)
ax.set_title('Year-over-Year Governance Changes - Top 25 Countries', fontweight='bold', fontsize=14, pad=20)
ax.set_xlabel('Year', fontweight='bold')
ax.set_ylabel('Country', fontweight='bold')
plt.tight_layout()
plt.savefig(output_dir / '10_yoy_change_heatmap.png', dpi=300, bbox_inches='tight')
print("  [+] Saved: 10_yoy_change_heatmap.png")
plt.close()

print(f"\n{'='*80}")
print("ANALYSIS COMPLETE!")
print(f"{'='*80}")
print(f"\nAll visualizations saved to: {output_dir.absolute()}")
print("\nGenerated 10 comprehensive visualizations:")
print("  1. Governance Distribution & Regional Comparison")
print("  2. Top and Bottom 15 Countries")
print("  3. Continental Governance Trends (2014-2023)")
print("  4. Category Performance Heatmap (Top 20)")
print("  5. Governance Change - All Countries")
print("  6. Regional Performance Comparison")
print("  7. Category vs Overall Governance Correlation")
print("  8. Top 5 vs Bottom 5 Trends")
print("  9. Subcategory Radar Chart (Top 5)")
print("  10. Year-over-Year Change Heatmap")
