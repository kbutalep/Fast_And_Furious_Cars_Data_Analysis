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

    max_sale_date = pd.DataFrame(df.loc[df['Car Name'] == "Ford GT40"]['Max Sale Date'].values)
    max_sale_format = max_sale_date.to_string()


    print(max_sale_format)

    #print((f"{np.array2string(max_sale_date, formatter={'date': lambda x: f'{x:}'}, separator=', ').strip('[]')}"))

    #(f"{np.array2string(max_car, formatter={'float': lambda x: f'{x:,}'}, separator=', ').strip('[]')}")
    #print(df.query('Make' == 'Corvette Sting Ray')['max'])

    #print(len(df_update))

    #

update_statistics(input_movie)
