import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.express as px

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

input_movie =input('> ')

def update_statistics(input_movie):

    df_update = df[(df['Film Order'].str.contains(input_movie))]

    print(len(df_update))
    print(df_update.columns)

update_statistics(input_movie)