import pandas as pd
import streamlit as st
import numpy as np

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

def update_statistics(input_movie):
    if input_movie == None:
        df_update = df
        # avg_car_sale = round(car_sales['Sale Amount'].mean(), ndigits=0)
        # car_options = sorted(df['Car Name'].unique())
    else:
        df_update = df[(df['Film Order'].str.contains(input_movie))]
        avg_car_sale = round(df_update['mean'].mean(), ndigits=0)
        car_options = [{'label': i, 'value': i} for i in df_update['Car Name']]


    maj = df_update.Role.str.contains('Major').sum()
    minor = df_update.Role.str.contains('Minor').sum()

    return len(df_update), f'{maj} vs {minor}', round(df_update['Year'].mean(), ndigits=0), avg_car_sale, car_options

#########callback for car stats#########

def update_car_stats(car_input):
    if car_input == None:
        return 0
    else:
        tot_sales = df.loc[df['Car Name'] == car_input]['Car Sales Count'].values
        max_sale = df.loc[df['Car Name'] == car_input]['max'].values
        max_sale_date = df.loc[df['Car Name'] == car_input]['Max Sale Date'].values
        min_sale = df.loc[df['Car Name'] == car_input]['min'].values
        min_sale_date = df.loc[df['Car Name'] == car_input]['Min Sale Date'].values

    return tot_sales, (f"{np.array2string(max_sale, formatter={'float': lambda x: f'{x:,}'}, separator=', ').strip('[]')}"), (f"{np.array2string(max_sale_date, formatter={'date': lambda x: f'{x:}'}, separator=', ').strip('[]')}"), (f"{np.array2string(min_sale, formatter={'float': lambda x: f'{x:,}'}, separator=', ').strip('[]')}"), (f"{np.array2string(min_sale_date, formatter={'date': lambda x: f'{x:}'}, separator=', ').strip('[]')}")


##### callback for  year radio button#######

def set_year_value(car_dropdown):
    if car_dropdown == None:
        available_options = df['Year'].unique()
    else:
        available_options = df.loc[df['Car Name'] == car_dropdown]['Year'].values

    return available_options



###### Callback for Car specific scatter chart ######

def update_car_chart(car_selection):
    cars = df[df["Car Name"] == car_selection]['Model']
    #print(cars)
    df_update = car_sales[(car_sales['Model'].isin(cars))]
    df_update = df_update.sort_values(["Sale Date"]).reset_index(drop=True)


    # fig2 = px.scatter(df_update, x="Sale Date", y="Sale Amount", color="Year", hover_data=['Model'])
    # fig2.update_layout(yaxis_range=[0, 300000])

    line_chart = px.line(
        data_frame=df_update,
        x='Sale Date',
        y='Sale Amount',
        color='Year',
        labels={'Model': 'Car', 'Sale Date': 'Date'},
    )
    return(line_chart)


######### Callback for scatter chart ##############################

def update_bar_chart(slider_range):
    low, high = slider_range
    mask = (car_sales['Sale Amount'] > low) & (car_sales['Sale Amount'] < high)
    fig = px.scatter(
        car_sales[mask], x="Sale Date", y="Sale Amount",
        color="Year",
        hover_data=['Model'])
    return fig