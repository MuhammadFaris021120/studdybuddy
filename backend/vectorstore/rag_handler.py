import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("SUBSCRIPTION_KEY"),
    api_version=os.getenv("API_VERSION")
)

def store_and_query_vector(text, question):
    # Simple RAG without file upload yet
    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT"),
        messages=[
            {"role": "system", "content": "You are an assistant that answers questions from a document."},
            {"role": "user", "content": f"Document:\n{text}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content
