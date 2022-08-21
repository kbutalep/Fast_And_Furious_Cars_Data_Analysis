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
   #  avg_car_sale1 = round(car_sales['Sale Amount'].mean(), ndigits=0)
   #  avg_car_sale2 = round(df['mean'].mean(), ndigits=0)
    #print(df[df['Make'] == 'Corvette Sting Ray']['max'].item())

    print(df[df['Car Name'] == 'Nissan Skyline GT-R R33'][0].values[0])



    # cars = df[df["Car Name"] == ['Nissan Skyline GT-R R33', 'Corvette Sting Ray']]['Model']
    # print(cars)
    #
    # df_update = car_sales[(car_sales['Model'].isin(cars))]
    # print(df_update)
    #
    # df_update = df_update.sort_values(["Sale Date"]).reset_index(drop=True)
    # print(df_update)

    #print((f"{np.array2string(max_sale_date, formatter={'date': lambda x: f'{x:}'}, separator=', ').strip('[]')}"))

    #(f"{np.array2string(max_car, formatter={'float': lambda x: f'{x:,}'}, separator=', ').strip('[]')}")
    #print(df.query('Make' == 'Corvette Sting Ray')['max'])

    #print(len(df_update))

    #

update_statistics(input_movie)
