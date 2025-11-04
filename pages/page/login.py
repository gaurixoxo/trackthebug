import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import streamlit as st
import random

# Connect to SQLite DB
conn = sqlite3.connect('bug_data.db')
cursor = conn.cursor()

# Create issue table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS issue (
        issue_name TEXT,
        Project_name TEXT,
        Status TEXT,
        Priority TEXT,
        open_date TEXT,
        closed_date TEXT,
        assigned_to TEXT
    )
''')
conn.commit()

# Fetch data
cursor.execute("SELECT * FROM issue")
issue = cursor.fetchall()

columns = ['issue_name', 'Project_name', 'Status', 'Priority', 'open_date', 'closed_date', 'assigned_to']
issue_df = pd.DataFrame(issue, columns=columns)

if not issue_df.empty:
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    bug_descriptions_tfidf = tfidf_vectorizer.fit_transform(issue_df['issue_name'])

    project_encoder = OneHotEncoder()
    project_names_encoded = project_encoder.fit_transform(issue_df[['Project_name']])

    status_encoder = OneHotEncoder()
    status_encoded = status_encoder.fit_transform(issue_df[['Status']])

    priority_encoder = OrdinalEncoder(categories=[['Low', 'Medium', 'High']])
    priority_encoded = priority_encoder.fit_transform(issue_df[['Priority']])

    assigned_to_encoder = OneHotEncoder()
    assigned_to_encoded = assigned_to_encoder.fit_transform(issue_df[['assigned_to']])

    features = pd.concat([
        pd.DataFrame(bug_descriptions_tfidf.toarray()),
        pd.DataFrame(project_names_encoded.toarray()),
        pd.DataFrame(status_encoded.toarray()),
        pd.DataFrame(priority_encoded, columns=['priority_encoded']),
        pd.DataFrame(assigned_to_encoded.toarray())
    ], axis=1)

    features.columns = features.columns.astype(str)

    X_train, X_test, y_train, y_test = train_test_split(features, issue_df['assigned_to'], test_size=0.2, random_state=42)
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(X_train, y_train)
else:
    rf_classifier = None
    tfidf_vectorizer = None
    project_encoder = None
    status_encoder = None
    priority_encoder = None
    y_train = pd.Series()
    X_train = pd.DataFrame()

# Prediction Function
def predict_assigned_person(issue_name, project_name, status, priority):
    if not all([issue_name, project_name, status, priority]) or rf_classifier is None:
        return random.choice(['Jessica', 'Joey', 'Charles', 'James'])

    try:
        project_name_encoded = project_encoder.transform([[project_name]])
        status_encoded = status_encoder.transform([[status]])
        priority_encoded = priority_encoder.transform([[priority]])

        bug_vector = tfidf_vectorizer.transform([issue_name])

        features = pd.concat([
            pd.DataFrame(bug_vector.toarray()),
            pd.DataFrame(project_name_encoded.toarray()),
            pd.DataFrame(status_encoded.toarray()),
            pd.DataFrame(priority_encoded, columns=['priority_encoded'])
        ], axis=1)

        features.columns = features.columns.astype(str)

        if set(features.columns) != set(X_train.columns):
            return random.choice(['Jessica', 'Joey', 'Charles', 'James'])

        assigned_person = rf_classifier.predict(features)[0]
        return assigned_person
    except:
        return random.choice(['Jessica', 'Joey', 'Charles', 'James'])

# Streamlit App
def app():
    global issue_df

    st.title("🪲 Bug Tracker")

    with st.expander("➕ Add New Bug"):
        issue_name = st.text_input("Issue Name")
        project_name = st.text_input("Project Name")
        status = st.selectbox("Status", ["Open", "Closed", "In Progress"])
        priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        open_date = st.date_input("Open Date")
        closed_date = st.date_input("Closed Date")

        assigned_person = ""
        if issue_name and project_name and open_date and closed_date:
            assigned_person = predict_assigned_person(issue_name, project_name, status, priority)
            st.text(f"Assigned To: {assigned_person}")

        if st.button("Add Bug"):
            if all([issue_name, project_name, status, priority, open_date, closed_date, assigned_person]):
                try:
                    cursor.execute("INSERT INTO issue (issue_name, Project_name, Status, Priority, open_date, closed_date, assigned_to) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (issue_name, project_name, status, priority, str(open_date), str(closed_date), assigned_person))
                    conn.commit()

                    cursor.execute("SELECT * FROM issue")
                    issue = cursor.fetchall()
                    issue_df = pd.DataFrame(issue, columns=columns)
                    st.success("Bug added successfully!")
                except Exception as e:
                    st.error(f"Database Error: {e}")
            else:
                st.warning("Please fill in all the fields!")

    st.header("📋 Bug Data")
    if issue_df.empty:
        st.info("No bug records found.")
    else:
        st.dataframe(issue_df)

        st.sidebar.header("✏️ Edit Status")
        selected_issue = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="status_edit_issue")
        new_status = st.sidebar.selectbox("Select New Status", ["Open", "Closed", "In Progress"], key="status_edit_select")
        if st.sidebar.button("Update Status"):
            cursor.execute("UPDATE issue SET Status=? WHERE issue_name=?", (new_status, selected_issue))
            conn.commit()
            st.sidebar.success("Status updated successfully!")
            st.experimental_rerun()

        st.sidebar.header("📅 Edit Closed Date")
        selected_issue_closed_date = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="date_edit_issue")
        new_closed_date = st.sidebar.date_input("New Closed Date", key="date_edit_select")
        if st.sidebar.button("Update Closed Date"):
            cursor.execute("UPDATE issue SET closed_date=? WHERE issue_name=?", (str(new_closed_date), selected_issue_closed_date))
            conn.commit()
            st.sidebar.success("Closed date updated successfully!")
            st.experimental_rerun()

if __name__ == '__main__':
    app()
