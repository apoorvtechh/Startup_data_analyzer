import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st



df=pd.read_csv('startup_cleaned.csv')
df = df.dropna(subset=['investors', 'vertical', 'city'])
df['subvertical'] = df['subvertical'].fillna('Not Specified')
df['date']=pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month']=df['date'].dt.month
count_df=df.groupby(['year','month'])['startup'].count().reset_index()
count_df['month']=count_df['month'].astype('int')
count_df['year']=count_df['year'].astype('int')
count_df['x_axis']=count_df['month'].astype(str) + '-' + count_df['year'].astype(str)
temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
temp_df['month']=temp_df['month'].astype('int')
temp_df['year']=temp_df['year'].astype('int')
temp_df['x_axis']=temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
st.set_page_config(page_title='Startip Funding Analysis',layout='wide')

 

def load_investor_detail(investor):
    st.title(investor)
    #loading recent five recent investment of the investor
    last5df=df[df['investors'].str.contains(investor, na=False)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5df)
    col1,col2=st.columns(2)
    with col1:
        
        #biggest investment by investor
        big_series=df[df['investors'].str.contains(investor,na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader(f'Investment by Vertical - {investor}')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
        city_df = df[df['investors'].str.contains(investor, na=False)].groupby('city')['amount'].sum()
        if  not city_df.empty and city_df.sum() > 0:
            st.subheader(f'City Details - {investor}')
            fig3, ax3 = plt.subplots()
            ax3.pie(city_df,labels=city_df.index,autopct="%0.01f%%")
            st.pyplot(fig3)
        else:
            st.warning(f"No investment data available to plot for investor: {investor}")

        year_df = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
        if  not year_df.empty and year_df.sum() > 0:
            st.subheader(f'Year Wise Investment Details - {investor}')
            fig4, ax4 = plt.subplots()
            ax4.plot(year_df.index,year_df.values)
            st.pyplot(fig4)
        else:
            st.warning(f"No investment data available to plot for investor: {investor}")







    with col2:
        vertical_df = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')['amount'].sum()
        round_df = df[df['investors'].str.contains(investor, na=False)].groupby('round')['amount'].sum()
        

        # Only plot if total > 0
        if  not vertical_df.empty and vertical_df.sum() > 0:
            st.subheader(f'Investment by Vertical - {investor}')
            fig1, ax1 = plt.subplots(figsize=(12,12))
            ax1.pie(vertical_df,labels=vertical_df.index,autopct="%0.01f%%")
            st.pyplot(fig1)
        else:
            st.warning(f"No investment data available to plot for investor: {investor}")

        if  not round_df.empty and round_df.sum() > 0:
            st.subheader(f'Investment Rounds - {investor}')
            fig2, ax2 = plt.subplots(figsize=(8,8))
            ax2.pie(round_df,labels=round_df.index,autopct="%0.01f%%")
            st.pyplot(fig2)
        else:
            st.warning(f"No investment data available to plot for investor: {investor}")



def Overall_analysis():
    st.title("Overall Analysis")
    total_invested_amount=  round(df['amount'].sum())
    st.metric(label="Total Invested Amount", value=f"{total_invested_amount} Cr")
    maximum_amount=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    company_name=str(df[df['amount']==maximum_amount]['startup'])
    mean_investment=df.groupby('startup')['amount'].sum().mean()
    total_funded_startups=df['startup'].nunique()
    col1,col2,col3=st.columns(3)
    with col1:
        st.metric(label="Maximum Amount", value=f"{maximum_amount} Cr")
        st.metric(label='Average Investment',value=f"{round(mean_investment)} Cr")
    with col2:
        st.metric(label='Startup Name', value=company_name)
        st.metric(label='Total Funded Startups',value=total_funded_startups)
    st.header('Amount Invested Over Each Month')
    # selected_option=st.selectbox('Select Type',['Total','Count'])
    #if selected_option=='Total':
    fig1,ax1=plt.subplots(figsize=(14, 6))
    ax1.plot(temp_df['x_axis'],temp_df['amount'])
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_xticks(ax1.get_xticks()[::2])
    st.pyplot(fig1)
    #else:
    st.header('Startups Funded Over Each Month')  
    fig2,ax2=plt.subplots(figsize=(14, 6))
    ax2.plot(count_df['x_axis'],count_df['startup'])
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_xticks(ax2.get_xticks()[::2])
    st.pyplot(fig2)
    col3,col4=st.columns(2)
    with col3:
        df['vertical'] = df['vertical'].str.strip().str.lower()
        total_startup_df=df.groupby('vertical')['startup'].count().sort_values(ascending=False).reset_index()
        total_startup_df.set_index('vertical')
        st.subheader(f'Top Five Sectors To Get Funded')
        fig3, ax3 = plt.subplots(figsize=(10, 3))
        filtered_df = total_startup_df[total_startup_df['startup'] > 50]
        ax3.pie(
        filtered_df['startup'],               # Numerical values
        labels=filtered_df['vertical'],       # Labels for each slice
        autopct="%0.1f%%")
        st.pyplot(fig3)
    with col4:
        total_amount_startup_df=df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        st.subheader('Top 10 Sectors Based on Amount Invested')
        fig4, ax4 = plt.subplots(figsize=(10, 10))
        ax4.pie(
            total_amount_startup_df,
            labels=total_amount_startup_df.index,
            autopct="%0.1f%%")
        st.pyplot(fig4)
    



    




st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    btn0=st.sidebar.button('Show Overall Analysis')
    if btn0:
        Overall_analysis()


elif option=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Starup Details')
    st.title('Startup Analysis')
else:
    selected_investor= st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].fillna('').astype(str).str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Detail')
   
    if btn2:
        load_investor_detail(selected_investor)