from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.express as px

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div(children=[
            html.H3(children='Fast and Furious Cars Data'),
            html.H6(children='Cars from the Fast & Furious Movie Franchise', style={'marginTop': '-15px', 'marginBottom': '30px'})
        ], style={'textAlign': 'center'}
     ),

html.Div(children=[
    ################### Filter box ######################
    html.Div(children=[
    html.Label('Filter by date (M-D-Y):'),
    dcc.DatePickerRange(
         id='input_date',
        month_format='DD/MM/YYYY',
            show_outside_days=True,
            minimum_nights=0,
            initial_visible_month=dt(2017, 1, 1),
            min_date_allowed=dt(2016, 1, 1),
            max_date_allowed=dt(2018, 12, 31),
            start_date=dt.strptime("2018-06-01", "%Y-%m-%d").date(),
            end_date=dt.strptime("2018-12-31", "%Y-%m-%d").date()
        ),

        html.Label('Day of the week:', style={'paddingTop': '2rem'}),
        dcc.Dropdown(
            id='input_days',
            options=[
                {'label': 'Sun', 'value': '1'},
                {'label': 'Mon', 'value': '2'},
                {'label': 'Tue', 'value': '3'},
                {'label': 'Wed', 'value': '4'},
                {'label': 'Thurs', 'value': '5'},
                {'label': 'Fri', 'value': '6'},
                {'label': 'Sat', 'value': '7'}
            ],
            value=['1', '2', '3', '4', '5', '6', '7'],
            multi=True
        ),

        html.Label('Accident Severity:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
        dcc.Checklist(
            id='input_acc_sev',
            options=[
                {'label': 'Fatal', 'value': '1'},
                {'label': 'Serious', 'value': '2'},
                {'label': 'Slight', 'value': '3'}
            ],
            value=['1', '2', '3'],
        ),

        html.Label('Speed limits (mph):', style={'paddingTop': '2rem'}),
        dcc.RangeSlider(
                id='input_speed_limit',
                min=20,
                max=70,
                step=10,
                value=[20, 70],
                marks={
                    20: '20',
                    30: '30',
                    40: '40',
                    50: '50',
                    60: '60',
                    70: '70'
                },
        ),

    ], className="four columns",
    style={'padding':'2rem', 'margin':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem'}),

    ##### HERE insert the code for four boxes & graph #########
    # Number statistics & number of accidents each day

html.Div(children=[
     html.Div(children=[
         html.Div(children=[
                html.H3(id='no_acc', style={'fontWeight': 'bold'}),
                html.Label('Total accidents', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='no_cas', style={'fontWeight': 'bold', 'color': '#f73600'}),
                html.Label('Casualties', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='no_veh', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                html.Label('Total vehicles', style={'paddingTop': '.3rem'}),
            ], className="three columns number-stat-box"),

            html.Div(children=[
                html.H3(id='no_days', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                html.Label('Number of days', style={'paddingTop': '.3rem'}),

            ], className="three columns number-stat-box"),
        ], style={'margin': '1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%',
                  'flex-wrap': 'wrap'}),

        # Line chart for accidents per day
        html.Div(children=[
            dcc.Graph(id='acc_line_chart')
        ], className="twleve columns",
            style={'padding': '.3rem', 'marginTop': '1rem', 'marginLeft': '1rem', 'boxShadow': '#e3e3e3 4px 4px 2px',
                   'border-radius': '10px', 'backgroundColor': 'white', }),

    ], className="eight columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'})

])
])



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