import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import time
import pandas

st.set_page_config(layout='wide',page_title='StartUp Analysis')

st.title('Startup Funding Analysis Dashboard')

csv_file = pd.read_csv('D:\Learning\DSMP 2.0\startup-analysis-dashboard\Datasets\startup_funding.csv')
# st.dataframe(csv_file)



#To Drop Remarks
csv_file.drop(columns=['Remarks'],inplace=True)
#To change column names.
csv_file.rename(columns={'Date dd/mm/yyyy':'Date','City  Location':'City','InvestmentnType':'Investment Type','Amount in USD':'Amount','Sr No':'No'},inplace=True)
#To set index as No
csv_file.set_index(['No'],inplace=True)
#Conver Date columd to date type.
csv_file['Date']=pd.to_datetime(csv_file['Date'], format='%d/%m/%Y',errors='coerce')
csv_file['Date']=csv_file['Date'].fillna(pd.to_datetime('1900-01-01'))

#To Create New Year and Month COlumn
csv_file['Year_Number']=csv_file['Date'].dt.year
csv_file['Month']=csv_file['Date'].dt.month
csv_file['Month_Year']=csv_file['Month'].astype(str)+'-'+csv_file['Year_Number'].astype(str)

#Handle Amount
csv_file['Amount']=csv_file['Amount'].fillna(0)
csv_file = csv_file[csv_file['Amount']!='Undisclosed']
csv_file = csv_file[csv_file['Amount']!='unknown']
csv_file = csv_file[csv_file['Amount']!='undisclosed']
csv_file['Amount'] = np.round(csv_file['Amount'].str.replace(r'[^0-9.]', '', regex=True).astype(float)*82.5/10000000,1)
csv_file['Amount'] = csv_file['Amount'].fillna(0)


#Load Startup dropdown
csv_file['Startup Name'] = csv_file['Startup Name'].str.strip('"#\\')
ustartup = sorted(csv_file['Startup Name'].unique().tolist())

#Load investor dropdown
csv_file['Investors Name'] = csv_file['Investors Name'].fillna('Undisclosed')
# csv_file['Investors Name'] = csv_file['Investors Name'].astype(str)
csv_file['Investors Name'] = csv_file['Investors Name'].str.strip('\\\\"')
uinvestor = sorted(set(csv_file['Investors Name'].str.split(',').sum()))

st.sidebar.title('Select Your Choice')

option = st.sidebar.selectbox('Select One',['StartUp','Investor','Overall Analysis'])

if option == 'StartUp':
    Startup_Name = st.sidebar.selectbox('Select StartUp Name',ustartup)
    btn1 = st.sidebar.button('See StartUp Anlysis')
    if btn1:
        st.title(Startup_Name)
        Ind_Verti = csv_file[csv_file['Startup Name'] == Startup_Name]['Industry Vertical']
        st.subheader('Industry Name')
        st.write(Ind_Verti)

        SubInd_Verti = csv_file[csv_file['Startup Name'] == Startup_Name]['SubVertical']
        st.subheader('Sub Industry Name')
        st.write(SubInd_Verti)

        Location = csv_file[csv_file['Startup Name'] == Startup_Name]['City']
        st.subheader('Startup Location Name')
        st.write(Location)

        at = csv_file[csv_file['Startup Name'] == Startup_Name]
        f_data = at[['Date', 'Startup Name', 'Investors Name', 'Amount']].sort_values('Date')
        st.dataframe(f_data)

        # st.write('Company Name ' + c_name)
