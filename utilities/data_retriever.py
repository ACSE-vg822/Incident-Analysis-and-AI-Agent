import faiss
from openai import OpenAI
import numpy as np
import pandas as pd
import os
import streamlit as st

#api_key = st.secrets["general"]["OPENAI_API_KEY"]
#client = OpenAI(api_key=api_key)

class DataRetriever:
    def __init__(self, api_key, index_file='index/incident_index.faiss'):
        """
        Initialize the DataRetriever with the FAISS index file and OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)

        # Ensure the index path is correct and use os.path for compatibility
        self.index_file = os.path.abspath(index_file)  # Get absolute path
        if not os.path.exists(self.index_file):
            raise FileNotFoundError(f"FAISS index file not found at {self.index_file}")
        # Load the FAISS index
        self.index = faiss.read_index(self.index_file)
        print(f"Loaded FAISS index from {self.index_file}")

    def embed_query(self, query):
        """Generate query embedding using OpenAI API."""
        response = self.client.embeddings.create(model="text-embedding-ada-002", input=[query])
        return np.array(response.data[0].embedding, dtype='float32')

    def retrieve(self, query, data, top_k=5):#5):
        """Retrieve the most relevant records based on the query."""
        query_embedding = self.embed_query(query).reshape(1, -1)
        if top_k is None:
            top_k = self.index.ntotal 
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Retrieve the relevant rows from the dataset
        # return data.iloc[indices[0]].to_dict(orient='records')
        # Extract relevant rows and dynamically construct incident_description
        records = data.iloc[indices[0]].to_dict(orient='records')
        for record in records:
            record['incident_description'] = (
                f"Summary: {record.get('Summary', 'N/A')}\n"
                f"Impact: {record.get('Impact', 'N/A')}\n"
                f"Detection: {record.get('Detection', 'N/A')}\n"
                f"Timeline: {record.get('Timeline', 'N/A')}\n"
                f"Conclusions: {record.get('Conclusions', 'N/A')}\n"
                f"Actionables: {record.get('Actionables', 'N/A')}"
            )
        return records
# Example usage
if __name__ == "__main__":
    data = pd.read_csv("parsed_incident_reports.csv")
    retriever = DataRetriever(api_key="your_openai_api_key")
    query = "What caused the MediaWiki outage?"
    results = retriever.retrieve(query, data)
    for result in results:
        print(result)
