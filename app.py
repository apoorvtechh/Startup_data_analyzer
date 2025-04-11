import streamlit as st
import pandas as pd
df=pd.read_csv('startup_cleaned.csv')


def load_investor_detail(investor):
    st.title(investor)
    #loading recent five recent investment of the investor
    last5df=df[df['investors'].str.contains(investor, na=False)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5df)
    #biggest investment by investor
    big_df=df[df['investors'].str.contains(investor,na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False)
    st.subheader('Biggest Investments')
    st.dataframe(big_df)

st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    st.title('Overall Analysis')
elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Starup Details')
    st.title('Startup Analysis')
else:
    selected_investor= st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].fillna('').astype(str).str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Detail')
   
    if btn2:
        load_investor_detail(selected_investor)