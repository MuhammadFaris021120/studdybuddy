from openai import AzureOpenAI
import os

client = AzureOpenAI(
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("SUBSCRIPTION_KEY"),
    api_version=os.getenv("API_VERSION")
)

def generate_quiz(text):
    prompt = f"""
    Generate 3 quiz questions with multiple choice answers (A, B, C, D) based on the following content:
    
    {text}

    Format:
    1. Question?
    A. ...
    B. ...
    C. ...
    D. ...
    Answer: ...
    """
    response = client.chat.completions.create(
        model=os.getenv("DEPLOYMENT"),
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
