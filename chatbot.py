from openai import OpenAI
import pandas as pd
import streamlit as st

# Get API key from Streamlit secrets
api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Set up OpenAI client
client = OpenAI(api_key=api_key)

def ask_gpt(question, context):
    """
    Query GPT with a question and dataset context.

    Args:
        question (str): The user's question.
        context (str): Dataset context to provide to the model.

    Returns:
        str: The response from GPT.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Adjust model version as needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing datasets."},
                {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error querying GPT: {str(e)}")
        return "An error occurred while querying the AI model."

def get_dataset_context(data):
    """
    Create a summary of the dataset to provide as context for GPT.

    Args:
        data (DataFrame): The dataset.

    Returns:
        str: A string representation of the dataset context.
    """
    return data.head(10).to_string(index=False)  # Example: Use the first 10 rows for context
