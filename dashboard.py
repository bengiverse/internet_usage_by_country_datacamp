import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os


# Load und clean data
df_raw = pd.read_csv('internet_usage.csv')
df = df_raw.replace('..', np.nan)

year_cols = [str(y) for y in range(2000, 2024)]
for col in year_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Long format (country, year, usage_pct)
df_long = df.melt(
    id_vars=['Country Name', 'Country Code'],
    value_vars=year_cols,
    var_name='Year',
    value_name='Internet Usage (%)'
)
df_long['Year'] = df_long['Year'].astype(int)
df_long = df_long.dropna(subset=['Internet Usage (%)'])

# Latest snapshot per country (most recent available year)
df_latest = (
    df_long.sort_values('Year', ascending=False)
    .groupby('Country Name', as_index=False)
    .first()
)

# World average per year
df_world_avg = (
    df_long.groupby('Year')['Internet Usage (%)']
    .mean()
    .reset_index()
    .rename(columns={'Internet Usage (%)': 'World Average (%)'})
)

all_countries = sorted(df['Country Name'].tolist())

# Colors
BG        = '#0f1117'
CARD      = '#1a1d27'
BORDER    = '#2a2d3e'
ACCENT    = '#4f8ef7'
ACCENT2   = '#f7794f'
TEXT      = '#e8eaf0'
SUBTEXT   = '#8b8fa8'
GRIDLINE  = '#22253a'

FONT = "'DM Sans', 'Segoe UI', sans-serif"

def card(children, style_extra=None):
    base = {
        'background': CARD,
        'border': f'1px solid {BORDER}',
        'borderRadius': '12px',
        'padding': '20px 24px',
    }
    if style_extra:
        base.update(style_extra)
    return html.Div(children, style=base)

def section_title(text, sub=None):
    elems = [html.H3(text, style={'margin': '0 0 4px', 'color': TEXT, 'fontSize': '15px', 'fontWeight': '600'})]
    if sub:
        elems.append(html.P(sub, style={'margin': 0, 'color': SUBTEXT, 'fontSize': '12px'}))
    return html.Div(elems, style={'marginBottom': '16px'})

# Dashboard
app = dash.Dash(__name__)
app.title = 'Global Internet Usage Dashboard'

app.layout = html.Div(style={
    'fontFamily': FONT,
    'backgroundColor': BG,
    'minHeight': '100vh',
    'padding': '28px 36px',
    'boxSizing': 'border-box',
}, children=[

    # Header
    html.Div([
        html.H1('🌐 Global Internet Usage', style={
            'color': TEXT, 'fontSize': '26px', 'fontWeight': '700', 'margin': '0 0 4px'
        }),
        html.P('% of population using the internet · 217 countries · 2000–2023 · World Bank',
               style={'color': SUBTEXT, 'fontSize': '13px', 'margin': 0}),
    ], style={'marginBottom': '28px'}),

    # ROW 1: KPI cards
    html.Div(id='kpi-row', style={
        'display': 'grid',
        'gridTemplateColumns': 'repeat(4, 1fr)',
        'gap': '16px',
        'marginBottom': '20px',
    }),

    # ROW 2: World trend + Top / Bottom countries
    html.Div([
        # World average trend
        card([
            section_title('World Average Over Time',
                          'Mean internet penetration across all countries per year'),
            dcc.Graph(id='world-trend', config={'displayModeBar': False},
                      style={'height': '260px'}),
        ], {'flex': '2', 'minWidth': 0}),

        # Top / Bottom snapshot
        card([
            section_title('Country Rankings',
                          'Most recent available year per country'),
            html.Div([
                html.Label('Show:', style={'color': SUBTEXT, 'fontSize': '12px', 'marginRight': '8px'}),
                dcc.RadioItems(
                    id='rank-toggle',
                    options=[{'label': 'Top 10', 'value': 'top'}, {'label': 'Bottom 10', 'value': 'bottom'}],
                    value='top',
                    inline=True,
                    labelStyle={'marginRight': '14px', 'color': TEXT, 'fontSize': '13px'},
                    inputStyle={'marginRight': '4px'},
                ),
            ], style={'marginBottom': '12px'}),
            dcc.Graph(id='rank-chart', config={'displayModeBar': False},
                      style={'height': '220px'}),
        ], {'flex': '1.2', 'minWidth': 0}),

    ], style={'display': 'flex', 'gap': '16px', 'marginBottom': '20px'}),

    #  ROW 3: Country comparison + World map
    html.Div([
        # Country comparison line chart
        card([
            section_title('Compare Countries Over Time',
                          'Select up to 8 countries to compare their internet adoption trend'),
            dcc.Dropdown(
                id='country-picker',
                options=[{'label': c, 'value': c} for c in all_countries],
                value=['United States', 'China', 'India', 'Brazil', 'Nigeria'],
                multi=True,
                placeholder='Search and select countries…',
                style={'marginBottom': '12px'},
            ),
            dcc.Graph(id='country-lines', config={'displayModeBar': False},
                      style={'height': '280px'}),
        ], {'flex': '1.5', 'minWidth': 0}),

        # World choropleth
        card([
            section_title('World Map by Year',
                          'Drag the slider to see how access has spread'),
            dcc.Slider(
                id='year-slider',
                min=2000, max=2022, step=1, value=2022,
                marks={y: {'label': str(y), 'style': {'color': SUBTEXT, 'fontSize': '10px'}}
                       for y in range(2000, 2023, 4)},
                tooltip={'placement': 'bottom', 'always_visible': False},
            ),
            dcc.Graph(id='world-map', config={'displayModeBar': False},
                      style={'height': '280px'}),
        ], {'flex': '2', 'minWidth': 0}),

    ], style={'display': 'flex', 'gap': '16px'}),

])


