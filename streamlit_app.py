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

st.markdown("<h1 style='text-align: center; color: black; '>The Cars of the Fast and Furious Movie Franchise</h1>", unsafe_allow_html=True)

########### SIDEBAR ###################
with st.sidebar.header('Filter Search'):
    movie_list = ['All Movies',"FF1", 'FF2', 'FF3', 'FF4', 'FF6', 'FF7', 'FF8', 'FF9']
    selected_movie= st.sidebar.selectbox('Movie', movie_list)

    if selected_movie != 'All Movies':
        df_update = df[(df['Film Order'].str.contains(selected_movie))]
    else:
        df_update = df

    car_movie=sorted(df_update['Model'].unique())
    selected_car= st.sidebar.multiselect(options=car_movie, label="Select a Car")

    car_movie_df = df_update[(df_update['Model'].isin(selected_car))]
    cm_df = {Model: car_movie_df[car_movie_df["Model"]== Model] for Model in selected_car}




############## MOVIE DATA STATS ###################
movie_data = st.container()
with movie_data:
    st.markdown(f'## Movie Cars Data for {selected_movie}')

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
        colors = sns.color_palette('plasma')
        car_year = df_update.groupby('Year')
        fig, ax = plt.subplots()
        ax.hist(df_update['Year'], bins= 10, color=colors[1], edgecolor='black', linewidth=1)
        ax.set_title('Count of Car Year')
        plt.xlabel('Car Year')

        st.pyplot(fig)


    with col6:
        car_model_stack = df_update.groupby(df_update['Make'])['Year'].value_counts()
        car_model_stack_chart = car_model_stack.unstack()
        colors = sns.color_palette('plasma')
        car_model_stack_chart.plot.bar(stacked=True,)
        plt.xlabel('Car Model Year')
        plt.legend(bbox_to_anchor=(1.05, 1))
        st.pyplot(plt.show(), user_container_width=True)




################## CAR DATA ###################
car_data = st.container()
dfs = {Model: car_sales[car_sales["Model"]== Model] for Model in selected_car}
with car_data:
    st.markdown('## Car Sales Data')
    # st.write(car_movie_df)
    st.subheader("You selected: {}".format(",  ".join(selected_car)))


    # col7, col8 = st.columns(2)
    #
    # with col7:
    #     st.write("column7")
    #     st.write(type(cm_df))
    #     for values in cm_df.values():
    #         st.write(values)
    #
    # with col8:
    #     st.write('column 8')
    #
    #     tot_sales = car_movie_df['Car Sales Count'].values.tolist()
    #     length= len(tot_sales)
    #     for i in range(length):
    #         st.write(f'The total sales were {tot_sales[i]}')


# max_sale = df_update.loc[df['Car Name'] == selected_car]['max'].values
# max_sale_date = df.loc[df['Car Name'] == selected_car]['Max Sale Date'].values
# min_sale = df.loc[df['Car Name'] == selected_car]['min'].values
# min_sale_date = df.loc[df['Car Name'] == selected_car]['Min Sale Date'].values

# st.write(tot_sales)

# dfs = {Model: car_sales[car_sales["Model"]== Model] for Model in selected_car}

fig = go.Figure()
for Model, car_sales in dfs.items():
    fig = fig.add_trace(go.Scatter(x=sorted(car_sales['Sale Date']), y=car_sales['Sale Amount'], name=Model))
st.plotly_chart(fig, use_container_width=True)
plt.cla()

if st.checkbox('Show Sales Data'):
    st.subheader('Sales Data')
    for Model, car_sales in dfs.items():
        st.write(Model, car_sales)

st.markdown(' ')
st.markdown(' ')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df)





