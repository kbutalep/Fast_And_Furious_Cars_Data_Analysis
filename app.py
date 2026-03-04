from dash import Dash, dcc, html, Input, Output, State, ALL, ctx
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Data ──────────────────────────────────────────────────────────────────────
car_sales = pd.read_csv('car_sales_clean.csv', parse_dates=['Sale Date'])
df = pd.read_csv('ff_cars_clean.csv')

# ── Theme (Plotly charts need Python values) ───────────────────────────────────
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

def card(children):
    return html.Div(children, className='card')

def section_label(text):
    return html.Div(text, className='section-label')

_COLOR_TO_MOD = {ACCENT: '--accent', GREEN: '--green', BLUE: '--blue'}

def stat_block(label, value, color=TEXT):
    mod = _COLOR_TO_MOD.get(color, '')
    return html.Div([
        html.Div(label, className='stat-label'),
        html.Div(value, className=f'stat-value{mod}'),
    ], className='stat-block')

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
        html.H2('FAST & FURIOUS', className='app-title'),
        html.P('Auction Data Explorer', className='app-subtitle'),
    ], className='app-header'),

    dcc.Store(id='selected-movie', data=None),

    # Film tiles
    html.Div([
        html.Div([
            html.Div(code, className='film-tile-code'),
            html.Div(name, className='film-tile-name'),
        ],
        id={'type': 'film-btn', 'index': code},
        className='film-tile',
        n_clicks=0,
        )
        for code, name in FILMS
    ], className='film-selector'),

    # Main layout
    html.Div([

        # Sidebar
        html.Div([
            card([
                section_label('Filters'),
                html.Label('Car', className='filter-label'),
                dcc.Dropdown(
                    id='car-dropdown',
                    value=None,
                    placeholder='All cars...',
                    clearable=True,
                ),
                html.Label('Model Year', className='filter-label filter-label-mt'),
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
                            className='chart-fixed-height')]),
            card([dcc.Graph(id='value-comparison-chart', config={'displayModeBar': False})]),
        ], className='nine columns'),

    ], className='row main-grid'),

], className='app-shell')


# ── Callbacks ─────────────────────────────────────────────────────────────────

# 0a. Film tile click → store selection (click again to deselect)
@app.callback(
    Output('selected-movie', 'data'),
    Input({'type': 'film-btn', 'index': ALL}, 'n_clicks'),
    State('selected-movie', 'data'),
    prevent_initial_call=True,
)
def select_movie(_n_clicks, current):
    triggered = ctx.triggered_id
    if triggered is None:
        return current
    clicked = triggered['index']
    return None if clicked == current else clicked


# 0b. Highlight the active tile
@app.callback(
    Output({'type': 'film-btn', 'index': ALL}, 'className'),
    Input('selected-movie', 'data'),
    State({'type': 'film-btn', 'index': ALL}, 'id'),
)
def update_tile_classes(selected, ids):
    return [
        'film-tile film-tile--selected' if id_obj['index'] == selected else 'film-tile'
        for id_obj in ids
    ]


# 1. Movie → car dropdown options + reset selection
@app.callback(
    [Output('car-dropdown', 'options'),
     Output('car-dropdown', 'value')],
    Input('selected-movie', 'data')
)
def update_car_options(movie):
    if movie is None:
        pool = df[df['Car Sales Count'] > 0]
    else:
        pool = df[(df['Film Order'].str.contains(movie)) & (df['Car Sales Count'] > 0)]
    options = [{'label': c, 'value': c} for c in sorted(pool['Car Name'].unique())]
    return options, None


# 2. Car / movie → year dropdown options + reset selection
@app.callback(
    [Output('year-dropdown', 'options'),
     Output('year-dropdown', 'value')],
    [Input('car-dropdown', 'value'),
     Input('selected-movie', 'data')]
)
def update_year_options(car, movie):
    if car is not None:
        years = sorted(df[df['Car Name'] == car]['Year'].unique())
    elif movie is not None:
        pool = df[df['Film Order'].str.contains(movie) & (df['Car Sales Count'] > 0)]
        years = sorted(pool['Year'].unique())
    else:
        years = sorted(df['Year'].unique())
    return [{'label': str(int(y)), 'value': y} for y in years], None


# 3. Sidebar stats — driven by car selection (specific) or movie (aggregate)
@app.callback(
    [Output('stat-avg', 'children'),
     Output('stat-count', 'children'),
     Output('stat-max', 'children'),
     Output('stat-min', 'children')],
    [Input('car-dropdown', 'value'),
     Input('selected-movie', 'data')]
)
def update_stats(car, movie):
    if car is not None:
        rows = df[df['Car Name'] == car]
        if movie is not None:
            movie_rows = rows[rows['Film Order'].str.contains(movie)]
            if not movie_rows.empty:
                rows = movie_rows
        row = rows[rows['Car Sales Count'] > 0]
        if row.empty:
            return [stat_block('No data', '—')] * 4
        row = row.iloc[0]
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


# 4. Price history chart — car-level or movie-level, optionally filtered by year
@app.callback(
    Output('price-history-chart', 'figure'),
    [Input('car-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('selected-movie', 'data')]
)
def update_price_history(car, year, movie):
    if car is None and movie is None:
        return empty_fig('Select a film or car to view auction price history')

    if car is not None:
        models = df[df['Car Name'] == car]['Model'].values
        color_col = 'Model'
        title = f'{car} — Price History'
    else:
        movie_cars = df[df['Film Order'].str.contains(movie) & (df['Car Sales Count'] > 0)]
        models = movie_cars['Model'].values
        color_col = 'Car Name'
        title = f'{dict(FILMS).get(movie, movie)} — Price History'

    data = car_sales[car_sales['Model'].isin(models)].copy()

    if year is not None:
        data = data[data['Year'] == year]

    if data.empty:
        return empty_fig('No auction records found for this selection')

    if color_col == 'Car Name':
        model_to_car = df.drop_duplicates('Model').set_index('Model')['Car Name'].to_dict()
        data = data.assign(**{'Car Name': data['Model'].map(model_to_car)})

    data = data.sort_values(['Sale Date'])

    fig = px.line(
        data, x='Sale Date', y='Sale Amount',
        color=color_col, markers=True,
        labels={'Sale Date': '', 'Sale Amount': 'Sale Price (USD)', 'Source': 'Auction House'},
        color_discrete_sequence=[ACCENT, BLUE, '#a78bfa', '#34d399', '#fb7185'],
        hover_data=['Source'],
    )
    fig.update_traces(line=dict(width=2), marker=dict(size=7))
    fig.update_layout(**plot_base(title))
    fig.update_layout(
        height=300,
        yaxis=dict(tickprefix='$', tickformat=',.0f'),
        legend_title='',
    )
    return fig


# 5. Car value comparison — average sale by car, filtered by movie
@app.callback(
    Output('value-comparison-chart', 'figure'),
    Input('selected-movie', 'data')
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

    fig.add_annotation(x=1, y=1.05, xref='paper', yref='paper',
        text=f'<span style="color:{ACCENT}">■</span> Major role  '
             f'<span style="color:{BLUE}">■</span> Minor role',
        showarrow=False, font=dict(size=10, color=MUTED), xanchor='right')

    chart_height = max(220, len(subset) * 30 + 80)
    fig.update_layout(**plot_base(title))
    fig.update_layout(
        height=chart_height,
        xaxis=dict(tickprefix='$', tickformat=',.0f', title='Average Sale (USD)'),
        yaxis=dict(tickfont=dict(size=10), automargin=True),
        showlegend=False,
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
