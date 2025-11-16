"""
Comprehensive Report Generator for Ibrahim Index of African Governance (IIAG)
Generates a detailed PDF report with cover page, analysis, and visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path
from datetime import datetime
import warnings
from math import pi
warnings.filterwarnings('ignore')

# Set professional styling
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Load data
print("Loading data...")
data_path = Path('data/csv-files')
composite_scores = pd.read_csv(data_path / '2024 IIAG_Composite Scores.csv', encoding='utf-8-sig')

# Clean data
composite_scores = composite_scores.replace('.', np.nan)
for col in composite_scores.columns[3:]:
    composite_scores[col] = pd.to_numeric(composite_scores[col], errors='coerce')

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

def get_region(country):
    for region, countries in regional_groups.items():
        if country in countries:
            return region
    return 'Other'

composite_scores['Region'] = composite_scores['Country'].apply(get_region)

latest_year = composite_scores['Year'].max()
earliest_year = composite_scores['Year'].min()
latest_data = composite_scores[composite_scores['Year'] == latest_year].copy()

# Calculate changes
def calculate_change(df, country, start_year, end_year):
    start_score = df[(df['Country'] == country) & (df['Year'] == start_year)]['OVERALL GOVERNANCE'].values
    end_score = df[(df['Country'] == country) & (df['Year'] == end_year)]['OVERALL GOVERNANCE'].values
    if len(start_score) > 0 and len(end_score) > 0:
        return end_score[0] - start_score[0]
    return np.nan

countries_list = composite_scores['Country'].unique()
changes = []
for country in countries_list:
    change = calculate_change(composite_scores, country, earliest_year, latest_year)
    if not np.isnan(change):
        changes.append({'Country': country, 'Change': change})

changes_df = pd.DataFrame(changes).sort_values('Change', ascending=False)

# Create PDF Report
print("Generating comprehensive report...")
pdf_filename = f'IIAG_Comprehensive_Report_{latest_year}.pdf'

with PdfPages(pdf_filename) as pdf:

    # ========== COVER PAGE ==========
    print("Creating cover page...")
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Title
    title_text = "IBRAHIM INDEX OF AFRICAN GOVERNANCE\n\nCOMPREHENSIVE ANALYTICAL REPORT"
    ax.text(0.5, 0.7, title_text, ha='center', va='center', fontsize=24, fontweight='bold',
            transform=ax.transAxes, wrap=True)

    # Subtitle
    subtitle = f"Analysis Period: {earliest_year}-{latest_year}"
    ax.text(0.5, 0.55, subtitle, ha='center', va='center', fontsize=16,
            transform=ax.transAxes, style='italic')

    # Key stats box
    stats_text = f"""
    Dataset Overview:
    • Countries Analyzed: {composite_scores['Country'].nunique()}
    • Years Covered: {earliest_year} - {latest_year}
    • Total Observations: {len(composite_scores):,}
    • Governance Categories: 4 Main Categories, 16 Subcategories
    """
    ax.text(0.5, 0.35, stats_text, ha='center', va='center', fontsize=12,
            transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))

    # Footer
    footer = f"Generated: {datetime.now().strftime('%B %d, %Y')}\nMo Ibrahim Foundation"
    ax.text(0.5, 0.1, footer, ha='center', va='center', fontsize=10,
            transform=ax.transAxes, style='italic', color='gray')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== EXECUTIVE SUMMARY PAGE ==========
    print("Creating executive summary...")
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    summary_text = f"""
EXECUTIVE SUMMARY

This report presents a comprehensive analysis of governance performance across African nations
from {earliest_year} to {latest_year}, based on the Ibrahim Index of African Governance (IIAG).

KEY FINDINGS:

1. OVERALL GOVERNANCE LANDSCAPE ({latest_year})
   • Continental Mean Score: {latest_data['OVERALL GOVERNANCE'].mean():.1f}/100
   • Median Score: {latest_data['OVERALL GOVERNANCE'].median():.1f}/100
   • Score Range: {latest_data['OVERALL GOVERNANCE'].min():.1f} to {latest_data['OVERALL GOVERNANCE'].max():.1f}
   • Standard Deviation: {latest_data['OVERALL GOVERNANCE'].std():.1f}

