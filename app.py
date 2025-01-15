import streamlit as st
import sys
import os
import pandas as pd

# Add utilities directory to system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utilities')))
# Set the working directory to the project root
os.chdir(os.path.dirname(__file__))

from visualizations import DashboardRenderer
from chatbot import Chatbot
from data_handler import DataLoader, DataPreprocessor
from graph_renderer import GraphRenderer
from graph_data_extractor import GraphDataExtractor  
from incident_report_overview import IncidentReportOverview
from data_retriever import DataRetriever

def main():
    # Sidebar navigation with radio buttons
    menu = ["Dashboard", "Chatbot", "Related Incidents", "Incident Overview"]
    choice = st.sidebar.radio("Menu", menu)

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
    
    # elif choice == "Chatbot":
    #     # Risk evaluation title
    #     st.title("AI Chatbot: Risk Evaluation Assistant")
        
    #     # Load data for chatbot context
    #     data_loader = DataLoader()
    #     data = data_loader.load_data()
        
    #     chatbot = Chatbot()  # Initialize the Chatbot class
    #     st.subheader("Ask Questions About the Dataset")
    #     question = st.text_input("e.g. Tell me what the dataset is about")
    #     if question:
    #         context = chatbot.generate_context(data)
    #         answer = chatbot.ask(question, context)
    #         st.write("**Chatbot's Response:**")
    #         st.write(answer)
    elif choice == "Chatbot":
        # Risk evaluation title
        st.title("AI Chatbot: Risk Evaluation Assistant")
        
        # Load data for chatbot context
        data_loader = DataLoader()
        data = data_loader.load_data()
        
        # Preprocess the data to add YearMonth
        preprocessor = DataPreprocessor()
        data = preprocessor.preprocess(data)
        
        # Initialize RAG components
        api_key = st.secrets["general"]["OPENAI_API_KEY"]
        retriever = DataRetriever(api_key=api_key)
        chatbot = Chatbot(api_key=api_key)

        # Chatbot interface
        st.subheader("Ask Questions About the Dataset")
        question = st.text_input("Enter your question:")

        if question:
            # Retrieve relevant context for RAG-based response
            context_records = retriever.retrieve(question, data, top_k=10)
            context = "\n".join([record['incident_description'] for record in context_records])

            # Handle query
            result = chatbot.handle_query(question, data, context)

            # Display result
            if isinstance(result, str):  # Text response
                st.subheader("Chatbot's Response")
                st.write(result)
            else:  # Visualization
                st.plotly_chart(result)


    elif choice == "Related Incidents":
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
        # st.title("Incident Report Overview")
        # Render the incident report overview page
        overview = IncidentReportOverview()
        overview.render()

if __name__ == "__main__":
    main()