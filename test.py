
import pandas as pd


car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

input_movie =input('> ')

def update_statistics(input_movie):



    print(len(df['Car Name'].unique()))


update_statistics(input_movie)