2. TOP PERFORMERS ({latest_year})
   The top five countries demonstrate exceptional governance:
   {chr(10).join(f"   • {row['Country']}: {row['OVERALL GOVERNANCE']:.1f}" for _, row in latest_data.nlargest(5, 'OVERALL GOVERNANCE').iterrows())}

3. SIGNIFICANT IMPROVERS ({earliest_year}-{latest_year})
   Countries showing the greatest governance improvements:
   {chr(10).join(f"   • {row['Country']}: +{row['Change']:.1f} points" for _, row in changes_df.head(5).iterrows())}

4. REGIONAL PATTERNS
   {chr(10).join(f"   • {region}: {score:.1f}" for region, score in latest_data.groupby('Region')['OVERALL GOVERNANCE'].mean().sort_values(ascending=False).head(5).items() if region != 'Other')}

5. CATEGORY PERFORMANCE
   Average scores across main governance categories:
   {chr(10).join(f"   • {cat}: {latest_data[cat].mean():.1f}" for cat in main_categories)}

METHODOLOGY:
The IIAG assesses governance across four main categories: Security & Rule of Law, Participation,
Rights & Inclusion, Foundations for Economic Opportunity, and Human Development. Each category
comprises multiple subcategories, creating a comprehensive governance assessment framework.

    """

    ax.text(0.05, 0.95, summary_text, ha='left', va='top', fontsize=9,
            transform=ax.transAxes, family='monospace')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 1: Distribution ==========
    print("Creating distribution visualization...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    ax1.hist(latest_data['OVERALL GOVERNANCE'].dropna(), bins=20, edgecolor='black', alpha=0.7, color='#3498db')
    ax1.axvline(latest_data['OVERALL GOVERNANCE'].mean(), color='red', linestyle='--', linewidth=2,
                label=f'Mean: {latest_data["OVERALL GOVERNANCE"].mean():.1f}')
    ax1.axvline(latest_data['OVERALL GOVERNANCE'].median(), color='green', linestyle='--', linewidth=2,
                label=f'Median: {latest_data["OVERALL GOVERNANCE"].median():.1f}')
    ax1.set_xlabel('Overall Governance Score', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Number of Countries', fontweight='bold', fontsize=11)
    ax1.set_title(f'Distribution of Governance Scores ({latest_year})', fontweight='bold', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    regional_stats = latest_data.groupby('Region')['OVERALL GOVERNANCE'].mean().sort_values(ascending=False)
    regional_stats = regional_stats[regional_stats.index != 'Other']
    region_data = [latest_data[latest_data['Region'] == region]['OVERALL GOVERNANCE'].dropna()
                   for region in regional_stats.index]

    bp = ax2.boxplot(region_data, labels=regional_stats.index, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('#3498db')
        patch.set_alpha(0.7)
    ax2.set_ylabel('Overall Governance Score', fontweight='bold', fontsize=11)
    ax2.set_xlabel('Region', fontweight='bold', fontsize=11)
    ax2.set_title(f'Regional Governance Comparison ({latest_year})', fontweight='bold', fontsize=13)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 2: Top/Bottom Countries ==========
    print("Creating top/bottom countries chart...")
    fig, ax = plt.subplots(figsize=(12, 10))

    top_bottom = pd.concat([
        latest_data.nlargest(15, 'OVERALL GOVERNANCE'),
        latest_data.nsmallest(15, 'OVERALL GOVERNANCE')
    ]).sort_values('OVERALL GOVERNANCE')

    colors = ['#e74c3c' if x < 50 else '#f39c12' if x < 60 else '#2ecc71'
              for x in top_bottom['OVERALL GOVERNANCE']]
    bars = ax.barh(range(len(top_bottom)), top_bottom['OVERALL GOVERNANCE'],
                   color=colors, edgecolor='black', linewidth=0.7)

    ax.set_yticks(range(len(top_bottom)))
    ax.set_yticklabels(top_bottom['Country'], fontsize=9)
    ax.set_xlabel('Overall Governance Score', fontweight='bold', fontsize=11)
    ax.set_title(f'Top and Bottom 15 Countries - Overall Governance ({latest_year})',
                 fontweight='bold', fontsize=14, pad=15)
    ax.grid(True, alpha=0.3, axis='x')
    ax.axvline(50, color='black', linestyle='--', linewidth=1, alpha=0.5)

    for i, (bar, val) in enumerate(zip(bars, top_bottom['OVERALL GOVERNANCE'])):
        ax.text(val + 1, i, f'{val:.1f}', va='center', fontweight='bold', fontsize=8)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 3: Temporal Trends ==========
    print("Creating temporal trends...")
    yearly_avg = composite_scores.groupby('Year')['OVERALL GOVERNANCE'].mean()
    yearly_categories = composite_scores.groupby('Year')[main_categories].mean()

    fig, ax = plt.subplots(figsize=(14, 7))

    ax.plot(yearly_avg.index, yearly_avg.values, marker='o', linewidth=3, markersize=10,
            label='Overall Governance', color='#2c3e50')

    colors_cat = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    for idx, cat in enumerate(main_categories):
        ax.plot(yearly_categories.index, yearly_categories[cat], marker='s', linewidth=2.5,
                markersize=7, label=cat, alpha=0.8, color=colors_cat[idx])

    ax.set_xlabel('Year', fontweight='bold', fontsize=11)
    ax.set_ylabel('Average Governance Score', fontweight='bold', fontsize=11)
    ax.set_title(f'Continental Governance Trends ({earliest_year}-{latest_year})',
                 fontweight='bold', fontsize=14, pad=15)
    ax.legend(loc='best', framealpha=0.95, fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 4: Category Heatmap ==========
    print("Creating category heatmap...")
    top20_data = latest_data.nlargest(20, 'OVERALL GOVERNANCE')
    heatmap_data = top20_data[['Country'] + main_categories].set_index('Country')

    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', center=50,
                linewidths=0.5, cbar_kws={'label': 'Score'}, ax=ax, vmin=30, vmax=90)
    ax.set_title(f'Category Performance - Top 20 Countries ({latest_year})',
                 fontweight='bold', fontsize=13, pad=15)
    ax.set_xlabel('')
    ax.set_ylabel('Country', fontweight='bold', fontsize=11)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 5: Governance Change ==========
    print("Creating governance change chart...")
    fig, ax = plt.subplots(figsize=(12, 11))

    colors_change = ['#27ae60' if x > 0 else '#e74c3c' for x in changes_df['Change']]
    bars = ax.barh(range(len(changes_df)), changes_df['Change'],
                   color=colors_change, edgecolor='black', linewidth=0.5)

    ax.set_yticks(range(len(changes_df)))
    ax.set_yticklabels(changes_df['Country'], fontsize=7)
    ax.set_xlabel(f'Change in Overall Governance Score ({earliest_year}-{latest_year})',
                  fontweight='bold', fontsize=11)
    ax.set_title(f'Governance Change: All Countries ({earliest_year}-{latest_year})',
                 fontweight='bold', fontsize=14, pad=15)
    ax.axvline(0, color='black', linewidth=2)
    ax.grid(True, alpha=0.3, axis='x')

    for i in list(range(10)) + list(range(len(changes_df)-10, len(changes_df))):
        val = changes_df['Change'].iloc[i]
        ax.text(val + (0.5 if val > 0 else -0.5), i, f'{val:.1f}', va='center',
                ha='left' if val > 0 else 'right', fontweight='bold', fontsize=7)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 6: Regional Comparison ==========
    print("Creating regional comparison...")
    regional_means = latest_data.groupby('Region')[['OVERALL GOVERNANCE'] + main_categories].mean()
    regional_means = regional_means[regional_means.index != 'Other'].sort_values('OVERALL GOVERNANCE', ascending=False)

    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(regional_means))
    width = 0.15

    colors_bar = ['#2c3e50', '#e74c3c', '#3498db', '#2ecc71', '#f39c12']
    for i, cat in enumerate(['OVERALL GOVERNANCE'] + main_categories):
        offset = width * (i - 2)
        ax.bar(x + offset, regional_means[cat], width, label=cat, color=colors_bar[i])

    ax.set_xlabel('Region', fontweight='bold', fontsize=11)
    ax.set_ylabel('Average Score', fontweight='bold', fontsize=11)
    ax.set_title(f'Regional Performance Across Categories ({latest_year})',
                 fontweight='bold', fontsize=14, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(regional_means.index, rotation=20, ha='right')
    ax.legend(loc='best', framealpha=0.95, fontsize=9)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 7: Category Correlation ==========
    print("Creating correlation scatter plots...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, cat in enumerate(main_categories):
        ax = axes[idx]
        plot_data = latest_data[['OVERALL GOVERNANCE', cat]].dropna()

        ax.scatter(plot_data[cat], plot_data['OVERALL GOVERNANCE'],
                   alpha=0.6, s=80, edgecolors='black', linewidth=0.5, color='#3498db')

        z = np.polyfit(plot_data[cat], plot_data['OVERALL GOVERNANCE'], 1)
        p = np.poly1d(z)
        ax.plot(plot_data[cat].sort_values(), p(plot_data[cat].sort_values()),
                "r--", linewidth=2.5, alpha=0.8)

        corr = plot_data[cat].corr(plot_data['OVERALL GOVERNANCE'])

        ax.set_xlabel(cat, fontweight='bold', fontsize=10)
        ax.set_ylabel('Overall Governance Score', fontweight='bold', fontsize=10)
        ax.set_title(f'{cat}\n(Correlation: {corr:.3f})', fontweight='bold', fontsize=11)
        ax.grid(True, alpha=0.3)

    plt.suptitle(f'Category vs Overall Governance Correlation ({latest_year})',
                 fontweight='bold', fontsize=14, y=0.995)
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== VISUALIZATION 8: Top/Bottom Trends ==========
    print("Creating top/bottom trends...")
    top5 = latest_data.nlargest(5, 'OVERALL GOVERNANCE')['Country'].values
    bottom5 = latest_data.nsmallest(5, 'OVERALL GOVERNANCE')['Country'].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for country in top5:
        country_data = composite_scores[composite_scores['Country'] == country]
        ax1.plot(country_data['Year'], country_data['OVERALL GOVERNANCE'],
                 marker='o', linewidth=2.5, label=country, markersize=7)

    ax1.set_xlabel('Year', fontweight='bold', fontsize=11)
    ax1.set_ylabel('Overall Governance Score', fontweight='bold', fontsize=11)
    ax1.set_title(f'Top 5 Performing Countries - Trends ({earliest_year}-{latest_year})',
                  fontweight='bold', fontsize=12)
    ax1.legend(loc='best', framealpha=0.95)
    ax1.grid(True, alpha=0.3)

    for country in bottom5:
        country_data = composite_scores[composite_scores['Country'] == country]
        ax2.plot(country_data['Year'], country_data['OVERALL GOVERNANCE'],
                 marker='s', linewidth=2.5, label=country, markersize=7)

    ax2.set_xlabel('Year', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Overall Governance Score', fontweight='bold', fontsize=11)
    ax2.set_title(f'Bottom 5 Performing Countries - Trends ({earliest_year}-{latest_year})',
                  fontweight='bold', fontsize=12)
    ax2.legend(loc='best', framealpha=0.95)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== DETAILED ANALYSIS PAGE ==========
    print("Creating detailed analysis page...")
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    # Calculate additional statistics
    improvers = changes_df[changes_df['Change'] > 0]
    decliners = changes_df[changes_df['Change'] < 0]

    regional_changes = []
    for region in regional_groups.keys():
        region_countries = [c for c in countries_list if get_region(c) == region]
        region_change = changes_df[changes_df['Country'].isin(region_countries)]['Change'].mean()
        if not np.isnan(region_change):
            regional_changes.append((region, region_change))
    regional_changes.sort(key=lambda x: x[1], reverse=True)

    analysis_text = f"""
