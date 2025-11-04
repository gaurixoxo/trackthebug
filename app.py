import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="TrackTheBug",
    page_icon="🐛",
    layout="wide"
)

# Initialize session state for bugs
if 'bugs' not in st.session_state:
    st.session_state.bugs = []

# Title and description
st.title("🐛 TrackTheBug - Bug Tracking System")
st.markdown("Track and manage software bugs efficiently")

# Sidebar for adding new bugs
with st.sidebar:
    st.header("➕ Report New Bug")
    
    bug_title = st.text_input("Bug Title", placeholder="Enter bug title...")
    bug_description = st.text_area("Description", placeholder="Describe the bug...")
    bug_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    bug_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    bug_category = st.selectbox("Category", ["UI", "Backend", "Database", "API", "Other"])
    
    if st.button("Submit Bug", type="primary"):
        if bug_title and bug_description:
            new_bug = {
                "ID": len(st.session_state.bugs) + 1,
                "Title": bug_title,
                "Description": bug_description,
                "Priority": bug_priority,
                "Status": bug_status,
                "Category": bug_category,
                "Reported Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.bugs.append(new_bug)
            st.success("Bug reported successfully!")
            st.rerun()
        else:
            st.error("Please fill in all required fields!")

# Main content area
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Bugs", len(st.session_state.bugs))

with col2:
    open_bugs = len([b for b in st.session_state.bugs if b['Status'] == 'Open'])
    st.metric("Open Bugs", open_bugs)

with col3:
    critical_bugs = len([b for b in st.session_state.bugs if b['Priority'] == 'Critical'])
    st.metric("Critical Bugs", critical_bugs)

with col4:
    resolved_bugs = len([b for b in st.session_state.bugs if b['Status'] == 'Resolved'])
    st.metric("Resolved Bugs", resolved_bugs)

st.divider()

# Filters
st.subheader("🔍 Filter Bugs")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    filter_priority = st.multiselect("Filter by Priority", ["Low", "Medium", "High", "Critical"], default=["Low", "Medium", "High", "Critical"])

with filter_col2:
    filter_status = st.multiselect("Filter by Status", ["Open", "In Progress", "Resolved", "Closed"], default=["Open", "In Progress", "Resolved", "Closed"])

with filter_col3:
    filter_category = st.multiselect("Filter by Category", ["UI", "Backend", "Database", "API", "Other"], default=["UI", "Backend", "Database", "API", "Other"])

# Display bugs
st.subheader("📋 Bug List")

if st.session_state.bugs:
    # Filter bugs based on selection
    filtered_bugs = [
        bug for bug in st.session_state.bugs
        if bug['Priority'] in filter_priority 
        and bug['Status'] in filter_status
        and bug['Category'] in filter_category
    ]
    
    if filtered_bugs:
        df = pd.DataFrame(filtered_bugs)
        
        # Display as interactive table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Title": st.column_config.TextColumn("Title", width="medium"),
                "Priority": st.column_config.TextColumn("Priority", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
            }
        )
        
        # Detailed view of selected bug
        st.subheader("🔍 Bug Details")
        selected_bug_id = st.selectbox("Select Bug ID to view details", [bug['ID'] for bug in filtered_bugs])
        
        if selected_bug_id:
            selected_bug = next((bug for bug in filtered_bugs if bug['ID'] == selected_bug_id), None)
            if selected_bug:
                st.write(f"**Title:** {selected_bug['Title']}")
                st.write(f"**Description:** {selected_bug['Description']}")
                st.write(f"**Priority:** {selected_bug['Priority']}")
                st.write(f"**Status:** {selected_bug['Status']}")
                st.write(f"**Category:** {selected_bug['Category']}")
                st.write(f"**Reported Date:** {selected_bug['Reported Date']}")
    else:
        st.info("No bugs match the selected filters.")
else:
    st.info("No bugs reported yet. Use the sidebar to report your first bug!")

# Footer
st.divider()
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | TrackTheBug v1.0")
