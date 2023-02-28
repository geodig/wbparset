# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:18:07 2023

@author: YOGB
"""
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="WBI Parset"
                    ,layout="wide"
                   )

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://climateapp.nl/img/about/logo-witteveenbos.png);
                background-repeat: no-repeat;
                padding-top: 10px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()



dflab = st.session_state['dflab']
dfcor = st.session_state['dfcor']

numcols = st.number_input("Select number of charts:", min_value=1, max_value=2)

col1, col2 = st.columns(2)

if numcols == 1:
    with col1:
        dfselect = col1.selectbox("Select dataframe:", options=["lab data","correlation"])
        if dfselect == "lab data":
            df = dflab
        elif dfselect == "correlation":
            df = dfcor
        
        col3, col4, col5 = col1.columns(3)
        x_axis_val = col3.selectbox('Select the X-axis', options=df.columns)
        y_axis_val = col4.selectbox('Select the Y-axis', options=df.columns)
        col_val = col5.selectbox('Select the color axis', options=df.columns)
        
        plot = px.scatter(df, x=x_axis_val, y=y_axis_val, color=col_val, height = 600, width = 600)
        plot.update_xaxes(showgrid=True)
        plot.update_yaxes(showgrid=True)
        col1.plotly_chart(plot, use_container_width=True)
    
elif numcols == 2:
    with col1:
        dfselect = col1.selectbox("Select dataframe:", options=["lab data","correlation"])
        if dfselect == "lab data":
            df = dflab
        elif dfselect == "correlation":
            df = dfcor
        col3, col4, col5 = col1.columns(3)
        x_axis_val = col3.selectbox('Select the X-axis', options=df.columns)
        y_axis_val = col4.selectbox('Select the Y-axis', options=df.columns)
        col_val = col5.selectbox('Select the color axis', options=df.columns)
        
        plot = px.scatter(df, x=x_axis_val, y=y_axis_val, color=col_val, height = 600, width = 600)
        plot.update_xaxes(showgrid=True)
        plot.update_yaxes(showgrid=True)
        col1.plotly_chart(plot, use_container_width=True)
    with col2:
        dfselect2 = col2.selectbox("Select dataframe:", options=["lab data","correlation"], key="2")
        if dfselect2 == "lab data":
            df2 = dflab
        elif dfselect2 == "correlation":
            df2 = dfcor
        col6, col7, col8 = col2.columns(3)
        x_axis_val2 = col6.selectbox('Select the X-axis', options=df2.columns, key="3")
        y_axis_val2 = col7.selectbox('Select the Y-axis', options=df2.columns, key="4")
        col_val2 = col8.selectbox('Select the color axis', options=df2.columns, key="5")
        
        plot2 = px.scatter(df2, x=x_axis_val2, y=y_axis_val2, color=col_val2, height = 600, width = 600)
        plot2.update_xaxes(showgrid=True)
        plot2.update_yaxes(showgrid=True)
        col2.plotly_chart(plot2, use_container_width=True)