from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

car_sales = pd.read_csv('car_sales_clean.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Fast & Furious Car Sales'),
    dcc.Graph(id="scatter-plot"),
    html.P("Filter by sales Price:"),
    dcc.RangeSlider(
        id='range-slider',
        min=0, max=300000, step=5000,
        marks={0: '0', 300000: '300,000'},
        value=[1, 299999]
    ),
])


@app.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"))
def update_bar_chart(slider_range):
    #df = px.data.iris() # replace with your own data source
    low, high = slider_range
    mask = (car_sales['Sale Amount'] > low) & (car_sales['Sale Amount'] < high)
    fig = px.scatter(
        car_sales[mask], x="Sale Date", y="Sale Amount",
        color="Year",
        hover_data=['Model'])
    return fig


app.run_server(debug=True)



# app = Dash(__name__)
#
#
# app.layout = html.Div([
#     html.H4('Fast & Furious Cars Sales Data'),
#     html.P("Select car"),
#     dcc.Dropdown(
#         id="dropdown",
#         options=['Gold', 'MediumTurquoise', 'LightGreen'],
#         value='Gold',
#         clearable=False,
#     ),
#     dcc.Graph(id="graph"),
# ])
#
#
# @app.callback(
#     Output("graph", "figure"),
#     Input("dropdown", "value"))
# def display_color(color):
#     fig = go.Figure(
#         data=go.Bar(y=[2, 3, 1], # replace with your own data source
#                     marker_color=color))
#     return fig
#
#
# app.run_server(debug=True)