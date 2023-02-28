# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 11:09:40 2023

@author: YOGB
"""
import streamlit as st
import pandas as pd
import openpyxl


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

st.write("# Welcome to WBI Parset interactive dashboard!")
st.markdown(
    """
    Please use this web-app dashboard to visualize and generate geotechnical parameter set.
    """)

col1, col2= st.columns(2)
with col1:
    form1 = st.form(key='master')
    file1 = form1.file_uploader("Upload the master spreadsheet for lab test result here:")
    submit1 = form1.form_submit_button('Upload')

with col2:
    form2 = st.form(key='strati')
    file2 = form2.file_uploader("Upload the WIBO-GINA input spreadsheet here:")
    utm_zone = form2.number_input("UTM zone:", min_value=46, max_value=54)
    utm_hemi = form2.selectbox("UTM hemisphere:", options=["North","South"])
    submit2 = form2.form_submit_button('Upload')

if submit1:
    dflab = pd.read_excel(file1, sheet_name="lab")
    dfcor = pd.read_excel(file1, sheet_name='corr')
    st.session_state['dflab'] = dflab
    st.session_state['dfcor'] = dfcor

if submit2:
    wb = openpyxl.load_workbook(file2, data_only=True)
    st.session_state['wb'] = wb
    st.session_state['utmz'] = utm_zone
    st.session_state['utmh'] = utm_hemi
