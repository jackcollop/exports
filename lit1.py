import pandas as pd
import streamlit as st
import os
import numpy as np
import plotly.express as px

key = os.environ['API']

z = pd.read_json(f'https://api.fas.usda.gov/api/esr/countries?api_key={key}')

z.countryDescription = z.countryDescription.str.strip(' ') #formatting: removes excess spacing from country names

zz = z.set_index('countryCode')['countryDescription'].to_dict() #creates dictionary to map country codes to names
#%%
zz[5700] = 'CHINA'
zz[5800] = 'KOREA'

year = 2026
temp = pd.read_json(
        f'https://api.fas.usda.gov/api/esr/exports/commodityCode/1404/allCountries/marketYear/{year}?api_key={key}')
temp['Year'] = str(year - 1)
#%%
upland = pd.concat([temp, pd.read_csv('upland.csv')])

year = 2026
temp = pd.read_json(
    f'https://api.fas.usda.gov/api/esr/exports/commodityCode/1301/allCountries/marketYear/{year}?api_key={key}')
temp['Year'] = str(year - 1)
pima = pd.concat([temp, pd.read_csv('pima.csv')])

upland['countryName'] = upland['countryCode'].map(zz)
pima['countryName'] = pima['countryCode'].map(zz)
#%%

upland['weekEndingDate'] = pd.to_datetime(upland.weekEndingDate)
pima['weekEndingDate'] = pd.to_datetime(pima.weekEndingDate)

xp = upland.pivot(index=['Year','weekEndingDate'], columns='countryName', values='weeklyExports')

xp['TOTAL'] = xp.sum(axis=1)
#%%
weeks = pd.Series(xp.TOTAL.reset_index().groupby('Year').cumcount() + 1).astype(int)
#%%
xp.reset_index(inplace=True)
#%%
xp['week'] = weeks.to_numpy()
#%%
# xp.Year = xp.Year.astype(int)
#%%

xpp = xp.pivot(index='week', columns='Year', values='TOTAL').drop(columns=['2025']).dropna()

fig = px.box(xpp.T)

st.caption('Pace of weekly export shipments')
st.plotly_chart(fig)

upland['Year'] = upland['Year'].astype(int)


xp = upland.pivot(index=['Year','weekEndingDate'], columns='countryName', values='currentMYNetSales')
xp['TOTAL'] = xp.sum(axis=1)
#%%
weeks = pd.Series(xp.TOTAL.reset_index().groupby('Year').cumcount() + 1).astype(int)
#%%
xp.reset_index(inplace=True)
#%%
xp['week'] = weeks.to_numpy()
st.caption('Weekly upland net sales')
st.dataframe(xp.reset_index().set_index(['Year','week'])[['TOTAL','VIETNAM','CHINA','TURKEY','INDONESIA','MEXICO','INDIA','PAKISTAN','KOREA','BANGLADESH','THAILAND','TAIWAN']].sort_index(ascending=False), width='content')

xp = upland.pivot(index=['Year','weekEndingDate'], columns='countryName', values='weeklyExports')
xp['TOTAL'] = xp.sum(axis=1)
#%%
weeks = pd.Series(xp.TOTAL.reset_index().groupby('Year').cumcount() + 1).astype(int)
#%%
xp.reset_index(inplace=True)
#%%
xp['week'] = weeks.to_numpy()
st.caption('Weekly upland shipments')
st.dataframe(xp.reset_index().set_index(['Year','week'])[['TOTAL','VIETNAM','CHINA','TURKEY','INDONESIA','MEXICO','INDIA','PAKISTAN','KOREA','BANGLADESH','THAILAND','TAIWAN']].sort_index(ascending=False), width='content')

xp = upland.pivot(index=['Year','weekEndingDate'], columns='countryName', values='accumulatedExports')

xp['TOTAL'] = xp.sum(axis=1)
#%%
weeks = pd.Series(xp.TOTAL.reset_index().groupby('Year').cumcount() + 1).astype(int)
#%%
xp.reset_index(inplace=True)
#%%
xp['week'] = weeks.to_numpy()
#%%
xp.Year = xp.Year.astype(int)
#%%
xpp = xp.pivot(index='week', columns='Year', values='TOTAL')

fig2 = px.line(xpp[[2021,2022,2023,2024,2025]])
fig2['data'][-1]['line']['width']=5
st.plotly_chart(fig2)

###

fig3 = px.line(xp.reset_index().set_index(['Year','week'])[['VIETNAM','CHINA','TURKEY','INDONESIA','MEXICO','INDIA','PAKISTAN','BANGLADESH','THAILAND']].sort_index(ascending=False).xs(2025))

st.caption('2025 Accumulated Exports by Destination')
st.plotly_chart(fig3)

xp = upland.pivot(index=['Year','weekEndingDate'], columns='countryName', values='outstandingSales')

xp['TOTAL'] = xp.sum(axis=1)
#%%
weeks = pd.Series(xp.TOTAL.reset_index().groupby('Year').cumcount() + 1).astype(int)
#%%
xp.reset_index(inplace=True)
#%%
xp['week'] = weeks.to_numpy()
#%%
xp.Year = xp.Year.astype(int)
#%%
xpp = xp.pivot(index='week', columns='Year', values='TOTAL')

###

fig4 = px.line(xp.reset_index().set_index(['Year','week'])[['VIETNAM','CHINA','TURKEY','INDONESIA','MEXICO','INDIA','PAKISTAN','BANGLADESH','THAILAND']].sort_index(ascending=False).xs(2025).pct_change().dropna())

st.caption('2025 Outstanding Sales by Destination')
st.plotly_chart(fig4)
