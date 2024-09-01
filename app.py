import streamlit as st
import sqlite3
from PIL import Image
import io
from ocr_text import ocr_detection
from llm_integration import ask_medical_question
from db_management import create_connection, create_table, insert_initial_data, update_or_insert_medicine, get_medicine_info
import os

def main():
    st.title("Medical Information App")

    # Initialize database
    conn = create_connection()
    create_table(conn)
    insert_initial_data(conn)

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a page", ["OCR", "LLM Query", "Database Management"])

    if page == "OCR":
        st.header("OCR - Extract Text from Image")
        uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            if st.button("Extract Text"):
                extracted_text = ocr_detection(image)
                st.subheader("Extracted Text:")
                st.write(extracted_text)

    elif page == "LLM Query":
        st.header("LLM Query - Ask about Medicines")
        query = st.text_input("Enter your question about a medicine:")
        if st.button("Ask LLM"):
            response, prompt_tokens, completion_tokens = ask_medical_question(query)
            st.subheader("LLM Response:")
            st.write(response)
            st.write(f"Prompt tokens: {prompt_tokens}")
            st.write(f"Completion tokens: {completion_tokens}")

    elif page == "Database Management":
        st.header("Database Management")
        
        # Display all medicines
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medicines")
        medicines = cursor.fetchall()
        
        st.subheader("Current Medicines in Database:")
        for medicine in medicines:
            st.write(f"ID: {medicine[0]}, Name: {medicine[1]}")
        
        # Add or update medicine
        st.subheader("Add or Update Medicine")
        medicine_name = st.text_input("Enter medicine name:")
        if st.button("Add/Update Medicine"):
            medicine_id = update_or_insert_medicine(conn, medicine_name)
            st.success(f"Medicine '{medicine_name}' added/updated with ID: {medicine_id}")
        
        # Retrieve medicine info
        st.subheader("Retrieve Medicine Information")
        medicine_id = st.number_input("Enter medicine ID:", min_value=1, step=1)
        if st.button("Get Info"):
            medicine_info = get_medicine_info(conn, medicine_id)
            if medicine_info:
                st.write(f"ID: {medicine_info[0]}")
                st.write(f"Name: {medicine_info[1]}")
                st.write(f"Dosage: {medicine_info[2]}")
                st.write(f"Description: {medicine_info[3]}")
            else:
                st.error("Medicine not found")

    conn.close()

if __name__ == "__main__":
    main()
