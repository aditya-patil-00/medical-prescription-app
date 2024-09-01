from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv('API_KEY')

# Create an OpenAI client with your DeepInfra token and endpoint
openai = OpenAI(
    api_key=api_key,
    base_url="https://api.deepinfra.com/v1/openai",
)

def ask_medical_question(question):
    # Define the conversation messages
    messages = [
        {"role": "system", "content": "You are a medical AI assistant. You have to answer questions related to certain medicines."},
        {"role": "user", "content": question},
    ]

    # Create a chat completion request
    chat_completion = openai.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=messages,
    )

    # Return the assistant's response and token usage
    response = chat_completion.choices[0].message.content
    prompt_tokens = chat_completion.usage.prompt_tokens
    completion_tokens = chat_completion.usage.completion_tokens

    return response, prompt_tokens, completion_tokens

# Example usage:
if __name__ == "__main__":
    question = "What is the typical dosage of aspirin?"
    response, prompt_tokens, completion_tokens = ask_medical_question(question)
    
    print("Assistant's response:", response)
    print("Prompt tokens:", prompt_tokens)
    print("Completion tokens:", completion_tokens)