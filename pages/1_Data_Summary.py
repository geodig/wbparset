# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:17:29 2023

@author: YOGB
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

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

st.markdown("# Lab test result table")
st.dataframe(dflab)
st.markdown("# Correlation table")
st.dataframe(dfcor)

bh_list = dflab['Borehole'].unique().tolist()

# st.write(bh_list)

sh = wb["stratigraphy"]
strati_n = sh.max_row - 1
strati_list = []
for i in range(strati_n):
    strati_list.append(sh.cell(i+2,1).value)

head = []
for i in range(sh.max_column):
    head.append(sh.cell(1,i+1).value)

strati = []
for i in range(len(dflab)):
    head_index = head.index(dflab["Borehole"].iloc[i])
    sample_depth = dflab["Depth"].iloc[i]
    strati_depth, val = [],[]
    for j in range(strati_n):
        strati_depth.append(sh.cell(j+2,head_index+1).value)
        if sample_depth < strati_depth[j]:
            val.append(0)
        elif sample_depth > strati_depth[j]:
            val.append(1)
    strati_index = np.sum(val)
    if strati_index == strati_n:
        strati_index = strati_n-1
    strati.append(strati_list[strati_index])

dflab["Stratigraphy"] = strati
dfcor["Stratigraphy"] = strati

st.markdown("# Grain size distribution bar chart")
select = st.selectbox("Select a strati unit:", options=strati_list)
dflab2 = dflab[dflab["Stratigraphy"]==select]

label = ["clay","silt","sand","gravel"]
color = ["turquoise","lightcoral","gold","silver"]

xdata, ydata = [],[]
for i in range(0,len(dflab2)):
    xdata.append([dflab2["Clay"].iloc[i],dflab2["Silt"].iloc[i],dflab2["Sand"].iloc[i],dflab2["Gravel"].iloc[i]])
    # xdata.append([dflab2["Clay"].iloc[i]])
    ydata.append("%s, depth %.1f m"%(dflab2["Borehole"].iloc[i],dflab2["Depth"].iloc[i]))

# st.write(len(dflab2))

fig = go.Figure()

for i in range(4):
    for xd, yd in zip(xdata, ydata):
        fig.add_trace(go.Bar(
            x=[xd[i]], y=[yd],
            orientation='h',
            marker=dict(
                color=color[i],
                line=dict(color="rgba(0,0,0,0)", width=1)
            )
        ))

fig.update_layout(
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
        domain=[0.15, 1]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        zeroline=False,
    ),
    barmode='stack',
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    # margin=dict(l=120, r=10, t=140, b=80),
    showlegend=False,
)

st.plotly_chart(fig)



