elif option == 'Investor':
    ivnt_name = st.sidebar.selectbox('Select Investor Name',uinvestor)
    btn2 = st.sidebar.button('See Investor Anlysis')

    #To Get Recent Investments
    recent_investments = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].sort_values('Date',ascending=False).head(5)[['Date','City','Amount','SubVertical','Investment Type']]

    #To get maximum invested
    max_investment = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].groupby('Startup Name')['Amount'].sum().sort_values(ascending=False).head(5)

    #To Get Generally Invest in Sector
    g_sector = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].groupby('Industry Vertical')['Amount'].sum()

    # To Get Generally Invest in Stage
    g_stage = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].groupby('Investment Type')['Amount'].sum()

    # To Get Generally Invest in City
    g_city = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].groupby('City')['Amount'].sum()

    #To get YoY Investment

    g_YoY = csv_file[csv_file['Investors Name'].str.contains(ivnt_name)].groupby('Year_Number')['Amount'].sum()

    if btn2:
        # st.title('Investor Analysis')

        st.title(ivnt_name)

        st.markdown(f'- #### Recent Investments Made By {ivnt_name} Investor :')
        st.dataframe(recent_investments)
        # csv_file

        st.markdown(f'- #### Maximum Investments Made By {ivnt_name} Investor :')
        a1,a2 = st.columns(2)
        with a1:
            st.dataframe(max_investment)
        with a2:
            st.bar_chart(max_investment)

        st.markdown(f'- #### Most Common Sector In Which Investments Made By {ivnt_name} Investor :')
        a1, a2 = st.columns(2)
        with a1:
            st.dataframe(g_sector)
        with a2:
            fig,ax = plt.subplots()
            ax.pie(g_sector.values,labels=g_sector.index, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig)

        st.markdown(f'- #### Most Common Stage In Which Investments Made By {ivnt_name} Investor :')
        a1, a2 = st.columns(2)
        with a1:
            st.dataframe(g_stage)
        with a2:
            fig, ax = plt.subplots()
            ax.pie(g_stage.values, labels=g_stage.index, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig)

        st.markdown(f'- #### Most Common City In Which Investments Made By {ivnt_name} Investor :')
        a1, a2 = st.columns(2)
        with a1:
            st.dataframe(g_city)
        with a2:
            fig, ax = plt.subplots()
            ax.pie(g_city.values, labels=g_city.index, autopct='%1.1f%%', startangle=90)
            st.pyplot(fig)

        st.markdown(f'- #### To Get Idea On YoY Investment Done By {ivnt_name} Investor :')
        a1, a2 = st.columns(2)
        with a1:
            st.dataframe(g_YoY)
        with a2:
            # fig, ax = plt.subplots()
            # ax.pie(g_YoY.values, labels=g_YoY.index, autopct='%1.1f%%', startangle=90)
            # st.pyplot(fig)
            st.line_chart(g_YoY)


else:
    btn3 = st.sidebar.button('See Overall Anlysis')
    # if btn3:

    st.title('OverAll Analysis')
    q1,q2,q3,q4 = st.columns(4)

    with q1:
        total_cr_invested = round(csv_file['Amount'].sum())
        st.metric('Total Invested Amount ',str(total_cr_invested), ' CR')

    with q2:
        max_cr_invested = round(csv_file.groupby('Startup Name')['Amount'].max().sort_values(ascending=False).head().values[0])
        st.metric('Max Invested Amount ',str(total_cr_invested), ' CR')

    with q3:
        avg_cr_invested = round(csv_file.groupby('Startup Name')['Amount'].sum().mean())
        st.metric('Average Invested Amount ',str(avg_cr_invested), ' CR')

    with q4:
        total_funded_startup = csv_file['Startup Name'].nunique()
        st.metric('Total Funded Startup ',str(total_funded_startup), ' CR')

    st.subheader('MoM Graph')
    sel = st.selectbox('Select Your Choice',['Total Amount','Total Funded Startup'])
    if sel=='Total Amount':
        MoM_Amount = csv_file.groupby(['Month_Year'])['Amount'].sum()
        st.line_chart(MoM_Amount)
    elif sel=='Total Funded Startup':
        MoM_Count = csv_file.groupby(['Month_Year'])['Startup Name'].count()
        st.line_chart(MoM_Count)

    st.subheader('Top Secotors By Invested Amount')
    Top_SA = csv_file.groupby('Industry Vertical')['Amount'].sum().sort_values(ascending=False).head(20)
    st.line_chart(Top_SA)

    st.subheader('Top Secotors By Total Industry')
    Top_TI = csv_file.groupby('Industry Vertical')['Startup Name'].count().sort_values(ascending=False).head(20)
    st.line_chart(Top_TI)

    st.subheader('Top Startup YearWise')
    Top_Startup_YW = csv_file.groupby('Year_Number').agg({'Startup Name': 'first', 'Amount': 'sum'}).sort_values('Amount',ascending=False)
    st.dataframe(Top_Startup_YW)

    st.subheader('Top Startup Based On Amount Invested')
    Top_Startup_AW = csv_file.groupby('Startup Name')['Amount'].sum().sort_values(ascending=False).head(10)
    st.dataframe(Top_Startup_AW)

    st.subheader('City Wise Funding')
    City_Fund = csv_file.groupby('City')['Amount'].sum().sort_values(ascending=False)
    st.dataframe(City_Fund)

    st.subheader('Top Investors')
    Top_Investor = csv_file.groupby('Investors Name')['Amount'].sum().sort_values(ascending=False).head(5)
    st.dataframe(Top_Investor)

