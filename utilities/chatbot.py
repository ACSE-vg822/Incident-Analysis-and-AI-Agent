from openai import OpenAI
import pandas as pd
import plotly.express as px
import ast

class Chatbot:
    def __init__(self, api_key, model="gpt-4o"):
        self.model = model
        self.client = OpenAI(api_key=api_key)
    
    def analyze_query(self, query):
        """Analyze the query to extract action, subject, and filters."""
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that converts user queries into a structured format. "
                    "Respond only with a valid JSON object like this: "
                    "{'action': 'plot', 'subject': 'incident count', 'chart_type': 'bar', 'filters': {'date': 'from October 2023'}}"
                )
            },
            {"role": "user", "content": f"Analyze this query: {query}"}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        try:
            return ast.literal_eval(response.choices[0].message.content.strip())
        except (SyntaxError, ValueError):
            return None

    def map_columns(self, query, data):
        """Map natural language terms to dataset columns."""
        column_mapping = {
            'root cause': 'RootCauseCategory',
            'incident count': 'Incident',
            'month': 'YearMonth',
            'component': 'Component',
            'service': 'Service',
            'symptom': 'Symptom'
        }
        mapped_columns = []
        for term, col in column_mapping.items():
            if term in query.lower() and col in data.columns:
                mapped_columns.append(col)
        return mapped_columns

    def generate_chart(self, data, columns, chart_type, filters=None):
        """Generate a chart based on parsed query."""
        if filters:
            # Handle date filter
            if 'date' in filters and 'from' in filters['date']:
                try:
                    date_filter = pd.to_datetime(filters['date'].replace("from", "").strip())
                    data = data[data['Date'] >= date_filter]
                except Exception as e:
                    return f"Error parsing date filter: {e}"

        # Ensure 'Frequency' column exists by grouping data
        if 'YearMonth' in columns:
            data = data.groupby('YearMonth').size().reset_index(name='Frequency')
        elif columns:
            data = data.groupby(columns[0]).size().reset_index(name='Frequency')
        else:
            return "Invalid query: no columns mapped for aggregation."

        # Generate the appropriate chart
        if chart_type == 'bar':
            fig = px.bar(data, x=columns[0], y='Frequency', title=f"{columns[0]} Frequency")
        elif chart_type == 'line':
            fig = px.line(data, x=columns[0], y='Frequency', title=f"{columns[0]} Trend Over Time")
        else:
            return "Unsupported chart type."

        return fig


    def generate_response(self, query, context):
        """Generate a text response using GPT with the retrieved context."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant analyzing incident data."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()

    def handle_query(self, query, data, context):
        """Handle user query and determine whether to generate a response or a chart."""
        analysis_result = self.analyze_query(query)

        if not analysis_result:
            # Fallback logic for common patterns
            if "monthly" in query.lower() and "incident" in query.lower():
                analysis_result = {'action': 'plot', 'subject': 'monthly incident count', 'chart_type': 'bar', 'filters': None}
            elif "root cause" in query.lower() and "frequency" in query.lower():
                analysis_result = {'action': 'plot', 'subject': 'root cause frequency', 'chart_type': 'bar', 'filters': None}
            else:
                #return "Sorry, I couldn't understand your query."
                return self.generate_response(query, context)

        action = analysis_result.get('action', '').lower()
        subject = analysis_result.get('subject', '')
        chart_type = analysis_result.get('chart_type', 'bar')
        filters = analysis_result.get('filters', None)
        columns = self.map_columns(query, data)

        # if not columns:
        #     return "I couldn't map any relevant columns for your query."

        if 'show' in action or 'plot' in action:
            return self.generate_chart(data, columns, chart_type, filters)
        else:
            return self.generate_response(query, context)