DETAILED ANALYSIS AND INSIGHTS

1. TEMPORAL DYNAMICS ({earliest_year}-{latest_year})

   Continental Trend:
   • Overall governance score changed from {composite_scores[composite_scores['Year']==earliest_year]['OVERALL GOVERNANCE'].mean():.1f} ({earliest_year}) to {latest_data['OVERALL GOVERNANCE'].mean():.1f} ({latest_year})
   • Net change: {latest_data['OVERALL GOVERNANCE'].mean() - composite_scores[composite_scores['Year']==earliest_year]['OVERALL GOVERNANCE'].mean():.2f} points
   • Countries improving: {len(improvers)} ({len(improvers)/len(changes_df)*100:.1f}%)
   • Countries declining: {len(decliners)} ({len(decliners)/len(changes_df)*100:.1f}%)

2. CATEGORY-SPECIFIC INSIGHTS ({latest_year})

   Strongest Category (Continental Average):
   • {max([(cat, latest_data[cat].mean()) for cat in main_categories], key=lambda x: x[1])[0]}: {max([latest_data[cat].mean() for cat in main_categories]):.1f}

   Weakest Category (Continental Average):
   • {min([(cat, latest_data[cat].mean()) for cat in main_categories], key=lambda x: x[1])[0]}: {min([latest_data[cat].mean() for cat in main_categories]):.1f}

   Category Variability (Standard Deviation):
   {chr(10).join(f"   • {cat}: {latest_data[cat].std():.1f}" for cat in main_categories)}

