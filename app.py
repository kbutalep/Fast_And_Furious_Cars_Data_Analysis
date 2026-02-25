from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Data ──────────────────────────────────────────────────────────────────────
car_sales = pd.read_csv('car_sales_clean.csv', parse_dates=['Sale Date'])
df = pd.read_csv('ff_cars_clean.csv')

# ── Theme ─────────────────────────────────────────────────────────────────────
BG     = '#111827'
CARD   = '#1f2937'
BORDER = '#374151'
ACCENT = '#f97316'
BLUE   = '#00aeef'
TEXT   = '#f9fafb'
MUTED  = '#9ca3af'
GREEN  = '#22c55e'

FILMS = [
    ('FF1', 'The Fast and the Furious'),
    ('FF2', '2 Fast 2 Furious'),
    ('FF3', 'Tokyo Drift'),
    ('FF4', 'Fast & Furious'),
    ('FF5', 'Fast Five'),
    ('FF6', 'Fast & Furious 6'),
    ('FF7', 'Furious 7'),
    ('FF8', 'Fate of the Furious'),
    ('FF9', 'F9'),
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    try:
        fv = float(v)
        return 'N/A' if np.isnan(fv) else f'${fv:,.0f}'
    except (TypeError, ValueError):
        return 'N/A'

def card(children, extra=None):
    style = {
        'backgroundColor': CARD,
        'border': f'1px solid {BORDER}',
        'borderRadius': '8px',
        'padding': '1rem',
        'marginBottom': '12px',
    }
    if extra:
        style.update(extra)
    return html.Div(children, style=style)

def section_label(text):
    return html.Div(text, style={
        'color': ACCENT,
        'fontSize': '10px',
        'letterSpacing': '2px',
        'textTransform': 'uppercase',
        'fontWeight': '700',
        'marginBottom': '12px',
    })

def stat_block(label, value, color=TEXT):
    return html.Div([
        html.Div(label, style={
            'color': MUTED, 'fontSize': '10px',
            'letterSpacing': '1px', 'textTransform': 'uppercase',
        }),
        html.Div(value, style={
            'color': color, 'fontSize': '18px', 'fontWeight': '700', 'marginTop': '2px',
        }),
    ], style={'marginBottom': '10px'})

def plot_base(title=''):
    return dict(
        template='plotly_dark',
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font=dict(color=TEXT, family='Arial, sans-serif', size=11),
        title=dict(text=title, font=dict(color=TEXT, size=13), x=0.01),
        margin=dict(l=40, r=20, t=45, b=40),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor='rgba(0,0,0,0)'),
    )

def empty_fig(message):
    fig = go.Figure()
    fig.add_annotation(
        text=message, xref='paper', yref='paper', x=0.5, y=0.5,
        showarrow=False, font=dict(size=13, color=MUTED),
    )
    fig.update_layout(**plot_base())
    return fig

