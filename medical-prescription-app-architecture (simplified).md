
graph TD
    A[User] -->|Interacts with| B[Streamlit Frontend]
    B -->|Uploads prescription| C[OCR Module]
    B -->|Sends chat messages| D[Chatbot Module]
    B -->|Queries medicine info| E[Medicine Database Module]
    C -->|Extracts text| F[OCR Engine]
    D -->|Processes queries| G[OpenAI GPT]
    E -->|Queries| H[(Medicine Database)]
    C -->|Returns recognized text| B
    D -->|Returns responses| B
    E -->|Returns medicine info| B