3. REGIONAL PERFORMANCE DYNAMICS

   Regional Rankings by Average Change ({earliest_year}-{latest_year}):
   {chr(10).join(f"   {i+1}. {region}: {change:+.2f} points" for i, (region, change) in enumerate(regional_changes[:5]))}

   Regional Governance Spread ({latest_year}):
   • Highest regional variance: {max([(r, latest_data[latest_data['Region']==r]['OVERALL GOVERNANCE'].std()) for r in regional_groups.keys()], key=lambda x: x[1])[0]}
   • Most homogeneous region: {min([(r, latest_data[latest_data['Region']==r]['OVERALL GOVERNANCE'].std()) for r in regional_groups.keys() if len(latest_data[latest_data['Region']==r]) > 3], key=lambda x: x[1])[0]}

4. NOTABLE PATTERNS AND OBSERVATIONS

   • The correlation between 'Security & Rule of Law' and 'Overall Governance' is
     {latest_data[['SECURITY & RULE OF LAW', 'OVERALL GOVERNANCE']].corr().iloc[0,1]:.3f}, indicating {
     'strong' if abs(latest_data[['SECURITY & RULE OF LAW', 'OVERALL GOVERNANCE']].corr().iloc[0,1]) > 0.8 else 'moderate'}
     relationship

   • {len(latest_data[latest_data['OVERALL GOVERNANCE'] >= 60])} countries ({len(latest_data[latest_data['OVERALL GOVERNANCE'] >= 60])/len(latest_data)*100:.1f}%)
     achieved governance scores above 60/100

   • {len(latest_data[latest_data['OVERALL GOVERNANCE'] < 50])} countries ({len(latest_data[latest_data['OVERALL GOVERNANCE'] < 50])/len(latest_data)*100:.1f}%)
     scored below 50/100, indicating significant governance challenges

