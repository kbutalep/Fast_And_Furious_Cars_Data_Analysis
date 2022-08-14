import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.express as px

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

input_movie =input('> ')

def update_statistics(input_movie):

    #df_update = df[(df['Film Order'].str.contains(input_movie))]
   #maj = df_update[(df_update['Role'].str.contains('Major'))].value_counts()
   # maj = df_update.Role.str.contains('Major').sum()
    avg_car_sale1 = round(car_sales['Sale Amount'].mean(), ndigits=0)
    avg_car_sale2 = round(df['mean'].mean(), ndigits=0)

    #print(len(df_update))

    print(avg_car_sale1)
    print(avg_car_sale2)

update_statistics(input_movie)
