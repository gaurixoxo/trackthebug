import streamlit as st
from issue import app as issue_app  
from bugBoard import app as bugBoard_app  #


def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Login successful")
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.current_page = "Main"
        else:
            st.error("Invalid username or password")

def app():
    if not hasattr(st.session_state, 'logged_in'):
        login()
    else:
        st.sidebar.title("Navigation")
         #  CSS 
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
        selected_page = st.sidebar.radio("Go to", [ "Issue List", "Bug Board"])
        
        if selected_page == "Issue List":
            issue_app()  
        elif selected_page == "Bug Board":
            bugBoard_app()  
        

def main():
    st.write("Welcome to the Bug Tracker App!")
    

if __name__ == '__main__':
    app()