5. METHODOLOGY NOTES

   The Ibrahim Index of African Governance (IIAG) provides a comprehensive assessment framework:
   • Covers 54 African countries
   • Uses ~100 indicators from ~30 independent sources
   • Scores range from 0-100 (higher is better)
   • Four main categories with equal weighting
   • Annual updates reflecting latest available data

    """

    ax.text(0.05, 0.95, analysis_text, ha='left', va='top', fontsize=8.5,
            transform=ax.transAxes, family='monospace')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # ========== REFERENCES PAGE ==========
    print("Creating references page...")
    fig = plt.figure(figsize=(11, 8.5))
    ax = fig.add_subplot(111)
    ax.axis('off')

    references_text = """
REFERENCES

Mo Ibrahim Foundation (2024). Ibrahim Index of African Governance (IIAG) 2024.
Available at: https://mo.ibrahim.foundation/iiag [Accessed: """ + datetime.now().strftime('%d %B %Y') + """].

Mo Ibrahim Foundation (2024). '2024 IIAG Composite Scores Dataset'.
Mo Ibrahim Foundation Data Portal.

Mo Ibrahim Foundation (2023). 2023 Ibrahim Index of African Governance:
Index Report. London: Mo Ibrahim Foundation.

African Development Bank (2023). African Economic Outlook 2023.
Abidjan: African Development Bank Group.

