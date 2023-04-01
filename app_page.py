# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import cufflinks as cf
import yfinance  as yf
import pandas    as pd
import streamlit as st
import locale
import strConstants as sc

import requests
import json
import os
import time

token = 'HO9XL9Anh7yI9cXLcv1xGoy4LsSA'
base = 'https://api.tradier.com/v1'
section = '/markets'

def GET_Quotes(symbol,
                     urlSubsectionText):
    resp = requests.get(base + section + urlSubsectionText,
                        params = {'symbols':symbol},
                        headers= {'Authorization':'Bearer '+token,'Accept':'application/json'}
                        )
    j = json.loads(resp.content)
    #jf = json.dumps(j,indent=2)
    return j['quotes']['quote']

aaa = GET_Quotes('msft', '/quotes')
    

locale.setlocale(locale.LC_ALL, '')

st.set_page_config(
     page_title="draft finance",
     layout="wide"
     )


# from streamlit_autorefresh import st_autorefresh
# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
#count = st_autorefresh(interval=20000, limit=5, key="fizzbuzzcounter")

cf.set_config_file(theme='space')


#st.markdown(sc.getCodeSnippet('reduceItemPadding'), unsafe_allow_html=True)
st.markdown(sc.getCodeSnippet('sidebarWidth'), unsafe_allow_html=True)
st.markdown(sc.getCodeSnippet('hideStreamlitStyle'), unsafe_allow_html=True)
st.markdown(sc.getCodeSnippet('adjustPaddingAndFont'), unsafe_allow_html=True)

with st.sidebar:
    searchTicker = st.text_input('Search Ticker:',value='MSFT').upper()
    searchPeriod = st.radio('Period:', ('1mo','3mo','6mo','1y'),index=2)
symb = yf.Ticker(searchTicker)
stockCurrent = GET_Quotes(searchTicker, '/quotes')
if stockCurrent['change'] > 0:
    posneg = '+'
elif stockCurrent['change'] < 0:
    posneg = '-'
else:
    posneg = ''

searchName = stockCurrent['description']
latestClose = stockCurrent['last']
posnegChange = posneg + ' $' + str(stockCurrent['change'])
                
# latestTime = symb.history(period='1d',interval='1m').index.max()
priorClose = stockCurrent['prevclose']
todayPctChange = str(stockCurrent['change_percentage']) + '%'
latestCloseNoD = str(latestClose)
latestClose = '$' + str(latestClose)

# with st.sidebar:
#     st.markdown(f'Last updated: {latestTime}')

st.markdown(f'## {searchName} \n  ## {latestClose}')
st.markdown(' ')
st.markdown(f'⠀{posnegChange} ({todayPctChange})')

#### Historical Price Action
df = symb.history(period=searchPeriod, 
                  interval='1d', 
                  group_by='ticker',
                  auto_adjust=True)
qf = cf.QuantFig(df, 
                 title=searchPeriod + ' Lookback', 
                 legend='top', 
                 name=searchTicker)
qf.add_bollinger_bands()
qf.add_volume()
qfpl = qf.iplot(asFigure=True,
                up_color='green',
                down_color='red')
qfpl.update_xaxes(rangebreaks=[dict(bounds=['sat','mon'])])

st.plotly_chart(qfpl, use_container_width=True)

col1, col2 = st.columns([1,1])
with col1:
    ### Current Day Price Action
    dfv = symb.history(period='1d',
                       interval='5m',
                       group_by='ticker',
                       auto_adjust=True)
    qfv = cf.QuantFig(dfv, 
                      title='Today', 
                      legend='top', 
                      name=searchTicker)
    qfv.add_volume()#layout={'yaxis': {'showticklabels': False}})
    qfvpl = qfv.iplot(asFigure=True,up_color='green',down_color='red')
    qfvpl.update_layout(
        autosize=False,
        height=200,
        yaxis3=dict(showticklabels=False,showgrid=False))
    
    st.plotly_chart(qfvpl, use_container_width=True)
