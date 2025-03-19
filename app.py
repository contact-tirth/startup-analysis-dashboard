import pandas as pd
import streamlit as st
import time
import pandas

st.title('Starup Funding Analysis Dashboard')

csv_file = pd.read_csv('D:\Learning\DSMP 2.0\startup-analysis-dashboard\Datasets\startup_funding.csv')
# st.dataframe(csv_file)

#Load Startup dropdown
csv_file['Startup Name'] = csv_file['Startup Name'].str.strip('"#\\')
ustartup = sorted(csv_file['Startup Name'].unique().tolist())

#Load investor dropdown
csv_file['Investors Name'] = csv_file['Investors Name'].fillna('Undisclosed')
# csv_file['Investors Name'] = csv_file['Investors Name'].astype(str)
csv_file['Investors Name'] = csv_file['Investors Name'].str.strip('\\\\"')
uinvestor = sorted(csv_file['Investors Name'].unique().tolist())

st.sidebar.title('Select Your Choice')

option = st.sidebar.selectbox('Select One',['StartUp','Investor','Overall Analysis'])

if option == 'StartUp':
    st.sidebar.selectbox('Select StartUp Name',ustartup)
    btn1 = st.sidebar.button('See StartUp Anlysis')
    if btn1:
        st.title('StartUp Analysis')
elif option == 'Investor':
    st.sidebar.selectbox('Select Investor Name',uinvestor)
    btn2 = st.sidebar.button('See Investor Anlysis')
    if btn2:
        st.title('Investor Analysis')
else:
    btn3 = st.sidebar.button('See Overall Anlysis')
    if btn3:
        st.title('OverAll Analysis')