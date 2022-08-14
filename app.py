from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.express as px

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div(children=[
        html.H3(children='Fast and Furious Cars Data'),
        html.H6(children='Cars from the Fast & Furious Movie Franchise',
                style={'marginTop': '-15px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}
    ),

    html.Div(children=[
        ################### Filter box ######################
        html.Div(children=[
            html.Label('Fast & Furious Movie', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input_movie',  ###was input_days
                options=[
                    {'label': 'The Fast and the Furious', 'value': 'FF1'},
                    {'label': '2 Fast 2 Furious', 'value': 'FF2'},
                    {'label': 'The Fast and the Furious: Tokyo Drift', 'value': 'FF3'},
                    {'label': 'Fast & Furious', 'value': 'FF4'},
                    {'label': 'Fast Five', 'value': 'FF5'},
                    {'label': 'Fast & Furious 6', 'value': 'FF6'},
                    {'label': 'Furious 7', 'value': 'FF7'},
                    {'label': 'The Fate of the Furious', 'value': 'FF8'},
                    {'label': 'F9', 'value': 'FF9'}
                ],
                value=None,
                multi=False
            ),
            html.Label('Car', style={'paddingTop': '2rem'}),
            dcc.Dropdown(df.columns, id='pandas-dropdown-1'),
                html.Div(id='pandas-output-container-1')

            # html.Label('Accident Severity:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            # dcc.Checklist(
            #     id='input_acc_sev',
            #     options=[
            #         {'label': 'Fatal', 'value': '1'},
            #         {'label': 'Serious', 'value': '2'},
            #         {'label': 'Slight', 'value': '3'}
            #     ],
            #     value=['1', '2', '3'],
            # ),
            #
            # html.Label('Speed limits (mph):', style={'paddingTop': '2rem'}),
            # dcc.RangeSlider(
            #         id='input_speed_limit',
            #         min=20,
            #         max=70,
            #         step=10,
            #         value=[20, 70],
            #         marks={
            #             20: '20',
            #             30: '30',
            #             40: '40',
            #             50: '50',
            #             60: '60',
            #             70: '70'
            #         },
            # ),

        ], className="four columns",
            style={'padding': '2rem', 'margin': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px',
                   'marginTop': '2rem'}),
    ]),
    ##### HERE insert the code for four boxes & graph #########
    # Number statistics & number of accidents each day

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H3(id='tot_cars', style={'fontWeight': 'bold'}),
                html.Label('Total Cars', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='maj_or_min', style={'fontWeight': 'bold', 'color': '#f73600'}),
                html.Label('Major vs. Minor Car', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='avg_year', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                html.Label('Average Car Model year', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='avg_sale', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                html.Label('Average Sale Amount', style={'paddingTop': '.3rem'}),

            ], className="three columns number-stat-box"),
        ], style={'margin': '1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%',
                  'flex-wrap': 'wrap'}),

        # Scatter plot
        html.Div(children=[
            dcc.Graph(id="scatter-plot"),
            html.P("Filter by sales Price:"),
            dcc.RangeSlider(
                id='range-slider',
                min=0, max=300000, step=5000,
                marks={0: '0', 300000: '300,000'},
                value=[1, 299999]
            )]
            , className="twleve columns",
            style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                   'border-radius': '10px', 'backgroundColor': 'white', }),

    ], className="eight columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'}),

])


@app.callback(
    [Output(component_id='tot_cars', component_property='children'),
     Output('maj_or_min', 'children'),
     Output('avg_year', 'children'),
     Output('avg_sale', 'children'),
     ],
    Input('input_movie', 'value'))
def update_statistics(input_movie):
    if input_movie == None:
        df_update = df
        avg_car_sale = round(car_sales['Sale Amount'].mean(), ndigits=0)
    else:
        df_update = df[(df['Film Order'].str.contains(input_movie))]
        avg_car_sale = 0

    maj = df_update.Role.str.contains('Major').sum()
    minor = df_update.Role.str.contains('Minor').sum()


    return len(df_update), f'{maj} / {minor}', round(df_update['Year'].mean(), ndigits=0), avg_car_sale


@app.callback(
    Output('pandas-output-container-1', 'children'),
    Input('pandas-dropdown-1', 'value')
)
def update_output(value):
    return f'You have selected {value}'

######### Callback for scatter chart ##############################
@app.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (car_sales['Sale Amount'] > low) & (car_sales['Sale Amount'] < high)
    fig = px.scatter(
        car_sales[mask], x="Sale Date", y="Sale Amount",
        color="Year",
        hover_data=['Model'])
    return fig


app.run_server(debug=True)

#############    Last working App    ###############

# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# from datetime import datetime as dt
# import plotly.express as px
#
# car_sales = pd.read_csv('car_sales_clean.csv')
#
# app = Dash(__name__)
#
# app.layout = html.Div([
#     html.H1('Fast & Furious Car Sales'),
#     dcc.Graph(id="scatter-plot"),
#     html.P("Filter by sales Price:"),
#     dcc.RangeSlider(
#         id='range-slider',
#         min=0, max=300000, step=5000,
#         marks={0: '0', 300000: '300,000'},
#         value=[1, 299999]
#     ),
# ])
#
#
# @app.callback(
#     Output("scatter-plot", "figure"),
#     Input("range-slider", "value"))
# def update_bar_chart(slider_range):
#     #df = px.data.iris() # replace with your own data source
#     low, high = slider_range
#     mask = (car_sales['Sale Amount'] > low) & (car_sales['Sale Amount'] < high)
#     fig = px.scatter(
#         car_sales[mask], x="Sale Date", y="Sale Amount",
#         color="Year",
#         hover_data=['Model'])
#     return fig
#
#
# app.run_server(debug=True)