# ── App ───────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([

    # Header
    html.Div([
        html.H2('FAST & FURIOUS', style={
            'color': ACCENT, 'letterSpacing': '6px', 'margin': '0',
            'fontWeight': '900', 'fontSize': '2rem',
        }),
        html.P('Auction Data Explorer', style={
            'color': MUTED, 'letterSpacing': '3px',
            'margin': '6px 0 0 0', 'fontSize': '11px', 'textTransform': 'uppercase',
        }),
    ], style={'textAlign': 'center', 'padding': '2rem 0 1.5rem 0'}),

    # Film tiles
    html.Div([
        dcc.RadioItems(
            id='movie-select',
            options=[
                {
                    'label': html.Div([
                        html.Div(code, style={'fontWeight': '700', 'fontSize': '13px', 'color': TEXT}),
                        html.Div(name, style={'fontSize': '9px', 'color': MUTED, 'marginTop': '3px'}),
                    ]),
                    'value': code,
                }
                for code, name in FILMS
            ],
            value=None,
            inputStyle={'display': 'none'},
            labelStyle={
                'display': 'inline-block',
                'margin': '0 3px',
                'padding': '8px 10px',
                'backgroundColor': CARD,
                'border': f'1px solid {BORDER}',
                'borderRadius': '6px',
                'cursor': 'pointer',
                'textAlign': 'center',
                'minWidth': '68px',
                'verticalAlign': 'top',
            },
            style={'textAlign': 'center'},
        ),
    ], style={'padding': '0 1rem 1.5rem 1rem'}),

    # Main layout
    html.Div([

        # Sidebar
        html.Div([
            card([
                section_label('Filters'),
                html.Label('Car', style={'color': MUTED, 'fontSize': '11px', 'display': 'block', 'marginBottom': '4px'}),
                dcc.Dropdown(
                    id='car-dropdown',
                    value=None,
                    placeholder='All cars...',
                    clearable=True,
                ),
                html.Label('Model Year', style={'color': MUTED, 'fontSize': '11px', 'display': 'block', 'marginTop': '12px', 'marginBottom': '4px'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    value=None,
                    placeholder='All years...',
                    clearable=True,
                ),
            ]),
            card([
                section_label('Stats'),
                html.Div(id='stat-avg'),
                html.Div(id='stat-count'),
                html.Div(id='stat-max'),
                html.Div(id='stat-min'),
            ]),
        ], className='three columns'),

        # Charts
        html.Div([
            card([dcc.Graph(id='price-history-chart', config={'displayModeBar': False},
                            style={'height': '300px'})]),
            card([dcc.Graph(id='value-comparison-chart', config={'displayModeBar': False})]),
        ], className='nine columns'),

    ], className='row', style={'padding': '0 1rem'}),

], style={
    'backgroundColor': BG,
    'minHeight': '100vh',
    'color': TEXT,
    'fontFamily': 'Arial, sans-serif',
})


# ── Callbacks ─────────────────────────────────────────────────────────────────

# 1. Movie → car dropdown options + reset selection
@app.callback(
    [Output('car-dropdown', 'options'),
     Output('car-dropdown', 'value')],
    Input('movie-select', 'value')
)
def update_car_options(movie):
    if movie is None:
        pool = df[df['Car Sales Count'] > 0]
    else:
        pool = df[(df['Film Order'].str.contains(movie)) & (df['Car Sales Count'] > 0)]
    options = [{'label': c, 'value': c} for c in sorted(pool['Car Name'].unique())]
    return options, None


# 2. Car → year dropdown options + reset selection
@app.callback(
    [Output('year-dropdown', 'options'),
     Output('year-dropdown', 'value')],
    Input('car-dropdown', 'value')
)
def update_year_options(car):
    if car is None:
        years = sorted(df['Year'].unique())
    else:
        years = sorted(df[df['Car Name'] == car]['Year'].unique())
    return [{'label': str(int(y)), 'value': y} for y in years], None


# 3. Sidebar stats — driven by car selection (specific) or movie (aggregate)
@app.callback(
    [Output('stat-avg', 'children'),
     Output('stat-count', 'children'),
     Output('stat-max', 'children'),
     Output('stat-min', 'children')],
    [Input('car-dropdown', 'value'),
     Input('movie-select', 'value')]
)
def update_stats(car, movie):
    if car is not None:
        row = df[df['Car Name'] == car].iloc[0]
        return (
            stat_block('Avg Sale Price', fmt(row['mean']), ACCENT),
            stat_block('Auction Sales', str(int(row['Car Sales Count'])), TEXT),
            stat_block('Highest Sale', fmt(row['max']), GREEN),
            stat_block('Lowest Sale', fmt(row['min']), BLUE),
        )

    if movie is not None:
        subset = df[(df['Film Order'].str.contains(movie)) & (df['Car Sales Count'] > 0)]
    else:
        subset = df[df['Car Sales Count'] > 0]

    if subset.empty:
        return [stat_block('No data', '—')] * 4

    avg   = subset['mean'].mean()
    total = int(subset['Car Sales Count'].sum())
    max_v = subset['max'].max()
    min_pool = subset.loc[subset['min'] > 0, 'min']
    min_v = min_pool.min() if not min_pool.empty else float('nan')

    return (
        stat_block('Avg Sale Price', fmt(avg), ACCENT),
        stat_block('Auction Sales', str(total), TEXT),
        stat_block('Highest Sale', fmt(max_v), GREEN),
        stat_block('Lowest Sale', fmt(min_v), BLUE),
    )


