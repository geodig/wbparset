# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:18:07 2023

@author: YOGB
"""
import streamlit as st
import plotly.express as px
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="wibopargen"
                    ,layout="wide"
                   )

add_logo("https://climateapp.nl/img/about/logo-witteveenbos.png")


dflab = st.session_state['dflab']
dfcor = st.session_state['dfcor']

numcols = st.number_input("Select number of charts:", min_value=1, max_value=3)

col1, col2, col3 = st.columns(3)

with col1:
    dfselect = col1.selectbox("Select dataframe:", options=["lab data","correlation"])
    if dfselect == "lab data":
        df = dflab
    elif dfselect == "correlation":
        df = dfcor
    
    col1a, col1b, col1c = col1.columns(3)
    x_axis_val = col1a.selectbox('Select the X-axis', options=df.columns)
    y_axis_val = col1b.selectbox('Select the Y-axis', options=df.columns)
    col_val = col1c.selectbox('Select the color axis', options=df.columns)
    
    plot = px.scatter(df, x=x_axis_val, y=y_axis_val, color=col_val, height = 700, width = 600)
    plot.update_xaxes(showgrid=True)
    plot.update_yaxes(showgrid=True)
    col1.plotly_chart(plot, use_container_width=True)
    
if numcols == 2:
    with col2:
        dfselect2 = col2.selectbox("Select dataframe:", options=["lab data","correlation"], key="2")
        if dfselect2 == "lab data":
            df2 = dflab
        elif dfselect2 == "correlation":
            df2 = dfcor
        col2a, col2b, col2c = col2.columns(3)
        x_axis_val2 = col2a.selectbox('Select the X-axis', options=df2.columns, key="3")
        y_axis_val2 = col2b.selectbox('Select the Y-axis', options=df2.columns, key="4")
        col_val2 = col2c.selectbox('Select the color axis', options=df2.columns, key="5")
        
        plot2 = px.scatter(df2, x=x_axis_val2, y=y_axis_val2, color=col_val2, height = 700, width = 600)
        plot2.update_xaxes(showgrid=True)
        plot2.update_yaxes(showgrid=True)
        col2.plotly_chart(plot2, use_container_width=True)
        
if numcols == 3:
    with col2:
        dfselect2 = col2.selectbox("Select dataframe:", options=["lab data","correlation"], key="2")
        if dfselect2 == "lab data":
            df2 = dflab
        elif dfselect2 == "correlation":
            df2 = dfcor
        col2a, col2b, col2c = col2.columns(3)
        x_axis_val2 = col2a.selectbox('Select the X-axis', options=df2.columns, key="3")
        y_axis_val2 = col2b.selectbox('Select the Y-axis', options=df2.columns, key="4")
        col_val2 = col2c.selectbox('Select the color axis', options=df2.columns, key="5")
        
        plot2 = px.scatter(df2, x=x_axis_val2, y=y_axis_val2, color=col_val2, height = 700, width = 600)
        plot2.update_xaxes(showgrid=True)
        plot2.update_yaxes(showgrid=True)
        col2.plotly_chart(plot2, use_container_width=True)
    with col3:
        dfselect3 = col3.selectbox("Select dataframe:", options=["lab data","correlation"], key="6")
        if dfselect3 == "lab data":
            df3 = dflab
        elif dfselect3 == "correlation":
            df3 = dfcor
        col3a, col3b, col3c = col3.columns(3)
        x_axis_val3 = col3a.selectbox('Select the X-axis', options=df3.columns, key="7")
        y_axis_val3 = col3b.selectbox('Select the Y-axis', options=df3.columns, key="8")
        col_val3 = col3c.selectbox('Select the color axis', options=df3.columns, key="9")
        
        plot3 = px.scatter(df3, x=x_axis_val3, y=y_axis_val3, color=col_val3, height = 700, width = 600)
        plot3.update_xaxes(showgrid=True)
        plot3.update_yaxes(showgrid=True)
        col3.plotly_chart(plot3, use_container_width=True)
