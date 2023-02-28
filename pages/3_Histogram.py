# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:39:13 2023

@author: YOGB
"""
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

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
wb = st.session_state['wb']
sh = wb["stratigraphy"]
strati_n = sh.max_row - 1
strati_list = []
for i in range(strati_n):
    strati_list.append(sh.cell(i+2,1).value)

col1, col2 = st.columns(2)

with col1:
    st.markdown("## Lab test set")
    paramlist = dflab.columns.tolist()
    paramlist = paramlist[11:]
    paramlist.append("NSPT")
    strati = st.selectbox('Select stratigraphy:', options=strati_list, key="sb1")
    param = st.selectbox("Select parameters:", options=paramlist, key="sb2")
    nbin = st.slider("Number of bins:", min_value=5, max_value=30, key="sl1")
    df = dflab[dflab["Stratigraphy"]==strati]
    fig = px.histogram(df, x=param, nbins=nbin, height = 400, width = 400)
    col1a,col1b = col1.columns(2)
    with col1a:
        st.plotly_chart(fig)
    with col1b:
        value = df[param].tolist()
        value = [i for i in value if ~np.isnan(i)]
        value = [float(i) for i in value]
        st.markdown("#### Statistics:")
        perc = df[param].quantile(0.05)
        output = {
            "Mean":[np.average(value)],
            "5% percentile":[perc]}
        df_output = pd.DataFrame(output)
        st.write(df_output)
        
with col2:
    st.markdown("## Correlation set")
    paramlist = dfcor.columns.tolist()
    paramlist = paramlist[11:]
    paramlist.append("NSPT")
    strati = st.selectbox('Select stratigraphy:', options=strati_list, key="sb3")
    param = st.selectbox("Select parameters:", options=paramlist, key="sb4")
    nbin = st.slider("Number of bins:", min_value=5, max_value=30, key="sl2")
    df = dfcor[dfcor["Stratigraphy"]==strati]
    fig = px.histogram(df, x=param, nbins=nbin, height = 400, width = 400)
    col2a,col2b = col2.columns(2)
    with col2a:
        st.plotly_chart(fig)
    with col2b:
        value = df[param].tolist()
        value = [i for i in value if ~np.isnan(i)]
        value = [float(i) for i in value]
        st.markdown("#### Statistics:")
        perc = df[param].quantile(0.05)
        output = {
            "Mean":[np.average(value)],
            "5% percentile":[perc]}
        df_output = pd.DataFrame(output)
        st.write(df_output)

recap = {
    "Stratigraphy":strati_list,
    "gamma_sat":[0.00]*strati_n,
    "CR":[0.00]*strati_n,
    "RR":[0.00]*strati_n,
    "Ca":[0.00]*strati_n,
    "cv":[0.00]*strati_n,
    "c'":[0.00]*strati_n,
    "phi'":[0.00]*strati_n,
    "cu":[0.00]*strati_n
    }


df_rec = pd.DataFrame(recap)
df_rec2 = st.experimental_data_editor(df_rec, use_container_width=True)
