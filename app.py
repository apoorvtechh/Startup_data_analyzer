import streamlit as st
import pandas as pd
df=pd.read_csv('startup_cleaned.csv')
st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    st.title('Overall Analysis')
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Starup Details')
    st.title('Startup Analysis')
else:
    st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].fillna('').astype(str).str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Detail')
    st.title('Inverstor Analysis')