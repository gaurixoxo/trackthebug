import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def app():
    st.title("Bug Board Analysis")

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mansi1608",
        database="practi",
    )

    query = "select*from issue"
    df = pd.read_sql(query, mydb)
    mydb.close()

    st.subheader("Number of Issues by Project")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='Project_name', data=df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Priority of Issues by Project")
    fig, ax = plt.subplots(figsize=(10, 6))
    priority_order = ['Low', 'Medium', 'High']
    sns.countplot(x='Project_name', hue='Priority', data=df, hue_order=priority_order, ax=ax)
    plt.legend(title='Priority')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Open vs. Closed Issues Over Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    df['open_date'] = pd.to_datetime(df['open_date'])
    df['closed_date'] = pd.to_datetime(df['closed_date'])
    df['open_year_month'] = df['open_date'].dt.to_period('M')
    df['closed_year_month'] = df['closed_date'].dt.to_period('M')
    open_counts = df['open_year_month'].value_counts().sort_index()
    closed_counts = df['closed_year_month'].value_counts().sort_index()
    open_counts.plot(label='Open', marker='o')
    closed_counts.plot(label='Closed', marker='o')
    plt.title('Open vs. Closed Issues Over Time')
    plt.xlabel('Year-Month')
    plt.ylabel('Number of Issues')
    plt.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Number of Issues Assigned to Each Person")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='assigned_to', data=df, order=df['assigned_to'].value_counts().index, ax=ax)
    plt.title('Number of Issues Assigned to Each Person')
    plt.xlabel('Assigned to')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Distribution of Issue Priority by Assignee")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='assigned_to', hue='Priority', data=df, ax=ax)
    plt.title('Distribution of Issue Priority by Assignee')
    plt.xlabel('Assigned to')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend(title='Priority')
    st.pyplot(fig)

    

if __name__ == "__main__":
    app()
