import streamlit as st
import plotly.express as px

class DashboardRenderer:
    """A class to handle rendering of dashboard visualizations."""

    def __init__(self, data):
        """Initialize with the dataset."""
        self.data = data

    def render_monthly_incident_count(self):
        """Render Monthly Incident Count chart."""
        st.subheader("Monthly Incident Count")
        monthly_data = self.data['YearMonth'].value_counts().sort_index().reset_index()
        monthly_data.columns = ['Month', 'Number of Incidents']
        fig = px.bar(monthly_data, x='Month', y='Number of Incidents',
                     title="Monthly Incident Count")
        st.plotly_chart(fig)

    def render_root_cause_analysis(self):
        """Render Root Cause Analysis chart."""
        st.subheader("What Components Fail the Most?")
        root_cause_data = self.data['Component'].value_counts().reset_index()
        root_cause_data.columns = ['Component', 'Number of Incidents']
        fig = px.bar(root_cause_data, x='Component', y='Number of Incidents',
                     title="Incident Distribution by Component Root Cause")
        st.plotly_chart(fig)

    def render_symptom_analysis(self):
        """Render Symptom Analysis chart."""
        st.subheader("What Symptoms are Most Common?")
        symptom_data = self.data['Symptom'].value_counts().reset_index()
        symptom_data.columns = ['Symptom', 'Number of Incidents']
        fig = px.bar(symptom_data, x='Symptom', y='Number of Incidents',
                     title="Incident Distribution by Symptom Type")
        st.plotly_chart(fig)

    def render_service_impact_analysis(self):
        """Render Services Impacted chart."""
        st.subheader("What Services are Affected the Most?")
        service_data = self.data['Service'].value_counts().reset_index()
        service_data.columns = ['Service', 'Number of Incidents']
        fig = px.bar(service_data, x='Service', y='Number of Incidents',
                     title="Incident Distribution by Service Impact Type")
        st.plotly_chart(fig)

    def render_user_impact_analysis(self):
        """Render User Impacted Areas chart."""
        st.subheader("Where were Users Impacted the Most?")
        user_impact_data = self.data['UserImpact'].value_counts().reset_index()
        user_impact_data.columns = ['User Impact Area', 'Number of Incidents']
        fig = px.bar(user_impact_data, x='User Impact Area', y='Number of Incidents',
                     title="Incident Distribution by User Impact Type")
        st.plotly_chart(fig)

    def render_root_cause_categories(self):
        """Render Root Cause Categories chart."""
        st.subheader("What are the Most Common Root Causes?")
        root_cause_category_data = self.data['RootCauseCategory'].value_counts().reset_index()
        root_cause_category_data.columns = ['Root Cause Category', 'Number of Incidents']
        fig = px.bar(root_cause_category_data, x='Root Cause Category', y='Number of Incidents',
                     title="Incident Distribution by Category Root Cause")
        st.plotly_chart(fig)

    def render_all(self):
        """Render all visualizations for the dashboard."""
        self.render_monthly_incident_count()
        self.render_root_cause_analysis()
        self.render_symptom_analysis()
        self.render_service_impact_analysis()
        self.render_user_impact_analysis()
        self.render_root_cause_categories()

# Example usage:
# if __name__ == "__main__":
#     data = ...  # Load your data here
#     dashboard = DashboardRenderer(data)
#     dashboard.render_all()
