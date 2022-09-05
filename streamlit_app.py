import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
import plotly.express as px
import matplotlib.dates as mdates
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from utils import *

st.set_page_config(layout="wide", page_title="Fast and Furious Car Analysis")
st.set_option('deprecation.showPyplotGlobalUse', False)

car_sales = pd.read_csv('car_sales_clean.csv')
df = pd.read_csv('ff_cars_clean.csv')

st.title("# Fast and Furious Site Remake")

########### SIDEBAR ###################
with st.sidebar.header('Filter Search'):
    movie_list = ['All Movies',"FF1", 'FF2', 'FF3', 'FF4', 'FF6', 'FF7', 'FF8', 'FF9']
    selected_movie= st.sidebar.selectbox('Movie', movie_list)

    if selected_movie != 'All Movies':
        df_update = df[(df['Film Order'].str.contains(selected_movie))]
    else:
        df_update = df

    car_movie=sorted(df_update['Car Name'].unique())
    selected_car= st.sidebar.multiselect(options=car_movie, label="Select a Car")

    car_movie_df = df_update[(df_update['Car Name'].isin(selected_car))]

    # brand = st.sidebar.selectbox('Select Brand', df.Make.unique())
    # model = st.sidebar.multiselect('Select your model', df.loc[df.Make == brand]['Model'].unique())

############## MOVIE DATA STATS ###################
movie_data = st.container()
with movie_data:
    st.markdown(f'## Movie Data for {selected_movie}')

    avg_car_sale = round(df_update['mean'].mean(), ndigits=0)
    maj = df_update.Role.str.contains('Major').sum()
    minor = df_update.Role.str.contains('Minor').sum()
    total_cars = len(df_update)
    mvm = f'{maj} vs {minor}'
    avg_year = round(df_update['Year'].mean(), ndigits=0)


    # with open('style.css') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Cars", total_cars)
    col2.metric("Major vs. Minor Car", mvm)
    col3.metric("Average Car Model Year", '{:.0f}'.format(avg_year))
    col4.metric("Mean Car Sales", '{:,.0f}'.format(avg_car_sale))

    col5, col6 = st.columns(2)
    with col5:
        car_year_stack = df_update.groupby(df_update['Year'])['Make'].value_counts()
        car_year_stack_chart=car_year_stack.unstack()
        colors=sns.color_palette('plasma')
        car_year_stack_chart.plot.bar(stacked=True, color=colors)
        plt.xlabel('Car Model Year')
        plt.legend(bbox_to_anchor=(1.05,1))
        st.pyplot(plt.show(), user_container_width=True)

    with col6:
        car_model_stack = df_update.groupby(df_update['Make'])['Year'].value_counts()
        car_model_stack_chart = car_model_stack.unstack()
        colors = sns.color_palette('plasma')
        car_model_stack_chart.plot.bar(stacked=True, color=colors)
        plt.xlabel('Car Model Year')
        plt.legend(bbox_to_anchor=(1.05, 1))
        st.pyplot(plt.show(), user_container_width=True)

# car_year = df_update.groupby('Year')
# fig, ax = plt.subplots()
# ax.hist(df_update['Year'], bins= 10)
# plt.xlabel('Car Year')
# # df_update['Year'].plot.hist(color='green', title= 'car year', bins = [1960, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2022], rwidth=0.7)
# st.pyplot(fig)


################## CAR DATA ###################
car_data = st.container()

with car_data:
    st.markdown('## Car Data')
    st.write(car_movie_df)
    st.write(car_movie_df['Car Name'].unique())


# tot_sales = car_movie_df.loc[car_movie_df['Car Name'] == selected_car]['Car Sales Count'].values
# max_sale = df_update.loc[df['Car Name'] == selected_car]['max'].values
# max_sale_date = df.loc[df['Car Name'] == selected_car]['Max Sale Date'].values
# min_sale = df.loc[df['Car Name'] == selected_car]['min'].values
# min_sale_date = df.loc[df['Car Name'] == selected_car]['Min Sale Date'].values

# st.write(tot_sales)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)





