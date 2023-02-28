# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:10:05 2023

@author: YOGB
"""
import folium
from streamlit_folium import st_folium
import streamlit as st
import utm
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

st.write("# Borehole/CPT Location")

# SESSION STATE ===============================================================
wb = st.session_state['wb']
utm_zone = st.session_state['utmz'] 
utm_hemi = st.session_state['utmh']

# READING INPUT SPREADSHEET ===================================================
sheet_bhmgr = wb['borehole_manager']
sheet_cptmgr = wb['cpt_manager']

BH_n = sheet_bhmgr.max_row - 1
BH_ID,BH_X,BH_Y,BH_Z,BH_GWL,BH_cat = [],[],[],[],[],[]
for i in range(BH_n):
    BH_ID.append(sheet_bhmgr.cell(i+2,2).value)
    BH_X.append(sheet_bhmgr.cell(i+2,3).value)
    BH_Y.append(sheet_bhmgr.cell(i+2,4).value)
    BH_Z.append(sheet_bhmgr.cell(i+2,5).value)
    BH_GWL.append(sheet_bhmgr.cell(i+2,6).value)
    BH_cat.append("BH")

BH_X = np.array(BH_X)
BH_Y = np.array(BH_Y)
BH_Z = np.array(BH_Z)
BH_GWL = np.array(BH_GWL)
BH_ID = np.array(BH_ID)
BH_cat = np.array(BH_cat)

CPT_n = sheet_cptmgr.max_row - 1
CPT_ID, CPT_X, CPT_Y, CPT_Z, CPT_GWL, CPT_cat = [],[],[],[],[],[]
for i in range(CPT_n):
    CPT_ID.append(sheet_cptmgr.cell(i+2,2).value)
    CPT_X.append(sheet_cptmgr.cell(i+2,3).value)
    CPT_Y.append(sheet_cptmgr.cell(i+2,4).value)
    CPT_Z.append(sheet_cptmgr.cell(i+2,5).value)
    CPT_GWL.append(sheet_cptmgr.cell(i+2,6).value) 
    CPT_cat.append("CPT")

CPT_X = np.array(CPT_X)
CPT_Y = np.array(CPT_Y)
CPT_Z = np.array(CPT_Z)
CPT_GWL = np.array(CPT_GWL)
CPT_ID = np.array(CPT_ID)
CPT_cat = np.array(CPT_cat)

ALL_X = np.concatenate((BH_X, CPT_X))
ALL_Y = np.concatenate((BH_Y, CPT_Y))
ALL_Z = np.concatenate((BH_Z, CPT_Z))
ALL_GWL = np.concatenate((BH_GWL, CPT_GWL))
ALL_ID = np.concatenate((BH_ID, CPT_ID))
ALL_cat = np.concatenate((BH_cat, CPT_cat))

ALL_X = [i for i in ALL_X if i != None]
ALL_Y = [i for i in ALL_Y if i != None]
ALL_Z = [i for i in ALL_Z if i != None]
ALL_GWL = [i for i in ALL_GWL if i != None]
ALL_ID = [i for i in ALL_ID if i != None]
ALL_cat = [i for i in ALL_cat if i != None]

data = {'ID' : ALL_ID,
        'X_UTM' : ALL_X,
        'Y_UTM' : ALL_Y,
        'Z' : ALL_Z,
        'GWL' : ALL_GWL,
        'CLASS' : ALL_cat}

df = pd.DataFrame(data)

latlon, lat, lon = [],[],[]
for i in range(len(ALL_X)):
    #print(df['ID'].iloc[i])
    if utm_hemi == 'North':
        hemis = True
    elif utm_hemi == 'South':
        hemis = False
    latlon.append(utm.to_latlon(ALL_X[i], ALL_Y[i], utm_zone, northern=hemis))
    lat.append(latlon[i][0])
    lon.append(latlon[i][1])

df['lat']=lat
df['lon']=lon

latmean = df['lat'].mean()
lonmean = df['lon'].mean()
location = [latmean, lonmean]
m = folium.Map(location=location, zoom_start=16
                , tiles="CartoDB positron"
               )

icons = []
for i in range(0,len(df)):
    if df['CLASS'].iloc[i] == "BH":
        icons.append(folium.Icon(color='blue'))
    elif df['CLASS'].iloc[i] == "CPT":
        icons.append(folium.Icon(color='red'))

for i in range(0,len(df)):
    folium.Marker([df['lat'].iloc[i], df['lon'].iloc[i]], popup=df['ID'].iloc[i], icon=icons[i]).add_to(m)

output = st_folium(m, width=1400, height=600)