import streamlit as st
import pandas as pd
from data_handler import DataLoader  # Assuming you already have this class

class IncidentReportOverview:
    """A class to handle the incident report overview page."""

    def __init__(self):
        """Initialize the IncidentReportOverview with a DataLoader."""
        self.data_loader = DataLoader()

    def load_data(self):
        """Load the dataset using DataLoader."""
        return self.data_loader.load_data()

    def display_metrics(self, data):
        """Display summary metrics for the dataset."""
        st.subheader("Summary Metrics")
        
        # Check if required columns are present
        if 'incident_start_time' in data.columns and 'incident_end_time' in data.columns:
            date_range = f"{data['incident_start_time'].min()} to {data['incident_end_time'].max()}"
        else:
            date_range = "N/A (Columns missing)"
        
        if 'severity_level' in data.columns:
            avg_severity = data['severity_level'].str.extract(r'(\d+)').astype(int).mean().iloc[0]
        else:
            avg_severity = "N/A"

        total_incidents = len(data)
        st.write(f"**Total Incidents:** {total_incidents}")
        #st.write(f"**Date Range:** {date_range}")
        #st.write(f"**Average Severity Level:** {avg_severity}")

    def display_data_table(self, data):
        """Display the dataset as a table."""
        st.subheader("Incident Data")
        st.dataframe(data)

    def display_top_components(self, data):
        """Display the top components by incident count."""
        st.subheader("Most Frequently Impacted Components")
        if 'Component' in data.columns:
            top_components = data['Component'].value_counts().head(5)
            st.bar_chart(top_components)
        else:
            st.write("No 'Component' column in the dataset.")

    def render(self):
        """Render the entire incident report overview page."""
        st.title("Incident Report Overview")
        st.markdown(
            "This app is trained on Repository of all incidents from Wikimedia's "
            "[publicly available RCA reports](https://wikitech.wikimedia.org/wiki/Incident_documentation)."
        )
        
        # Load data
        data = self.load_data()
        
        # Display metrics, data table, and top components
        self.display_metrics(data)
        self.display_data_table(data)
        self.display_top_components(data)
