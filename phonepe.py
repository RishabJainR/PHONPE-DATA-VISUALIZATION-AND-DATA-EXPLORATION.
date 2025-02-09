import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image



### dataframe creation

mydb=psycopg2.connect(host ="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="Rishab@90")

cursor = mydb.cursor()

#aggregated insurance dataframe

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

aggregated_insurance=pd.DataFrame(table1,columns=("States", "Years", "Quarters", "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggregated transaction dataframe

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

aggregated_transaction=pd.DataFrame(table2,columns=("States", "Years", "Quarters", "Transaction_type", "Transaction_count", "Transaction_amount"))

#aggregated user dataframe

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

aggregated_user=pd.DataFrame(table3,columns=("States", "Years", "Quarters", "Brands", "Transaction_count", "Percentage"))


#Map insurance dataframe

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

map_insurance=pd.DataFrame(table4,columns=("States", "Years", "Quarters", "Districts", "Transaction_count", "Transaction_amount"))


#Map transaction dataframe

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

map_transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarters", "Districts", "Transaction_count", "Transaction_amount"))


#Map user dataframe

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

map_user=pd.DataFrame(table6,columns=("States", "Years", "Quarters", "Districts", "RegisteredUsers", "AppOpens"))

# top insurance dataframe

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

top_insurance=pd.DataFrame(table7,columns=("States", "Years", "Quarters", "Pincodes", "Transaction_amount", "Transaction_count"))

# top transaction dataframe

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

top_transaction=pd.DataFrame(table8,columns=("States", "Years", "Quarters", "Pincodes", "Transaction_amount", "Transaction_count"))

# top user dataframe

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

top_user=pd.DataFrame(table9,columns=("States", "Years", "Quarters", "Pincodes", "RegisteredUsers"))





def Transaction_amount_count_Y(df, year):

    tacy=df[df["Years"]== year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States",y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset,height=650,width=600)
      
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States",y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        
        st.plotly_chart(fig_count)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color="Transaction_amount", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max() ),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color="Transaction_count", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max() ),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)


    return tacy


def Transaction_amount_count_Y_Q(df, quarter):
    tacy=df[df["Quarters"] == quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States",y="Transaction_amount", title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States",y="Transaction_count", title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)


    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response =requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    col1,col2=st.columns(2)
    with col1:
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color="Transaction_amount", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max() ),
                                hover_name="States", title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color="Transaction_count", color_continuous_scale="Rainbow", 
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max() ),
                                hover_name="States", title=f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy



def Aggre_Tran_Transaction_type(df, state):


    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame = tacyg, names="Transaction_type", values="Transaction_amount", 
                            width=600, title=f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)

        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame = tacyg, names="Transaction_type", values="Transaction_count", 
                            width=600, title=f"{state.upper()} TRANSACTION COUNT", hole= 0.5)

        st.plotly_chart(fig_pie_2)


# aggregated user analysis 1

