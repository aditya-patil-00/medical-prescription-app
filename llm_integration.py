from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('API_KEY')

# Create an OpenAI client with your DeepInfra token and endpoint
openai = OpenAI(
    api_key=api_key,
    base_url="https://api.deepinfra.com/v1/openai",
)

# Define the conversation messages
messages = [
    {"role": "system", "content": "You are a medical AI assistant. You have to answer questions related to certain medicines."},
    {"role": "user", "content": "What is the typical dosage of aspirin?"},
]

# Create a chat completion request
chat_completion = openai.chat.completions.create(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    messages=messages,
)

# Print the assistant's response
print(chat_completion.choices[0].message.content)

# Print token usage (if available)
print("Prompt tokens:", chat_completion.usage.prompt_tokens)
print("Completion tokens:", chat_completion.usage.completion_tokens)
