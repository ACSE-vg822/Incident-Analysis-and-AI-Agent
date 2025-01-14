import streamlit as st
import sys
import os
import pandas as pd

# Add utilities directory to system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utilities')))

from visualizations import DashboardRenderer
from chatbot import Chatbot
from data_handler import DataLoader, DataPreprocessor
from graph_renderer import GraphRenderer
from graph_data_extractor import GraphDataExtractor  
from incident_report_overview import IncidentReportOverview

def main():
    # Sidebar navigation
    menu = ["Dashboard", "Chatbot", "Graph", "Incident Overview"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Dashboard":
        # Dashboard title
        st.title("Wikimedia Incident Analysis Dashboard")
        
        # Load data
        data_loader = DataLoader()
        data = data_loader.load_data()

        # Preprocess data
        preprocessor = DataPreprocessor()
        data = preprocessor.preprocess(data)

        # Render the dashboard
        dashboard = DashboardRenderer(data)
        dashboard.render_all()
    
    elif choice == "Chatbot":
        # Chatbot title
        st.title("AI Chatbot: Dataset Analysis Assistant")
        
        # Load data for chatbot context
        data_loader = DataLoader()
        data = data_loader.load_data()
        
        chatbot = Chatbot()  # Initialize the Chatbot class
        st.subheader("Ask Questions About the Dataset")
        question = st.text_input("e.g. Tell me what the dataset is about")
        if question:
            context = chatbot.generate_context(data)
            answer = chatbot.ask(question, context)
            st.write("**Chatbot's Response:**")
            st.write(answer)

    elif choice == "Graph":
        st.title("Interactive Service and Component Correlation Graph")
        
        # Load the parsed incident data
        data_loader = DataLoader()
        incident_data = data_loader.load_data()
        
        # Extract relationships for the graph
        extractor = GraphDataExtractor(incident_data)
        graph_data = extractor.extract_graph_data()
        
        # Render the graph using the extracted data
        graph_renderer = GraphRenderer(graph_data)
        graph_renderer.graph_ui()

    elif choice == "Incident Overview":
        #st.title("Incident Overview")
        # Render the incident report overview page
        overview = IncidentReportOverview()
        overview.render()

if __name__ == "__main__":
    main()
