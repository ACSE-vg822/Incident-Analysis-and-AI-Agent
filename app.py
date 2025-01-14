import streamlit as st
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utilities')))

from visualizations import render_dashboard
from chatbot import ask_gpt, get_dataset_context


@st.cache_data
def load_data():
    """Load the parsed incident reports data."""
    return pd.read_csv("parsed_data\parsed_incident_reports.csv")

def preprocess_data(data):
    """Preprocess the dataset to extract and format date information."""
    # Ensure Date column is in datetime format
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    # Extract year and month as a string (instead of Period)
    data['YearMonth'] = data['Date'].dt.to_period('M').astype(str)
    return data

def main():
    st.title("Wikimedia Incident Analysis Dashboard")

    # Load and preprocess data
    data = load_data()
    data = preprocess_data(data)

    # Sidebar navigation
    menu = ["Dashboard", "Chatbot"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        render_dashboard(data)
    elif choice == "Chatbot":
        st.subheader("AI Chatbot: Ask Questions About the Dataset")
        question = st.text_input("Ask a question about the dataset:")
        if question:
            context = get_dataset_context(data)
            answer = ask_gpt(question, context)
            st.write("**Chatbot's Response:**")
            st.write(answer)


if __name__ == "__main__":
    main()