# 4. Price history chart — for the selected car, optionally filtered by year
@app.callback(
    Output('price-history-chart', 'figure'),
    [Input('car-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_price_history(car, year):
    if car is None:
        return empty_fig('Select a car to view its auction price history')

    models = df[df['Car Name'] == car]['Model'].values
    data = car_sales[car_sales['Model'].isin(models)].copy()

    if year is not None:
        data = data[data['Year'] == year]

    if data.empty:
        return empty_fig('No auction records found for this selection')

    data = data.sort_values(['Sale Date'])

    fig = px.line(
        data, x='Sale Date', y='Sale Amount',
        color='Model', markers=True,
        labels={'Sale Date': '', 'Sale Amount': 'Sale Price (USD)', 'Source': 'Auction House'},
        color_discrete_sequence=[ACCENT, BLUE, '#a78bfa', '#34d399', '#fb7185'],
        hover_data=['Source'],
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=7))
    fig.update_layout(
        **plot_base(f'{car} — Price History'),
        height=300,
        yaxis=dict(tickprefix='$', tickformat=',.0f', gridcolor=BORDER),
        xaxis=dict(gridcolor=BORDER),
        legend_title='',
    )
    return fig


# 5. Car value comparison — average sale by car, filtered by movie
@app.callback(
    Output('value-comparison-chart', 'figure'),
    Input('movie-select', 'value')
)
def update_value_comparison(movie):
    if movie is None:
        subset = df[df['Car Sales Count'] > 0].copy()
        title = 'Average Auction Price — All Cars with Sales Data'
    else:
        subset = df[(df['Film Order'].str.contains(movie)) & (df['Car Sales Count'] > 0)].copy()
        movie_name = dict(FILMS).get(movie, movie)
        title = f'Average Auction Price — {movie_name}'

    if subset.empty:
        return empty_fig('No sales data available for this selection')

    subset = subset.sort_values('mean')
    subset['short_name'] = subset['Car Name'].apply(
        lambda x: x if len(x) <= 38 else x[:35] + '...'
    )
    # Orange = Major role, Blue = Minor role
    bar_colors = [ACCENT if str(r) == 'Major' else BLUE for r in subset['Role']]

    fig = go.Figure(go.Bar(
        y=subset['short_name'],
        x=subset['mean'],
        orientation='h',
        marker_color=bar_colors,
        error_x=dict(
            type='data',
            symmetric=False,
            array=subset['max'] - subset['mean'],
            arrayminus=subset['mean'] - subset['min'],
            color=MUTED,
            thickness=1.5,
            width=4,
        ),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Avg: $%{x:,.0f}<br>'
            'Sales: %{customdata[0]:.0f}<extra></extra>'
        ),
        customdata=subset[['Car Sales Count']],
    ))

    # Legend annotations (Major/Minor)
    fig.add_annotation(x=1, y=1.05, xref='paper', yref='paper',
        text=f'<span style="color:{ACCENT}">■</span> Major role  '
             f'<span style="color:{BLUE}">■</span> Minor role',
        showarrow=False, font=dict(size=10, color=MUTED), xanchor='right')

    chart_height = max(220, len(subset) * 30 + 80)
    fig.update_layout(
        **plot_base(title),
        height=chart_height,
        xaxis=dict(tickprefix='$', tickformat=',.0f', title='Average Sale (USD)', gridcolor=BORDER),
        yaxis=dict(tickfont=dict(size=10), automargin=True),
        showlegend=False,
    )
    return fig


app.run(debug=True)
