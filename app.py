import streamlit as st
import sys
import os

# Add utilities directory to system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'utilities')))

from visualizations import DashboardRenderer
from chatbot import Chatbot
from data_handler import DataLoader, DataPreprocessor

def main():
    # Sidebar navigation
    menu = ["Dashboard", "Chatbot"]
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

if __name__ == "__main__":
    main()
