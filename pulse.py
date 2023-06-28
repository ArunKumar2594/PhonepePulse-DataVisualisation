# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import git
import json
from streamlit_option_menu import option_menu
from PIL import Image

# Load the icon image
icon = Image.open("G:\\Arun\\phonepe\\phonepe.jpg")

# Set the page configuration with the custom icon image
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)


st.sidebar.header(":wave: :black[**Hello! Welcome to the dashboard**]")

# Git Cloning
# Add the path to the git executable to the system path
os.environ['PATH'] = os.environ['PATH'] + ';C:\\Program Files\\Git\\bin'

# Set the GIT_PYTHON_REFRESH environment variable to quiet
os.environ['GIT_PYTHON_REFRESH'] = 'quiet'

repo_path = 'F:\\Arun\\phonepe\\phonepepulse'

if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
    # The repository already exists, perform a git pull to update it
    repo = git.Repo(repo_path)
    repo.remotes.origin.pull()

else:
    # The repository doesn't exist, clone it
    git.Repo.clone_from('https://github.com/PhonePe/pulse.git', repo_path)

# Creating connection with sql workbench
con = sql.connect(host="localhost",
                  user="root",
                  password="250994",
                  database="phonepe_data"
                  )

mycursor = con.cursor(buffered=True)

# Creating option menu in the sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Top Charts", "Explore Data"],
                icons=["house", "graph-up-arrow", "bar-chart-line"],
                menu_icon="menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "purple"},
                        "nav-link-selected": {"background-color": "purple"}})


# MENU 1 - HOME
if selected == "Home":
    st.image("https://cdn.uxhack.co/product_logos/PhonePe_logo_0709210959")
    st.markdown("# :violet[Data Visualization and Exploration]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[Overview :]  This project aims to extract, transform, and visualize data from "
                    "Phonepe Pulse Github repository. "
                    "It involves scripting to extract the data, transformation and "
                    "cleaning using Python, and creating an "
                    "interactive dashboard using Streamlit and Plotly. "
                    "The result is a user-friendly dashboard providing valuable insights from the data.")
    with col2:
        st.image("https://i.gadgets360cdn.com/large/phonepe_1_1624421682624.jpg")

# MENU 2 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :green[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
            """
            #### This menu provides valuable information and insights:
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
            - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
            - Top 10 mobile brands and its percentage based on the how many people use phonepe.
            """
        )

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :blue[State]")
            mycursor.execute(
                f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from trans_agg where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :blue[District]")
            mycursor.execute(
                f"select district , sum(Count) as Total_Count, sum(Amount) as Total from trans_map1 where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count', 'Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                         names='District',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :blue[Pincode]")
            mycursor.execute(
                f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from trans_top where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count', 'Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactions_Count'],
                         labels={'Transactions_Count': 'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2], gap="small")

        with col1:
            st.markdown("### :blue[Brands]")
            if Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(
                    f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from user_agg where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users', 'Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### :blue[District]")
            mycursor.execute(
                f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from user_map where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            st.markdown("### :blue[Pincode]")
            mycursor.execute(
                f"select Pincode, sum(Registered_Users) as Total_Users from user_top where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        with col4:
            st.markdown("### :blue[State]")
            mycursor.execute(
                f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from user_map where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                         names='State',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Appopens'],
                         labels={'Total_Appopens': 'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# MENU 3 - EXPLORE DATA
if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)

    # EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        with col1:
            st.markdown("## :blue[Overall State Data - Transactions Amount]")
            mycursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from trans_map1 where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('G:\\Arun\\phonepe\\state.csv')
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from trans_map1 where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv('G:\\Arun\\phonepe\\state.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(
            f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from trans_map1 where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                         'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

# EXPLORE DATA - USERS
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(
            f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from user_map where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv('G:\\Arun\\phonepe\\state.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        st.markdown("## :blue[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        mycursor.execute(
            f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from user_map where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

        df = pd.DataFrame(mycursor.fetchall(),
                          columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)
