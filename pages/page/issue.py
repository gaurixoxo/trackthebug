import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import random



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mansi1608",
    database="practi"
)


cursor = mydb.cursor()
cursor.execute("SELECT * FROM issue")
issue = cursor.fetchall()


columns = ['issue_name', 'Project_name', 'Status', 'Priority', 'open_date', 'closed_date', 'assigned_to']
issue_df = pd.DataFrame(issue, columns=columns)


tfidf_vectorizer = TfidfVectorizer(max_features=1000)
bug_descriptions_tfidf = tfidf_vectorizer.fit_transform(issue_df['issue_name'])


project_encoder = OneHotEncoder()
project_names_encoded = project_encoder.fit_transform(issue_df[['Project_name']])


status_placeholder = 'Unknown'
issue_df['Status'].fillna(status_placeholder, inplace=True)
status_encoder = OrdinalEncoder(categories=[['Open', 'In Progress', 'Closed', status_placeholder]])
status_encoded = status_encoder.fit_transform(issue_df[['Status']])


priority_encoder = OrdinalEncoder(categories=[['Low', 'Medium', 'High']])
priority_encoded = priority_encoder.fit_transform(issue_df[['Priority']])


assigned_to_encoder = OneHotEncoder()
assigned_to_encoded = assigned_to_encoder.fit_transform(issue_df[['assigned_to']])


features = pd.concat([pd.DataFrame(bug_descriptions_tfidf.toarray()),
                      pd.DataFrame(project_names_encoded.toarray()),
                      pd.DataFrame(status_encoded),
                      pd.DataFrame(priority_encoded, columns=['priority_encoded'])], axis=1)


features.columns = features.columns.astype(str)


X_train, X_test, y_train, y_test = train_test_split(features, issue_df['assigned_to'], test_size=0.2, random_state=42)


y_train.fillna('Unknown', inplace=True)


rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)



import random


def predict_assigned_person(issue_name, project_name, status, priority):
   
    if project_name in project_encoder.categories_[0]:
        
        project_name_encoded = project_encoder.transform([[project_name]])
        status_encoded = status_encoder.transform([[status]])
        priority_encoded = priority_encoder.transform([[priority]])

        
        features = pd.concat([pd.DataFrame(bug_descriptions_tfidf.toarray()),
                              pd.DataFrame(project_name_encoded.toarray()),
                              pd.DataFrame(status_encoded),
                              pd.DataFrame(priority_encoded, columns=['priority_encoded'])], axis=1)

       
        features.columns = features.columns.astype(str)

        
        missing_columns = set(X_train.columns) - set(features.columns)
        for col in missing_columns:
            features[col] = 0

        
        features = features[X_train.columns]

        try:
            
            assigned_person_idx = rf_classifier.predict(features)[0]

            
            assigned_person = assigned_to_categories[assigned_person_idx]

            return assigned_person  
        except:
            pass

    
    team_members = ['Jessica', 'Joey', 'Charles', 'James']
    return random.choice(team_members)


def app():
    global issue_df  
    st.header("Add New Bug")
    with st.expander("Add New Bug"):
        issue_name = st.text_input("Issue Name")
        project_name = st.text_input("Project Name")
        status = st.selectbox("Status", ["Open", "Closed", "In Progress"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        open_date = st.date_input("Open Date")
        closed_date = st.date_input("Closed Date")
        
        
        if st.button("Add Bug"):
            print(f"Issue Name: '{issue_name.strip()}', Project Name: '{project_name.strip()}', Status: '{status}', Priority: '{priority}', Open Date: '{open_date}', Closed Date: '{closed_date}'")
            assigned_person = random.choice(['Jessica', 'Joey', 'Charles', 'James'])
            print(f"Assigned Person: '{assigned_person}'")
            if assigned_person:
                if assigned_person == 'Open':
                    st.error("Cannot assign 'Open' status as a person.")
                else:
                    try:
                        print("Trying to insert into the database...")
                        cursor.execute("INSERT INTO issue (issue_name, Project_name, Status, Priority, open_date, closed_date, assigned_to) VALUES (%s, %s, %s, %s, %s, %s, %s)", (issue_name, project_name, status, priority, open_date, closed_date, assigned_person))
                        mydb.commit()
                        print("Inserted into the database successfully!")
                        st.success("Bug added successfully!")
                        
                        
                        cursor.execute("SELECT * FROM issue")
                        issue = cursor.fetchall()
                        issue_df = pd.DataFrame(issue, columns=columns)
                    except mysql.connector.Error as err:
                        print(f"Error adding bug to MySQL database: {err}")
                        st.error(f"Error adding bug to MySQL database: {err}")
            else:
                print("Error assigning person or person not found.")
                st.error("An error occurred while assigning the person. Please try again.")



   
    st.header("Bug Data")
    if issue_df.empty:
        st.info("No bug data available.")
    else:
        st.table(issue_df)  
        st.sidebar.header("Edit Status")
        selected_issue = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="status_edit_issue")
        new_status = st.sidebar.selectbox("Select New Status", ["Open", "Closed", "In Progress"], key="status_edit_select")
        if st.sidebar.button("Edit Status"):
            cursor.execute("UPDATE issue SET Status=%s WHERE issue_name=%s", (new_status, selected_issue))
            mydb.commit()
            st.sidebar.success("Status updated successfully!")
    
            
            cursor.execute("SELECT * FROM issue")
            issue = cursor.fetchall()
            issue_df = pd.DataFrame(issue, columns=columns)

            
            st.experimental_rerun()


       
        st.sidebar.header("Edit Closed Date")
        selected_issue_closed_date = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="date_edit_issue")
        new_closed_date = st.sidebar.date_input("Select New Closed Date", key="date_edit_select")
        if st.sidebar.button("Edit Closed Date"):
            cursor.execute("UPDATE issue SET closed_date=%s WHERE issue_name=%s", (new_closed_date, selected_issue_closed_date))
            mydb.commit()
            st.sidebar.success("Closed date updated successfully!")
            
            
            cursor.execute("SELECT * FROM issue")
            issue = cursor.fetchall()
            issue_df = pd.DataFrame(issue, columns=columns)

            
            st.experimental_rerun()


if __name__ == '__main__':
    app()
