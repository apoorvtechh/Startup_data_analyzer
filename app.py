import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import calendar




df=pd.read_csv('startup_cleaned.csv')
df = df.dropna(subset=['investors', 'vertical', 'city'])
df['subvertical'] = df['subvertical'].fillna('Not Specified')
df['date']=pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month']=df['date'].dt.month
df['month'] = df['month'].astype('Int64')
df['year'] = df['year'].astype('Int64')
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
            ax3.pie(city_df,labels=None,autopct="%0.01f%%")
            ax3.legend( labels=city_df.index, title="City", loc="center left", bbox_to_anchor=(1, 1))
            
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
            ax1.pie(vertical_df,labels=None,autopct="%0.01f%%")
            ax1.legend( labels=vertical_df.index, title="Verticals", loc="center left", bbox_to_anchor=(1, 1))
            
            st.pyplot(fig1)
        else:
            st.warning(f"No investment data available to plot for investor: {investor}")

        if  not round_df.empty and round_df.sum() > 0:
            st.subheader(f'Investment Rounds - {investor}')
            fig2, ax2 = plt.subplots(figsize=(8,8))
            ax2.pie(round_df,labels=None,autopct="%0.01f%%")
            ax2.legend( labels=round_df.index, title="Rounds", loc="center left", bbox_to_anchor=(1, 1))
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
    col5,col6=st.columns(2)
    with col5:
        st.subheader('Top 10 Round Based on Investments')
        round_dff=df.groupby('round')['amount'].sum().sort_values(ascending=False).head(10)
        fig5, ax5 = plt.subplots(figsize=(10, 10))
        ax5.pie(
            round_dff,
            labels=round_dff.index,
            autopct="%0.1f%%")
        st.pyplot(fig5)
    with col6:
        st.subheader('Top 10 City Based on Investments')
        city_dff=df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        fig6,ax6=plt.subplots(figsize=(10,7.5))
        ax6.pie(city_dff,labels=city_dff.index,autopct="%0.1f%%")
        st.pyplot(fig6)
    st.subheader('Top Startup Year-Wise Based On Amount Invested')
    year_wise_startup=df[df['amount'] == df.groupby('year')['amount'].transform('max')].reset_index(drop=True).drop(columns=['Sr No'])
    st.dataframe(year_wise_startup)
    # Group and pivot the data
    heatmap_data = df.groupby(['year', 'month'])['amount'].sum().unstack().fillna(0)
   
    fig7, ax7 = plt.subplots(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax7)

    ax7.set_title("Total Funding Amount by Year and Month")
    ax7.set_xlabel("Month")
    ax7.set_ylabel("Year")
    st.pyplot(fig7)

def load_startup_setails(startup):
    st.title(startup)
    df['date'] = pd.to_datetime(df['date']).dt.date
    last5df=df[df['startup'].str.contains(startup, na=False)][['date','investors','vertical','subvertical','city','round','amount','year']].reset_index().drop(columns=['index'])
    st.subheader('Most Recent Investments')
    st.dataframe(last5df)
    col1,col2=st.columns(2)
    with col1:
        round_inv=last5df.groupby('round')['amount'].sum()
        if  not round_inv.empty and round_inv.sum()>0:
            st.subheader(f'Investment Made Upon Rounds- {startup}')
            fig1, ax1 = plt.subplots(figsize=(10,5))
            ax1.pie(round_inv,labels=None,autopct="%0.01f%%")
            ax1.legend( labels=round_inv.index, title="Funding Rounds", loc="center left", bbox_to_anchor=(1, 1))
            st.pyplot(fig1)
        else:
            st.warning(f"No investment data available to plot for startup: {startup}")
    with col2:
        investor_wise=last5df.groupby('investors')['amount'].sum()
        if  not investor_wise.empty and investor_wise.sum()>0:
            st.subheader(f'Investment Made By Investors- {startup}')
            fig2, ax2 = plt.subplots(figsize=(10,15))
            ax2.pie(investor_wise,labels=None,autopct="%0.01f%%")
            ax2.legend( labels=investor_wise.index, title="Investors", loc="center left", bbox_to_anchor=(1, 1))
            st.pyplot(fig2)
        else:
            st.warning(f"No investment data available to plot for startup: {startup}")
    st.header('Date Wise Investments')
    date_wise=last5df.groupby('year')['amount'].sum()
    date_wise.index=date_wise.index.astype(int)
    fig3,ax3=plt.subplots(figsize=(14, 6))
    ax3.bar(date_wise.index,date_wise.values)
    ax3.set_xticks(ax3.get_xticks()[::1])
    st.pyplot(fig3)
   
    
        
        

        



    




st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if option=='Overall Analysis':
    btn0=st.sidebar.button('Show Overall Analysis')
    if btn0:
        Overall_analysis()


elif option=='Startup':
    selected_stratup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Starup Details')
    if btn1:
        load_startup_setails(selected_stratup)
        
else:
    selected_investor= st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].fillna('').astype(str).str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Detail')
   
    if btn2:
        load_investor_detail(selected_investor)