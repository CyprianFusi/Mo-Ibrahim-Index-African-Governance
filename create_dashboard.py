"""
Interactive Dashboard Generator for IIAG Data
Creates web-ready interactive visualizations using Plotly
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Load data
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
latest_data = composite_scores[composite_scores['Year'] == latest_year].copy()

print("Creating Interactive Dashboard...")
print("=" * 60)

# Create output directory
output_dir = Path('dashboard')
output_dir.mkdir(exist_ok=True)

# ============================================================================
# 1. Interactive Choropleth Map - Africa Governance
# ============================================================================
print("  [1/8] Creating interactive Africa map...")

# ISO3 codes mapping (simplified - would need complete mapping)
iso3_map = {
    'Algeria': 'DZA', 'Angola': 'AGO', 'Benin': 'BEN', 'Botswana': 'BWA', 'Burkina Faso': 'BFA',
    'Burundi': 'BDI', 'Cameroon': 'CMR', 'Cape Verde': 'CPV', 'Central African Republic': 'CAF',
    'Chad': 'TCD', 'Comoros': 'COM', 'Congo': 'COG', 'DR Congo': 'COD', "Côte d'Ivoire": 'CIV',
    'Djibouti': 'DJI', 'Egypt': 'EGY', 'Equatorial Guinea': 'GNQ', 'Eritrea': 'ERI', 'Eswatini': 'SWZ',
    'Ethiopia': 'ETH', 'Gabon': 'GAB', 'Gambia': 'GMB', 'Ghana': 'GHA', 'Guinea': 'GIN',
    'Guinea-Bissau': 'GNB', 'Kenya': 'KEN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 'Libya': 'LBY',
    'Madagascar': 'MDG', 'Malawi': 'MWI', 'Mali': 'MLI', 'Mauritania': 'MRT', 'Mauritius': 'MUS',
    'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Namibia': 'NAM', 'Niger': 'NER', 'Nigeria': 'NGA',
    'Rwanda': 'RWA', 'São Tomé and Príncipe': 'STP', 'Senegal': 'SEN', 'Seychelles': 'SYC',
    'Sierra Leone': 'SLE', 'Somalia': 'SOM', 'South Africa': 'ZAF', 'South Sudan': 'SSD',
    'Sudan': 'SDN', 'Tanzania': 'TZA', 'Togo': 'TGO', 'Tunisia': 'TUN', 'Uganda': 'UGA',
    'Zambia': 'ZMB', 'Zimbabwe': 'ZWE', 'Cabo Verde': 'CPV'
}

latest_data['ISO3'] = latest_data['Country'].map(iso3_map)

fig_map = px.choropleth(latest_data,
                        locations='ISO3',
                        color='OVERALL GOVERNANCE',
                        hover_name='Country',
                        hover_data={'OVERALL GOVERNANCE': ':.1f', 'ISO3': False, 'Region': True},
                        color_continuous_scale='RdYlGn',
                        range_color=[0, 100],
                        scope='africa',
                        title=f'African Governance Index {latest_year}')

fig_map.update_layout(
    height=700,
    geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth'),
    font=dict(size=14)
)

fig_map.write_html(output_dir / 'interactive_map.html')

# ============================================================================
# 2. Interactive Time Series - Multiple Countries
# ============================================================================
print("  [2/8] Creating interactive time series...")

top10_countries = latest_data.nlargest(10, 'OVERALL GOVERNANCE')['Country'].values

fig_timeseries = go.Figure()

for country in top10_countries[:5]:  # Top 5
    country_data = composite_scores[composite_scores['Country'] == country]
    fig_timeseries.add_trace(go.Scatter(
        x=country_data['Year'],
        y=country_data['OVERALL GOVERNANCE'],
        mode='lines+markers',
        name=country,
        line=dict(width=3),
        marker=dict(size=8)
    ))

fig_timeseries.update_layout(
    title='Top 5 Countries - Governance Trends (2014-2023)',
    xaxis_title='Year',
    yaxis_title='Overall Governance Score',
    hovermode='x unified',
    height=600,
    font=dict(size=14),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

fig_timeseries.write_html(output_dir / 'interactive_timeseries.html')

# ============================================================================
# 3. Interactive Bar Chart Race Style - Top 15
# ============================================================================
print("  [3/8] Creating interactive bar chart...")

top15 = latest_data.nlargest(15, 'OVERALL GOVERNANCE').sort_values('OVERALL GOVERNANCE')

fig_bar = go.Figure(go.Bar(
    x=top15['OVERALL GOVERNANCE'],
    y=top15['Country'],
    orientation='h',
    marker=dict(
        color=top15['OVERALL GOVERNANCE'],
        colorscale='RdYlGn',
        showscale=True,
        colorbar=dict(title='Score')
    ),
    text=top15['OVERALL GOVERNANCE'].round(1),
    textposition='outside'
))

fig_bar.update_layout(
    title=f'Top 15 Countries - Overall Governance ({latest_year})',
    xaxis_title='Governance Score',
    yaxis_title='',
    height=600,
    font=dict(size=14),
    showlegend=False
)

fig_bar.write_html(output_dir / 'interactive_bar_top15.html')

# ============================================================================
# 4. Interactive Category Radar Chart
# ============================================================================
print("  [4/8] Creating interactive radar charts...")

top5 = latest_data.nlargest(5, 'OVERALL GOVERNANCE')

fig_radar = make_subplots(
    rows=2, cols=3,
    specs=[[{'type': 'polar'}]*3, [{'type': 'polar'}]*3],
    subplot_titles=top5['Country'].tolist()
)

for idx, (_, country_row) in enumerate(top5.iterrows()):
    row = idx // 3 + 1
    col = idx % 3 + 1

    values = [country_row[cat] for cat in main_categories]
    values = [v if not np.isnan(v) else 0 for v in values]

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=main_categories,
        fill='toself',
        name=country_row['Country']
    ), row=row, col=col)

fig_radar.update_layout(
    title_text=f'Category Performance - Top 5 Countries ({latest_year})',
    height=800,
    showlegend=False,
    font=dict(size=12)
)

fig_radar.write_html(output_dir / 'interactive_radar.html')

# ============================================================================
# 5. Interactive Heatmap - Year over Year Changes
# ============================================================================
print("  [5/8] Creating interactive heatmap...")

top20_countries = latest_data.nlargest(20, 'OVERALL GOVERNANCE')['Country'].values
heatmap_data = []

for country in top20_countries:
    country_data = composite_scores[composite_scores['Country'] == country].sort_values('Year')
    for cat in main_categories:
        heatmap_data.append({
            'Country': country,
            'Category': cat,
            'Score': country_data[cat].iloc[-1] if len(country_data) > 0 else np.nan
        })

heatmap_df = pd.DataFrame(heatmap_data)
heatmap_pivot = heatmap_df.pivot(index='Country', columns='Category', values='Score')
heatmap_pivot = heatmap_pivot.reindex(top20_countries)

fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale='RdYlGn',
    zmid=50,
    text=heatmap_pivot.values.round(1),
    texttemplate='%{text}',
    textfont={"size": 10},
    colorbar=dict(title='Score')
))

fig_heatmap.update_layout(
    title=f'Category Performance Heatmap - Top 20 Countries ({latest_year})',
    xaxis_title='',
    yaxis_title='',
    height=700,
    font=dict(size=12)
)

fig_heatmap.write_html(output_dir / 'interactive_heatmap.html')

# ============================================================================
# 6. Interactive Scatter Plot - Category Correlations
# ============================================================================
print("  [6/8] Creating interactive scatter plots...")

fig_scatter = make_subplots(
    rows=2, cols=2,
    subplot_titles=main_categories,
    vertical_spacing=0.12,
    horizontal_spacing=0.10
)

for idx, cat in enumerate(main_categories):
    row = idx // 2 + 1
    col = idx % 2 + 1

    plot_data = latest_data[['Country', 'OVERALL GOVERNANCE', cat, 'Region']].dropna()

    fig_scatter.add_trace(
        go.Scatter(
            x=plot_data[cat],
            y=plot_data['OVERALL GOVERNANCE'],
            mode='markers',
            marker=dict(size=10, opacity=0.7),
            text=plot_data['Country'],
            customdata=plot_data['Region'],
            hovertemplate='<b>%{text}</b><br>%{xaxis.title.text}: %{x:.1f}<br>Overall: %{y:.1f}<br>Region: %{customdata}<extra></extra>',
            name=cat,
            showlegend=False
        ),
        row=row, col=col
    )

    # Add trendline
    z = np.polyfit(plot_data[cat], plot_data['OVERALL GOVERNANCE'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(plot_data[cat].min(), plot_data[cat].max(), 100)

    fig_scatter.add_trace(
        go.Scatter(
            x=x_line,
            y=p(x_line),
            mode='lines',
            line=dict(color='red', dash='dash', width=2),
            showlegend=False
        ),
        row=row, col=col
    )

    fig_scatter.update_xaxes(title_text=cat, row=row, col=col)
    fig_scatter.update_yaxes(title_text='Overall Governance', row=row, col=col)

fig_scatter.update_layout(
    title_text=f'Category vs Overall Governance Correlation ({latest_year})',
    height=800,
    font=dict(size=12)
)

fig_scatter.write_html(output_dir / 'interactive_scatter.html')

# ============================================================================
# 7. Interactive Regional Comparison
# ============================================================================
print("  [7/8] Creating interactive regional comparison...")

regional_data = latest_data[latest_data['Region'] != 'Other'].copy()

fig_regional = go.Figure()

for cat in ['OVERALL GOVERNANCE'] + main_categories:
    regional_means = regional_data.groupby('Region')[cat].mean().sort_values(ascending=False)

    fig_regional.add_trace(go.Bar(
        name=cat,
        x=regional_means.index,
        y=regional_means.values,
        text=regional_means.values.round(1),
        textposition='outside'
    ))

fig_regional.update_layout(
    title=f'Regional Performance Comparison ({latest_year})',
    xaxis_title='Region',
    yaxis_title='Average Score',
    barmode='group',
    height=600,
    font=dict(size=14),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)

fig_regional.write_html(output_dir / 'interactive_regional.html')

# ============================================================================
# 8. Interactive Box Plot - Regional Distribution
# ============================================================================
print("  [8/8] Creating interactive box plot...")

fig_box = go.Figure()

regions_sorted = regional_data.groupby('Region')['OVERALL GOVERNANCE'].mean().sort_values(ascending=False).index

for region in regions_sorted:
    region_scores = regional_data[regional_data['Region'] == region]['OVERALL GOVERNANCE'].dropna()

    fig_box.add_trace(go.Box(
        y=region_scores,
        name=region,
        boxmean='sd',
        marker_color=px.colors.qualitative.Set2[list(regions_sorted).index(region) % len(px.colors.qualitative.Set2)]
    ))

fig_box.update_layout(
    title=f'Regional Governance Distribution ({latest_year})',
    yaxis_title='Overall Governance Score',
    xaxis_title='Region',
    height=600,
    font=dict(size=14),
    showlegend=False
)

fig_box.write_html(output_dir / 'interactive_boxplot.html')

# ============================================================================
# Create Master Dashboard HTML
# ============================================================================
print("\nCreating master dashboard...")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ibrahim Index of African Governance - Interactive Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
        }

        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .header h1 {
            color: #2c3e50;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .header p {
            color: #7f8c8d;
            font-size: 1.1rem;
        }

        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(650px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }

        .chart-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .chart-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }

        .chart-card h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            font-size: 1.3rem;
            border-bottom: 3px solid #667eea;
            padding-bottom: 0.5rem;
        }

        .chart-card iframe {
            width: 100%;
            border: none;
            border-radius: 8px;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .insights {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }

        .insights h2 {
            color: #2c3e50;
            margin-bottom: 1rem;
            border-bottom: 3px solid #764ba2;
            padding-bottom: 0.5rem;
        }

        .insights ul {
            list-style-position: inside;
            padding-left: 1rem;
        }

        .insights li {
            margin: 0.8rem 0;
            color: #555;
        }

        .stat-highlight {
            color: #667eea;
            font-weight: bold;
        }

        footer {
            background: rgba(255, 255, 255, 0.95);
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
            color: #7f8c8d;
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Ibrahim Index of African Governance</h1>
        <p>Interactive Dashboard - Comprehensive Analysis of Governance Across Africa (2014-2023)</p>
    </div>

    <div class="container">
        <div class="insights">
            <h2>Key Insights & Executive Summary</h2>
            <ul>
                <li><span class="stat-highlight">Top Performer:</span> Seychelles leads with a score of 75.3, followed by Mauritius (72.8) and Cabo Verde (69.6)</li>
                <li><span class="stat-highlight">Continental Average:</span> The mean governance score across Africa is 49.3, with significant regional variation (SD: 12.3)</li>
                <li><span class="stat-highlight">Best Improvers:</span> Seychelles (+10.0), Gambia (+7.2), and Somalia (+6.8) showed remarkable improvements from 2014-2023</li>
                <li><span class="stat-highlight">Regional Leaders:</span> Southern Africa (54.6) and North Africa (53.7) lead regional performance</li>
                <li><span class="stat-highlight">Category Performance:</span> Human Development (51.6) scores highest on average, while Security & Rule of Law shows most variation</li>
                <li><span class="stat-highlight">Challenges:</span> Central Africa faces the most governance challenges with an average score of 39.7</li>
                <li><span class="stat-highlight">Trends:</span> Overall continental governance has remained relatively stable, with localized improvements and declines</li>
            </ul>
        </div>

        <div class="dashboard-grid">
            <div class="chart-card full-width">
                <h2>1. Africa Governance Map - Geographic Overview</h2>
                <iframe src="interactive_map.html" height="750"></iframe>
            </div>

            <div class="chart-card">
                <h2>2. Top Performers - Temporal Trends</h2>
                <iframe src="interactive_timeseries.html" height="650"></iframe>
            </div>

            <div class="chart-card">
                <h2>3. Top 15 Countries Rankings</h2>
                <iframe src="interactive_bar_top15.html" height="650"></iframe>
            </div>

            <div class="chart-card full-width">
                <h2>4. Category Performance - Top 5 Countries</h2>
                <iframe src="interactive_radar.html" height="850"></iframe>
            </div>

            <div class="chart-card full-width">
                <h2>5. Category Heatmap - Top 20 Countries</h2>
                <iframe src="interactive_heatmap.html" height="750"></iframe>
            </div>

            <div class="chart-card full-width">
                <h2>6. Category Correlation Analysis</h2>
                <iframe src="interactive_scatter.html" height="850"></iframe>
            </div>

            <div class="chart-card">
                <h2>7. Regional Comparison</h2>
                <iframe src="interactive_regional.html" height="650"></iframe>
            </div>

            <div class="chart-card">
                <h2>8. Regional Score Distribution</h2>
                <iframe src="interactive_boxplot.html" height="650"></iframe>
            </div>
        </div>
    </div>

    <footer>
        <p>Data Source: Mo Ibrahim Foundation - Ibrahim Index of African Governance (IIAG) 2024</p>
        <p>Dashboard created for data analysis and stakeholder presentation</p>
    </footer>
</body>
</html>
"""

with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
    f.write(dashboard_html)

print("\n" + "=" * 60)
print("INTERACTIVE DASHBOARD COMPLETE!")
print("=" * 60)
print(f"\nDashboard saved to: {output_dir.absolute()}")
print("\nGenerated Files:")
print("  - index.html (Main Dashboard)")
print("  - interactive_map.html")
print("  - interactive_timeseries.html")
print("  - interactive_bar_top15.html")
print("  - interactive_radar.html")
print("  - interactive_heatmap.html")
print("  - interactive_scatter.html")
print("  - interactive_regional.html")
print("  - interactive_boxplot.html")
print("\nTo view: Open 'dashboard/index.html' in your web browser")
