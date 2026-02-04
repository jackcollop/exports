import pandas as pd
import streamlit as st
import os

key = os.environ['API']

z = pd.read_json(f'https://api.fas.usda.gov/api/esr/countries?api_key={key}')

st.dataframe(z)