def Aggre_user_plot_1(df, year):

    aguy=df[df["Years"]== year]
    aguy.reset_index(drop=True,inplace=True)
    

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)


    fig_bar_1= px.bar(aguyg,x="Brands",y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT", 
                    width=1000, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aguy


# aggregated user analysis 2

def Aggre_user_plot_2(df,quarter):
    aguyq=df[df["Quarters"]== quarter]
    aguyq.reset_index(drop=True,inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_1= px.bar(aguyqg,x="Brands",y="Transaction_count", title= f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT", 
                        width=1000, color_discrete_sequence=px.colors.sequential.haline , hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aguyq


# aggregate user analysis 3

def Aggre_user_plot_3(df, state):
    auyqs=df[df["States"]== state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1= px.line(auyqs,x="Brands", y="Transaction_count", hover_data="Percentage", 
                        title=f"{state.upper()} BRANDS , TRANSACTION COUNT, PERCENTAGE", width=1000 , markers=True)

    st.plotly_chart(fig_line_1)

    return auyqs


# Map insurance district

def Map_insur_District(df, state):


    tacy=df[df["States"] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg,x="Transaction_amount", y="Districts", orientation= "h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody_r)

        st.plotly_chart(fig_bar_1)
    with col2:    
        fig_bar_2= px.bar(tacyg,x="Transaction_count", y="Districts", orientation= "h",
                        title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Blackbody_r)

        st.plotly_chart(fig_bar_2)

        return tacy
    


# MAP USER PLOT 1

def map_user_plot_1(df,year):

    muy=df[df["Years"]== year]
    muy.reset_index(drop=True,inplace=True)


    muyg=pd.DataFrame(muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyg.reset_index(inplace=True)

    fig_line_1= px.line(muyg, x="States", y=["RegisteredUsers","AppOpens"],  
                            title=f"{year} REGISTER USER AND APP OPENS", width=1000 ,height=800, markers=True)

    st.plotly_chart(fig_line_1)

    return muy

# MAP USER PLOT 2

def map_user_plot_2(df,quarter):

    muyq=df[df["Quarters"]== quarter]
    muyq.reset_index(drop=True,inplace=True)


    muyqg=pd.DataFrame(muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum())
    muyqg.reset_index(inplace=True)

    fig_line_1= px.line(muyqg, x="States", y=["RegisteredUsers","AppOpens"],  
                            title=f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTER USER AND APP OPENS", width=1000 ,height=800, markers=True, 
                            color_discrete_sequence=px.colors.sequential.Rainbow)

    st.plotly_chart(fig_line_1)

    return muyq


# map user plot 3
def map_user_plot_3(df, states):
    muyqs=df[df["States"]== states]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts" , orientation="h",
                                title=f"{states.upper()}REGISTERD USER", height=800 , color_discrete_sequence= px.colors.sequential.Agsunset)

        st.plotly_chart(fig_map_user_bar_1)
        
    with col2:

        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts" ,
                                title=f"{states.upper()} APPS OPEN", height=800 , color_discrete_sequence= px.colors.sequential.Aggrnyl_r)

        st.plotly_chart(fig_map_user_bar_2)

        return muyqs


# Top insurance plot 1
def Top_insurance_plot_1(df, state):
    tiy=df[df["States"]== state]
    tiy.reset_index(drop=True,inplace=True)

    tiyg=tiy.groupby("Pincodes")[["Transaction_amount","Transaction_count"]].sum()
    tiyg.reset_index(inplace=True)


    col1,col2 = st.columns(2)
    with col1:
        fig_top_insur_bar_1=px.bar(tiy, x="Quarters", y="Transaction_amount" , hover_data= "Pincodes",
                                    title="TRANSACTION AMOUNT", height=800 , color_discrete_sequence= px.colors.sequential.GnBu_r)

        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x="Quarters", y="Transaction_count" , hover_data= "Pincodes",
                                    title="TRANSACTION COUNT", height=800 , color_discrete_sequence= px.colors.sequential.Agsunset)

        st.plotly_chart(fig_top_insur_bar_2)

        return tiy
    

# top user plot 1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]== year]
    tuy.reset_index(drop=True,inplace=True)


    tuyg=pd.DataFrame(tuy.groupby(["States","Quarters"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_plot_1=px.bar(tuy, x="States", y="RegisteredUsers" , color= "Quarters", hover_name="States",
                                    title=f"{year} REGISTERED USERS",height=800 ,width=1000, color_discrete_sequence= px.colors.sequential.Burgyl)

    st.plotly_chart(fig_top_plot_1)


    return tuy


# top user plot 2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot_2=px.bar(tuys,x="Quarters", y="RegisteredUsers", title="REGISTRATION, PINCODE, QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta)
    
    st.plotly_chart(fig_top_plot_2)




# SQL Connection

def top_chart_transaction_amount(table_name):

    mydb=psycopg2.connect(host ="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Rishab@90")

    cursor = mydb.cursor()


    # PLOT 1
    query1=f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="states",y="transaction_amount", title=f"TOP 10 OF TRANSACTION AMOUNT", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="states")
        
        st.plotly_chart(fig_amount_1)



    #### PLOT 2

    query2=f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount ASC
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_amount"))

    
    with col2:

        fig_amount_2 = px.bar(df_2, x="states",y="transaction_amount", title=f"TOP 10 OF TRANSACTION AMOUNT", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="states")
        
        st.plotly_chart(fig_amount_2)



    #### plot 3

    query3=f'''SELECT states, AVG(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states 
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_amount"))



    fig_amount_3 = px.bar(df_3, y="states",x="transaction_amount", title=f"AVERAGE OF TRANSACTION AMOUNT", height=800,
                            width=1000,color_discrete_sequence=px.colors.sequential.Blues_r, hover_name="states",
                            orientation="h")
    
    st.plotly_chart(fig_amount_3)


    #######


def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host ="localhost",
                            user="postgres",
                            port="5432",
                            database="phonepe_data",
                            password="Rishab@90")

    cursor = mydb.cursor()


        # PLOT 1
    query1=f'''SELECT states, SUM(transaction_count) AS transaction_count 
                    FROM {table_name}
                    GROUP BY states 
                    ORDER BY transaction_count DESC
                    LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","transaction_count"))
        
    col1,col2=st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="states",y="transaction_count", title=f"TOP 10 OF TRANSACTION COUNT", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.YlOrBr, hover_name="states")
        st.plotly_chart(fig_amount_1)



        #### PLOT 2

    query2=f'''SELECT states, SUM(transaction_count) AS transaction_count 
                    FROM {table_name}
                    GROUP BY states 
                    ORDER BY transaction_count ASC
                    LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","transaction_count"))

    with col2:

        fig_amount_2 = px.bar(df_2, x="states",y="transaction_count", title=f"LAST 10 OF TRANSACTION COUNT", height=650,
                                    width=600,color_discrete_sequence=px.colors.sequential.YlOrBr, hover_name="states")
        st.plotly_chart(fig_amount_2)

        #### plot 3

    query3=f'''SELECT states, AVG(transaction_count) AS transaction_count 
                    FROM {table_name}
                    GROUP BY states 
                    ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","transaction_count"))

    fig_amount_3 = px.bar(df_3, y="states",x="transaction_count", title=f"AVERAGE OF TRANSACTION COUNT", height=800,
                                width=1000,color_discrete_sequence=px.colors.sequential.thermal, hover_name="states",
                                orientation="h")
    st.plotly_chart(fig_amount_3)

    

###########################################


def top_chart_registered_user(table_name, state):

    mydb=psycopg2.connect(host ="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Rishab@90")

    cursor = mydb.cursor()


    # PLOT 1
    query1=f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1 = px.bar(df_1, x="districts",y="registeredusers", title=f"TOP 10 OF REGISTERED USER", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="districts")
        st.plotly_chart(fig_amount_1)



    #### PLOT 2

    query2=f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY registeredusers;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","registeredusers"))

    with col2:

        fig_amount_2 = px.bar(df_2, x="districts",y="registeredusers", title=f"LAST 10 OF REGISTERED USER", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="districts")
        st.plotly_chart(fig_amount_2)

    #### plot 3

    query3=f'''SELECT districts, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","registeredusers"))

    fig_amount_3 = px.bar(df_3, y="districts",x="registeredusers", title=f"AVERAGE OF REGISTERED USER", height=650,orientation="h",
                            width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="districts")
    st.plotly_chart(fig_amount_3)



    #######################


def top_chart_appopens(table_name, state):

    mydb=psycopg2.connect(host ="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Rishab@90")

    cursor = mydb.cursor()


    # PLOT 1
    query1=f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts","appopens"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="districts",y="appopens", title=f"TOP 10 OF APP OPENS", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Reds_r, hover_name="districts")
        st.plotly_chart(fig_amount_1)



    #### PLOT 2

    query2=f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY appopens;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts","appopens"))

    with col2:

        fig_amount_2 = px.bar(df_2, x="districts",y="appopens", title=f"LAST 10 OF APP OPENS", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Bluyl, hover_name="districts")
        st.plotly_chart(fig_amount_2)

    #### plot 3

    query3=f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts 
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts","appopens"))

    fig_amount_3 = px.bar(df_3, y="districts",x="appopens", title=f"AVERAGE OF APP OPENS", height=650,orientation="h",
                            width=600,color_discrete_sequence=px.colors.sequential.Magma, hover_name="districts")
    st.plotly_chart(fig_amount_3)




    ##########################


def top_chart_registered_user(table_name):

    mydb=psycopg2.connect(host ="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="Rishab@90")

    cursor = mydb.cursor()


    # PLOT 1
    query1=f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name} 
                GROUP BY states 
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states","registeredusers"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1 = px.bar(df_1, x="states",y="registeredusers", title=f"TOP 10 OF REGISTERED USERS", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="states")
        st.plotly_chart(fig_amount_1)



    #### PLOT 2

    query2=f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}  
                GROUP BY states 
                ORDER BY registeredusers ASC
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states","registeredusers"))

    with col2:

        fig_amount_2 = px.bar(df_2, x="states",y="registeredusers", title=f"BOTTOM 10 OF REGISTERED USERS", height=650,
                                width=600,color_discrete_sequence=px.colors.sequential.Agsunset, hover_name="states")
        st.plotly_chart(fig_amount_2)

    #### plot 3

    query3=f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name} 
                GROUP BY states 
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states","registeredusers"))

    fig_amount_3 = px.bar(df_3, y="states",x="registeredusers", title=f"AVERAGE OF REGISTERED USERS", height=800,
                            width=1000,color_discrete_sequence=px.colors.sequential.Agsunset, orientation="h")
    st.plotly_chart(fig_amount_3)





#streamlit part

st.set_page_config(layout="wide")
st.title("PHONPE DATA VISUALIZATION AND DATA EXPLORATION")

with st.sidebar:

    select = option_menu("MAIN MENU",["HOME","DATA EXPLORATION","TOP CHARTS"])


if select == "HOME":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\risha\Desktop\New folder\pic.png"),width= 600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\risha\Desktop\New folder\download.jpeg"),width=600)

    with col4:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")

        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\risha\Desktop\New folder\download.png"),width= 600)





    
elif select == "DATA EXPLORATION":

    tab1,tab2,tab3 = st.tabs(["AGGREGATERD ANALYSIS","MAP ANALYSIS","TOP ANALYSIS"])

    with tab1:
        
        method=st.radio("SELECT THE METHOD",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])
        
        if method == "INSURANCE ANALYSIS":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year ia",aggregated_insurance["Years"].min(),aggregated_insurance["Years"].max(),aggregated_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(aggregated_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ia ",tac_Y["Quarters"].min(),tac_Y["Quarters"].max(),tac_Y["Quarters"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method == "TRANSACTION ANALYSIS":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year ta ",aggregated_transaction["Years"].min(),aggregated_transaction["Years"].max(),aggregated_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(aggregated_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State ta", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ta",Aggre_tran_tac_Y["Quarters"].min(),Aggre_tran_tac_Y["Quarters"].max(),Aggre_tran_tac_Y["Quarters"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State tay", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q, states)
            

        elif method == "USER ANALYSIS":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year ua",aggregated_user["Years"].min(),aggregated_user["Years"].max(),aggregated_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(aggregated_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter ua ",Aggre_user_Y["Quarters"].min(),Aggre_user_Y["Quarters"].max(),Aggre_user_Y["Quarters"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State ua", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q, states)


            

    with tab2:
        
        method2=st.radio("SELECT THE METHOD",["MAP INSURANCE","MAP TRANSACTION","MAP USER"])
        
        if method2 == "MAP INSURANCE":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years mi",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min())
            map_insur_tac_Y=Transaction_amount_count_Y(map_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State Map Insurance mi", map_insur_tac_Y["States"].unique())

            Map_insur_District(map_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter Map mi",map_insur_tac_Y["Quarters"].min(),map_insur_tac_Y["Quarters"].max(),map_insur_tac_Y["Quarters"].min())
            map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(map_insur_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State mi", map_insur_tac_Y_Q["States"].unique())

            Map_insur_District(map_insur_tac_Y_Q, states)


        elif method2 == "MAP TRANSACTION":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years mt",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min())
            map_tran_tac_Y=Transaction_amount_count_Y(map_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State Map Insurance mt", map_tran_tac_Y["States"].unique())

            Map_insur_District(map_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter Map mt",map_tran_tac_Y["Quarters"].min(),map_tran_tac_Y["Quarters"].max(),map_tran_tac_Y["Quarters"].min())
            map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(map_tran_tac_Y,quarters)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State mt", map_tran_tac_Y_Q["States"].unique())

            Map_insur_District(map_tran_tac_Y_Q, states)



        elif method2 == "MAP USER":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years mu",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min())
            map_user_Y=map_user_plot_1(map_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter Map mu",map_user_Y["Quarters"].min(),map_user_Y["Quarters"].max(),map_user_Y["Quarters"].min())
            map_user_Y_Q=map_user_plot_2(map_user_Y,quarters)


            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State mu", map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)

            
    with tab3:
        
        method3=st.radio("SELECT THE METHOD",["TOP INSURANCE","TOP TRANSACTION","TOP USER"])
        
        if method3 == "TOP INSURANCE":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years ti",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min())
            top_insur_tac_Y=Transaction_amount_count_Y(top_insurance, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State ti", top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(top_insur_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter Map ti",top_insur_tac_Y["Quarters"].min(),top_insur_tac_Y["Quarters"].max(),top_insur_tac_Y["Quarters"].min())
            top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(top_insur_tac_Y,quarters)


        elif method3 == "TOP TRANSACTION":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years tt",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min())
            top_tran_tac_Y=Transaction_amount_count_Y(top_transaction, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State tt", top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(top_tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter Map tt",top_tran_tac_Y["Quarters"].min(),top_tran_tac_Y["Quarters"].max(),top_tran_tac_Y["Quarters"].min())
            top_trans_tac_Y_Q=Transaction_amount_count_Y_Q(top_tran_tac_Y,quarters)
            



        elif method3 == "TOP USER":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Years tu",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
            top_user_Y=top_user_plot_1(top_user, years)

            col1,col2 = st.columns(2)
            with col1:
                states=st.selectbox("Select the State tu", top_user_Y["States"].unique())
            
            top_user_plot_2(top_user_Y, states)

 

elif select == "TOP CHARTS":
    
    question=st.selectbox("SELECT THE QUESTION",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User", 
                                                    "8. Registered users of the Map User", 
                                                    "9. App opens of Map User", 
                                                    "10. Registered users of the Top User"
                                                    ])
    


    if question== "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")



    elif question== "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question== "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question== "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")


    elif question=="5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")


    elif question=="6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")


        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")


    elif question== "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")


    elif question=="8. Registered users of the Map User":

        states=st.selectbox("SELECT THE STATE", map_user["States"].unique())
        
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user", states )


    elif question=="9. App opens of Map User":

        states=st.selectbox("SELECT THE STATE", map_user["States"].unique())
        
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states )
    

    elif question=="10. Registered users of the Top User":

        st.subheader("TOP USER")
        top_chart_registered_user("top_user")




