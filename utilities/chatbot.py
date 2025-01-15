from openai import OpenAI
import pandas as pd
import plotly.express as px
import ast

class Chatbot:
    def __init__(self, api_key, model="gpt-4"):
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def analyze_query(self, query):
        """Analyze the query to extract action, subject, and filters."""
        messages = [
            {"role": "system", "content": "You are a query analysis assistant. Return your analysis as a Python dictionary with keys: 'action', 'subject', and 'filters'."},
            {"role": "user", "content": f"Analyze this query: {query}"}
        ]
        response = self.client.chat.completions.create(model=self.model,
        messages=messages,
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()


    def generate_chart(self, data, subject, filters=None):
        """Generate a chart based on the subject and filters."""
        if "monthly incident count" in subject.lower():
            filtered_data = data  # Apply filters if needed
            monthly_data = filtered_data['YearMonth'].value_counts().sort_index().reset_index()
            monthly_data.columns = ['Month', 'Number of Incidents']
            fig = px.bar(monthly_data, x='Month', y='Number of Incidents', title="Monthly Incident Count")
            return fig

        elif "most frequent components" in subject.lower():
            filtered_data = data  # Apply filters if needed
            component_data = filtered_data['Component'].value_counts().reset_index()
            component_data.columns = ['Component', 'Number of Incidents']
            fig = px.bar(component_data, x='Component', y='Number of Incidents', title="Most Frequent Components")
            return fig

        # Add more cases as needed for other visualizations
        return "I couldn't generate a chart for this query."

    def generate_response(self, query, context):
        """Generate a text response using GPT with the retrieved context."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant analyzing incident data."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
        response = self.client.chat.completions.create(model=self.model,
        messages=messages,
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()

    def handle_query(self, query, data, context):
        """Handle user query and determine whether to generate a response or a chart."""
        analysis = self.analyze_query(query)

        try:
            # Safely evaluate the response as a dictionary
            analysis_result = ast.literal_eval(analysis)
        except (SyntaxError, ValueError):
            return "Sorry, I couldn't understand the query structure."

        action = analysis_result.get('action', '').lower()
        subject = analysis_result.get('subject', '')
        filters = analysis_result.get('filters', None)

        if 'show' in action or 'plot' in action:  # Handle visualization requests
            return self.generate_chart(data, subject, filters)
        else:  # Handle text-based queries
            return self.generate_response(query, context)
