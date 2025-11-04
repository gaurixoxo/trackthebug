# Display the bug data table
    st.header("Bug Data")
    if issue_df.empty:
        st.info("No bug data available.")
    else:
        st.table(issue_df)  # Display bug data in a table format
        
        # Add edit button to change status
        st.sidebar.header("Edit Status")
        selected_issue = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="status_edit_issue")
        new_status = st.sidebar.selectbox("Select New Status", ["Open", "Closed", "In Progress"], key="status_edit_select")
        if st.sidebar.button("Edit Status"):
            cursor.execute("UPDATE issue SET Status=%s WHERE issue_name=%s", (new_status, selected_issue))
            mydb.commit()
            st.sidebar.success("Status updated successfully!")
    
            # Update issue_df with new data
            cursor.execute("SELECT * FROM issue")
            issue = cursor.fetchall()
            issue_df = pd.DataFrame(issue, columns=columns)

            # Rerun the app to reflect the updated status
            st.experimental_rerun()


        # Add edit button to change closed date
        st.sidebar.header("Edit Closed Date")
        selected_issue_closed_date = st.sidebar.selectbox("Select Issue", issue_df['issue_name'], key="date_edit_issue")
        new_closed_date = st.sidebar.date_input("Select New Closed Date", key="date_edit_select")
        if st.sidebar.button("Edit Closed Date"):
            cursor.execute("UPDATE issue SET closed_date=%s WHERE issue_name=%s", (new_closed_date, selected_issue_closed_date))
            mydb.commit()
            st.sidebar.success("Closed date updated successfully!")
            
            # Update issue_df with new data
            cursor.execute("SELECT * FROM issue")
            issue = cursor.fetchall()
            issue_df = pd.DataFrame(issue, columns=columns)

            # Rerun the app to reflect the updated status
            st.experimental_rerun()

            st.subheader("Proportion of Open vs. Closed Issues by Assignee")
            fig, ax = plt.subplots(figsize=(10, 6))
            status_counts = df.groupby('assigned_to')['Status'].value_counts().unstack().fillna(0)
            status_counts['Total'] = status_counts.sum(axis=1)
            status_counts['Open Ratio'] = status_counts['Open'] / status_counts['Total']
            status_counts['Closed Ratio'] = status_counts['Closed'] / status_counts['Total']
            status_counts[['Open Ratio', 'Closed Ratio']].plot(kind='bar', stacked=True, cmap='coolwarm', ax=ax)
            plt.title('Proportion of Open vs. Closed Issues by Assignee')
            plt.xlabel('Assigned To')
            plt.ylabel('Proportion')
            plt.xticks(rotation=45)
            plt.legend(title='Status')
            st.pyplot(fig)


# Run the Streamlit app
if __name__ == '__main__':
    app()