United Nations Development Programme (2023). Human Development Report 2023.
New York: UNDP.

World Bank (2023). Worldwide Governance Indicators 2023.
Washington DC: World Bank Group.


ABOUT THE IBRAHIM INDEX OF AFRICAN GOVERNANCE (IIAG)

The IIAG is the most comprehensive assessment of African governance, providing an annual
statistical measure of governance performance in every African country. Launched in 2007
by the Mo Ibrahim Foundation, it covers all 54 African countries and is based on data from
over 30 independent African and global institutions.

The Index measures governance performance across four main categories:
• Security & Rule of Law
• Participation, Rights & Inclusion
• Foundations for Economic Opportunity
• Human Development

Each category comprises subcategories and indicators that assess different dimensions of
governance, from civil liberties to infrastructure development.


METHODOLOGY

Data Sources: The IIAG uses approximately 100 indicators from reputable independent sources
including international organizations, research institutes, and African institutions.

Scoring: All indicators are converted to a 0-100 scale where 100 represents the best
possible outcome. Country scores are calculated as weighted averages of indicator values.

Coverage: The analysis in this report covers """ + f"{earliest_year}-{latest_year}" + """, examining trends
across """ + f"{len(countries_list)} countries" + """ and providing insights into governance performance at
continental, regional, and national levels.


ACKNOWLEDGMENTS

This report utilizes data provided by the Mo Ibrahim Foundation under their open data
policy. The analysis, interpretations, and conclusions presented are those of the report
author and do not necessarily reflect the views of the Mo Ibrahim Foundation.
    """

    ax.text(0.08, 0.95, references_text, ha='left', va='top', fontsize=9,
            transform=ax.transAxes)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # Set PDF metadata
    d = pdf.infodict()
    d['Title'] = f'Ibrahim Index of African Governance - Comprehensive Report {latest_year}'
    d['Author'] = 'Data Analysis Team'
    d['Subject'] = f'African Governance Analysis {earliest_year}-{latest_year}'
    d['Keywords'] = 'IIAG, African Governance, Mo Ibrahim Foundation'
    d['CreationDate'] = datetime.now()

print(f"\n{'='*80}")
print("REPORT GENERATION COMPLETE!")
print(f"{'='*80}")
print(f"\nReport saved as: {pdf_filename}")
print(f"Total pages: ~13")
print("\nReport Contents:")
print("  1. Cover Page")
print("  2. Executive Summary")
print("  3. Governance Distribution & Regional Comparison")
print("  4. Top and Bottom 15 Countries")
print("  5. Continental Governance Trends")
print("  6. Category Performance Heatmap")
print("  7. Governance Change Analysis")
print("  8. Regional Performance Comparison")
print("  9. Category Correlation Analysis")
print("  10. Top/Bottom Country Trends")
print("  11. Detailed Analysis and Insights")
print("  12. References and Methodology")
print(f"\n{'='*80}")
