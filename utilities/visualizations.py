import streamlit as st
import plotly.express as px

def render_dashboard(data):
    """Render all visualizations for the dashboard."""

    # Chart 1: Monthly Incident Count
    st.subheader("Monthly Incident Count")
    monthly_data = data['YearMonth'].value_counts().sort_index().reset_index()
    monthly_data.columns = ['Month', 'Number of Incidents']
    fig1 = px.bar(monthly_data, x='Month', y='Number of Incidents',
                  title="Monthly Incident Count")
    st.plotly_chart(fig1)

    # Chart 2: Root Cause Analysis
    st.subheader("What Components Fail the Most?")
    root_cause_data = data['Component'].value_counts().reset_index()
    root_cause_data.columns = ['Component', 'Number of Incidents']
    fig2 = px.bar(root_cause_data, x='Component', y='Number of Incidents',
                  title="Incident Distribution by Component Root Cause")
    st.plotly_chart(fig2)

    # Chart 3: Symptom Analysis
    st.subheader("What Symptoms are Most Common?")
    symptom_data = data['Symptom'].value_counts().reset_index()
    symptom_data.columns = ['Symptom', 'Number of Incidents']
    fig3 = px.bar(symptom_data, x='Symptom', y='Number of Incidents',
                  title="Incident Distribution by Symptom Type")
    st.plotly_chart(fig3)

    # Chart 4: Services Impacted
    st.subheader("What Services are Affected the Most?")
    service_data = data['Service'].value_counts().reset_index()
    service_data.columns = ['Service', 'Number of Incidents']
    fig4 = px.bar(service_data, x='Service', y='Number of Incidents',
                  title="Incident Distribution by Service Impact Type")
    st.plotly_chart(fig4)

    # Chart 5: User Impacted Areas
    st.subheader("Where were Users Impacted the Most?")
    user_impact_data = data['UserImpact'].value_counts().reset_index()
    user_impact_data.columns = ['User Impact Area', 'Number of Incidents']
    fig5 = px.bar(user_impact_data, x='User Impact Area', y='Number of Incidents',
                  title="Incident Distribution by User Impact Type")
    st.plotly_chart(fig5)

    # Chart 6: Root Cause Categories
    st.subheader("What are the Most Common Root Causes?")
    root_cause_category_data = data['RootCauseCategory'].value_counts().reset_index()
    root_cause_category_data.columns = ['Root Cause Category', 'Number of Incidents']
    fig6 = px.bar(root_cause_category_data, x='Root Cause Category', y='Number of Incidents',
                  title="Incident Distribution by Category Root Cause")
    st.plotly_chart(fig6)