#  Graph theme helper 
def apply_theme(fig, height=None):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=FONT, color=TEXT, size=11),
        margin=dict(l=0, r=0, t=4, b=0),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color=TEXT, size=11)),
        xaxis=dict(gridcolor=GRIDLINE, linecolor=BORDER, tickcolor=BORDER, zerolinecolor=GRIDLINE),
        yaxis=dict(gridcolor=GRIDLINE, linecolor=BORDER, tickcolor=BORDER, zerolinecolor=GRIDLINE),
    )
    if height:
        fig.update_layout(height=height)
    return fig


#  Callbacks 

@app.callback(Output('kpi-row', 'children'), Input('year-slider', 'value'))
def update_kpis(year):
    yr = str(year)
    vals = pd.to_numeric(df[yr], errors='coerce').dropna()
    world_avg = vals.mean()
    n_above_50 = (vals >= 50).sum()
    n_below_10 = (vals < 10).sum()

    # Global avg change vs previous year
    prev_yr = str(year - 1)
    prev_vals = pd.to_numeric(df[prev_yr], errors='coerce').dropna()
    delta = world_avg - prev_vals.mean() if len(prev_vals) else 0

    def kpi(label, value, suffix='', delta_val=None, color=ACCENT):
        delta_el = []
        if delta_val is not None:
            arrow = '▲' if delta_val >= 0 else '▼'
            delta_color = '#4ecb71' if delta_val >= 0 else ACCENT2
            delta_el = [html.Span(f'{arrow} {abs(delta_val):.1f}pp vs prev year',
                                  style={'color': delta_color, 'fontSize': '11px'})]
        return card([
            html.P(label, style={'color': SUBTEXT, 'fontSize': '12px', 'margin': '0 0 6px'}),
            html.Div([
                html.Span(value, style={'color': color, 'fontSize': '28px', 'fontWeight': '700'}),
                html.Span(suffix, style={'color': SUBTEXT, 'fontSize': '14px', 'marginLeft': '4px'}),
            ]),
        ] + delta_el)

    return [
        kpi(f'World Avg in {year}', f'{world_avg:.1f}', '%', delta),
        kpi('Countries with data', str(len(vals)), 'countries'),
        kpi('Above 50% access', str(n_above_50), 'countries', color='#4ecb71'),
        kpi('Below 10% access', str(n_below_10), 'countries', color=ACCENT2),
    ]


