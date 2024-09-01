from llama_index.llms.llama_api import LlamaAPI
import os
from dotenv import load_dotenv
from llama_index.core.llms import ChatMessage

load_dotenv()

api_key = os.getenv("API_KEY")

llm = LlamaAPI(api_key=api_key)

def chat_with_model(question):
    try:
        messages = [
        ChatMessage(
            role="system", content="You are a medical AI assistant. You have to answer questions related to certain medicines."
            ),
        ChatMessage(role="user", content=question),]
        resp = llm.chat(messages)

    except Exception as e:
        return f"An error occurred: {str(e)}"

# For testing
if __name__ == "__main__":
    print(chat_with_model("what is typical dosage of aspirin?"))