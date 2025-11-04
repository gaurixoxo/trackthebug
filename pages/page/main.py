import streamlit as st
from issue import app as issue_app
from bugBoard import app as bugBoard_app


def main():
    st.write("Welcome to the Bug Tracker App!")
    st.sidebar.title("Bug Tracker")
     # Custom CSS for styling sidebar options
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding-top: 2rem;
        }
        .sidebar .sidebar-content .block-container {
            margin-bottom: 1rem;
        }
        .sidebar .sidebar-content .block-container .stButton {
            width: 100%;
            text-align: left;
            padding: 1rem 1.5rem;  /* Adjust padding to increase size */
            border-radius: 0.5rem;   /* Border radius to make it rectangular */
            background-color: transparent;
            cursor: pointer;
            margin-bottom: 0.5rem; /* Add margin bottom for spacing */
        }
        .sidebar .sidebar-content .block-container .stButton:hover {
            background-color: #f0f0f0; /* Hover color for unselected options */
        }
        .sidebar .sidebar-content .block-container .stButton.active {
            background-color: #f0f0f0; /* Highlighted background color for selected option */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    options = ['Issue List', 'Bug Board']
    selected_option = st.sidebar.radio("Select Page", options)
    if selected_option == 'Issue List':
        issue_app()
    elif selected_option == 'Bug Board':
        bugBoard_app()

