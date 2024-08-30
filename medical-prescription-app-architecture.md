graph TD
    A[User] -->|Interacts with| B[Frontend Web Interface]
    B -->|Uploads prescription| C[API Gateway]
    B -->|Sends chat messages| C
    C -->|Routes requests| D[OCR Service]
    C -->|Routes requests| E[Chatbot Service]
    C -->|Routes requests| F[Medicine Database Service]
    D -->|Extracts text| G[OCR Engine]
    E -->|Processes queries| H[OpenAI GPT]
    F -->|Queries| I[(Medicine Database)]
    D -->|Sends recognized text| C
    E -->|Sends responses| C
    F -->|Sends medicine info| C
    C -->|Returns results| B