@app.callback(Output('world-trend', 'figure'), Input('year-slider', 'value'))
def update_world_trend(selected_year):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_world_avg['Year'], y=df_world_avg['World Average (%)'],
        mode='lines+markers',
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=5, color=ACCENT),
        fill='tozeroy',
        fillcolor='rgba(79,142,247,0.1)',
        name='World Avg',
        hovertemplate='%{x}: %{y:.1f}%<extra></extra>',
    ))
    # Highlight selected year
    sel_val = df_world_avg.loc[df_world_avg['Year'] == selected_year, 'World Average (%)']
    if not sel_val.empty:
        fig.add_vline(x=selected_year, line_dash='dot', line_color=ACCENT2, line_width=1.5)
        fig.add_annotation(x=selected_year, y=sel_val.values[0],
                           text=f'{sel_val.values[0]:.1f}%',
                           showarrow=True, arrowhead=2, arrowcolor=ACCENT2,
                           font=dict(color=ACCENT2, size=11), bgcolor=CARD, bordercolor=BORDER)
    fig.update_yaxes(title_text='Avg Usage (%)', range=[0, 75])
    apply_theme(fig)
    return fig


@app.callback(Output('rank-chart', 'figure'), Input('rank-toggle', 'value'))
def update_ranks(mode):
    n = 10
    sorted_df = df_latest.sort_values('Internet Usage (%)', ascending=(mode == 'bottom'))
    subset = sorted_df.head(n)
    color = '#4ecb71' if mode == 'top' else ACCENT2
    fig = go.Figure(go.Bar(
        x=subset['Internet Usage (%)'],
        y=subset['Country Name'],
        orientation='h',
        marker_color=color,
        hovertemplate='%{y}: %{x:.1f}%<extra></extra>',
    ))
    fig.update_xaxes(range=[0, 105], title_text='%')
    apply_theme(fig)
    return fig


@app.callback(Output('country-lines', 'figure'), Input('country-picker', 'value'))
def update_lines(countries):
    if not countries:
        return go.Figure()
    filtered = df_long[df_long['Country Name'].isin(countries[:8])]
    fig = px.line(
        filtered, x='Year', y='Internet Usage (%)',
        color='Country Name',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    fig.update_traces(marker_size=4, line_width=2,
                      hovertemplate='%{x}: %{y:.1f}%<extra></extra>')
    fig.update_yaxes(range=[0, 105], title_text='Usage (%)')
    fig.update_xaxes(title_text='Year')
    apply_theme(fig)
    return fig


@app.callback(Output('world-map', 'figure'), Input('year-slider', 'value'))
def update_map(year):
    yr = str(year)
    map_df = df[['Country Name', 'Country Code', yr]].copy()
    map_df.columns = ['Country Name', 'Country Code', 'Usage']
    map_df['Usage'] = pd.to_numeric(map_df['Usage'], errors='coerce')
    map_df = map_df.dropna(subset=['Usage'])

    fig = px.choropleth(
        map_df,
        locations='Country Code',
        color='Usage',
        hover_name='Country Name',
        color_continuous_scale='Blues',
        range_color=[0, 100],
        labels={'Usage': 'Usage (%)'},
    )
    fig.update_traces(hovertemplate='<b>%{hovertext}</b><br>%{z:.1f}%<extra></extra>')
    fig.update_geos(
        showcoastlines=True, coastlinecolor=BORDER,
        showland=True, landcolor='#1e2133',
        showocean=True, oceancolor=BG,
        showlakes=False,
        projection_type='natural earth',
    )
    fig.update_coloraxes(colorbar=dict(
        tickfont=dict(color=TEXT, size=10),
        title=dict(text='%', font=dict(color=TEXT)),
        bgcolor=CARD,
        bordercolor=BORDER,
        len=0.7,
        thickness=12,
    ))
    apply_theme(fig)
    fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)'), margin=dict(l=0, r=0, t=0, b=0))
    return fig


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=8050)
