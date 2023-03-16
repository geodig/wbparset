# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 09:39:13 2023

@author: YOGB
"""
import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="wibopargen"
                    ,layout="wide"
                   )

add_logo("https://climateapp.nl/img/about/logo-witteveenbos.png")


dflab = st.session_state['dflab']
dfcor = st.session_state['dfcor']
dfstrati = st.session_state["dfstrati"] 
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
    df = dflab[dflab["Stratigraphy [-]"]==strati]
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
            "5% percentile":[perc],
            "# samples":[len(value)]}
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
    df = dfcor[dfcor["Stratigraphy [-]"]==strati]
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
            "5% percentile":[perc],
            "# samples":[len(value)]}
        df_output = pd.DataFrame(output)
        st.write(df_output)

if dfstrati.empty:
    pass
else:
    strati_list2 = strati_list.insert(0,"parameter unit")
    recap = {
        "Stratigraphy":strati_list,
        "gamma_sat":[None]*(strati_n+1),
        "CR":[None]*(strati_n+1),
        "RR":[None]*(strati_n+1),
        "Ca":[None]*(strati_n+1),
        "cv":[None]*(strati_n+1),
        "POP":[None]*(strati_n+1),
        "OCR":[None]*(strati_n+1),
        "c'":[None]*(strati_n+1),
        "phi'":[None]*(strati_n+1),
        "cu":[None]*(strati_n+1)
        }
    
    df_rec = pd.DataFrame(recap)
    df_rec2 = st.experimental_data_editor(df_rec, use_container_width=True)
    
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df_rec2)
    
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='parset.csv',
        mime='text/csv',
    )
