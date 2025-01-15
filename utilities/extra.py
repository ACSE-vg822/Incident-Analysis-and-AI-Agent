from openai import OpenAI

client = OpenAI(api_key=api_key)

class Chatbot:
    def __init__(self, api_key, model="gpt-4"):
        self.model = model

    def generate_response(self, query, context):
        """Generate a response using GPT with the retrieved context."""
        messages = [
            {"role": "system", "content": "You are a helpful assistant analyzing incident data."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
        response = client.chat.completions.create(model=self.model,
        messages=messages,
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()
