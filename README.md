# Prescription Recognition and Chatbot Streamlit App

This Streamlit application allows users to upload medical prescriptions for text extraction and interact with a chatbot to get information about medicines. The app combines Optical Character Recognition (OCR) for text extraction with a chatbot powered by a large language model (LLM) and a medicine database.

<h2> Local installation Steps:</h2>

<p>1. Clone the repository</p>

```
git clone https://github.com/aditya-patil-00/medical-prescription-app.git
```

<p>2. Setup virtual environment</p>

```
python -m venv myenv 
```

<p>3. Install requirements.txt</p>

```
pip install -r requirements.txt
```

<p>4. Run the app</p>

```
streamlit run app.py
```

## Features

- **Prescription Upload**: Users can upload prescription images in JPG, JPEG, or PNG formats.
- **Text Extraction**: Utilizes Tesseract-OCR (`pytesseract`) to extract text from prescription images.
- **Chatbot Interaction**: Chatbot powered by Llama 3.1 processes user queries and provides responses related to medicines.
- **Medicine Information Retrieval**: Retrieves and displays information about medicines from an SQLite database.
- **User-Friendly Interface**: Built with Streamlit for an intuitive user experience.
- **Real-Time Processing**: Provides real-time text extraction and chatbot responses.
- **Error Handling**: Includes error handling for text extraction and database queries to ensure a smooth user experience.

### Architecture Diagram

```mermaid
graph TD
    A[User] -->|Interacts with| B[Streamlit Frontend]
    B -->|Uploads prescription| C[OCR Module]
    B -->|Sends chat messages| D[Chatbot Module]
    B -->|Queries medicine info| E[Medicine Database Module]
    C -->|Extracts text| F[OCR Engine]
    D -->|Processes queries| G[LLM]
    E -->|Queries| H[(Medicine Database)]
    C -->|Returns recognized text| B
    D -->|Returns responses| B
    E -->|Returns medicine info| B
