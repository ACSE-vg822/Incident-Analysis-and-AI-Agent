import pandas as pd
import faiss
from openai import OpenAI

import numpy as np
from data_handler import DataLoader
import streamlit as st
import os

class DataIndexer:
    def __init__(self, api_key, index_file='incident_index.faiss'):
        """Initialize the DataIndexer with the specified index file path."""
        self.index_file = os.path.join('index', index_file)  # Save in the 'index' folder
        self.index = None
        self.client = OpenAI(api_key=api_key)

    def embed_text(self, text):
        """Generate embeddings using OpenAI API (new syntax for v1.0.0+)."""
        response = self.client.embeddings.create(model="text-embedding-ada-002", input=[text])
        return response.data[0].embedding

    def embed_and_index(self, data, column):
        """Embed data and store in a FAISS index."""
        if column not in data.columns:
            raise KeyError(f"Column '{column}' not found in dataset. Available columns: {data.columns}")

        embeddings = []
        for text in data[column]:
            embeddings.append(self.embed_text(text))

        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]

        # Create FAISS index
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        print(f"Number of embeddings in FAISS index: {self.index.ntotal}")
        # Save the index
        faiss.write_index(self.index, self.index_file)
        print(f"Index saved to {self.index_file}")

# Example usage:
if __name__ == "__main__":
    # Load data for chatbot context
    data_loader = DataLoader()
    data = data_loader.load_data()

    # Combine columns to create 'incident_description'
    data['incident_description'] = (
        data['Summary'].fillna('') + ' ' +
        data['Impact'].fillna('') + ' ' +
        data['Detection'].fillna('') + ' ' +
        data['Timeline'].fillna('') + ' ' +
        data['Conclusions'].fillna('') + ' ' +
        data['Actionables'].fillna('')
    ).str.strip()

    print("Sample data with incident_description:\n", data[['incident_description']].head())

    # Embed and index the data
    api_key = st.secrets["general"]["OPENAI_API_KEY"]
    indexer = DataIndexer(api_key=api_key)
    indexer.embed_and_index(data, column='incident_description')

