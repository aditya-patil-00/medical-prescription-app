import sqlite3
from llm_integration import ask_medical_question
import re

def create_connection():
    conn = sqlite3.connect('medical_database.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        dosage TEXT,
        description TEXT
    )
    ''')
    conn.commit()

def insert_initial_data(conn):
    initial_data = [
        (1, 'Aspirin', '325-650 mg every 4-6 hours as needed, not to exceed 4,000 mg per day. Take with food to reduce stomach upset.', 'Aspirin is a nonsteroidal anti-inflammatory drug (NSAID) used to relieve pain, reduce fever, and as a blood thinner. It is commonly used for headaches, minor aches, and to prevent heart attacks and strokes in high-risk individuals.'),
        (2, 'Ibuprofen', '200-400 mg every 4-6 hours as needed, not to exceed 1,200 mg per day unless directed by a doctor. Take with food or milk to prevent stomach upset.', 'Ibuprofen is a nonsteroidal anti-inflammatory drug (NSAID) used to reduce fever and treat pain or inflammation caused by headaches, toothaches, back pain, arthritis, menstrual cramps, or minor injuries.'),
        (3, 'Acetaminophen', '325-650 mg every 4-6 hours as needed, not to exceed 3,000 mg per day. Can be taken with or without food.', 'Acetaminophen is a pain reliever and fever reducer used to treat mild to moderate pain from headaches, muscle aches, menstrual periods, colds and sore throats, toothaches, backaches, and reactions to vaccinations.'),
        (4, 'Amoxicillin', '250-500 mg every 8 hours, or 500-875 mg every 12 hours, taken orally for 7-10 days depending on the type and severity of infection.', 'Amoxicillin is a penicillin-type antibiotic used to treat a wide variety of bacterial infections such as bronchitis, pneumonia, tonsillitis, and infections of the ear, nose, throat, skin, or urinary tract.'),
        (5, 'Lisinopril', '10-40 mg once daily, with or without food. The dosage may be adjusted based on blood pressure response.', 'Lisinopril is an ACE inhibitor used to treat high blood pressure (hypertension), congestive heart failure, and to improve survival after a heart attack. It works by relaxing blood vessels to lower blood pressure and improve blood flow.'),
        (6, 'Metformin', '500-1000 mg twice daily with meals, or 850 mg once daily with a meal. The dosage may be gradually increased to reduce gastrointestinal side effects.', 'Metformin is an oral diabetes medication that helps control blood sugar levels in patients with type 2 diabetes. It works by decreasing glucose production in the liver and increasing the sensitivity of body to insulin.'),
        (7, 'Levothyroxine', '50-100 mcg once daily on an empty stomach, 30-60 minutes before breakfast. Dosage is individualized based on lab results and patient response.', 'Levothyroxine is a thyroid hormone replacement medication used to treat hypothyroidism (low thyroid hormone). It replaces or provides more thyroid hormone, which is normally produced by the thyroid gland.'),
        (8, 'Atorvastatin', '10-80 mg once daily, with or without food. The starting dose is usually 10-20 mg, which may be adjusted based on cholesterol levels and response.', 'Atorvastatin is a statin medication used to lower cholesterol and triglycerides in the blood. It works by blocking an enzyme that produces cholesterol in the liver, thereby reducing the risk of heart disease and stroke.'),
        (9, 'Omeprazole', '20-40 mg once daily before a meal, typically in the morning. For severe cases, up to 120 mg daily may be given in divided doses.', 'Omeprazole is a proton pump inhibitor (PPI) used to treat various stomach and esophagus problems such as acid reflux and ulcers. It works by decreasing the amount of acid produced in the stomach.'),
        (10, 'Sertraline', '50-200 mg once daily, either in the morning or evening. Starting dose is usually 50 mg, which may be increased gradually based on response.', 'Sertraline is a selective serotonin reuptake inhibitor (SSRI) antidepressant used to treat depression, obsessive-compulsive disorder, panic attacks, post-traumatic stress disorder, and social anxiety disorder.')
    ]
    
    cursor = conn.cursor()
    cursor.executemany('INSERT OR REPLACE INTO medicines (id, name, dosage, description) VALUES (?, ?, ?, ?)', initial_data)
    conn.commit()

def parse_llm_response(response):
    # Use regular expressions to find the dosage and description
    dosage_match = re.search(r'1\.\s*Typical adult dosage:\s*(.*?)(?=2\.|\Z)', response, re.DOTALL)
    description_match = re.search(r'2\.\s*Brief description:\s*(.*)', response, re.DOTALL)

    dosage = dosage_match.group(1).strip() if dosage_match else "Unknown"
    description = description_match.group(1).strip() if description_match else "No description available"

    return dosage, description

def update_or_insert_medicine(conn, medicine_name):
    cursor = conn.cursor()
    
    # Check if the medicine already exists
    cursor.execute('SELECT id FROM medicines WHERE name = ?', (medicine_name,))
    result = cursor.fetchone()
    
    if result:
        medicine_id = result[0]
    else:
        cursor.execute('SELECT MAX(id) FROM medicines')
        max_id = cursor.fetchone()[0]
        medicine_id = max_id + 1 if max_id else 1
    
    # Ask LLM for dosage and description with an improved prompt
    question = f"""Provide information about {medicine_name} in the following format:
1. Typical adult dosage (1 line)
2. Brief description (1 line)
Please be concise and factual."""

    response, _, _ = ask_medical_question(question)
    
    # Parse the response using the simplified function
    dosage, description = parse_llm_response(response)
    
    # Update or insert the medicine
    cursor.execute('''
    INSERT OR REPLACE INTO medicines (id, name, dosage, description)
    VALUES (?, ?, ?, ?)
    ''', (medicine_id, medicine_name, dosage, description))
    
    conn.commit()
    return medicine_id

def get_medicine_info(conn, medicine_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM medicines WHERE id = ?', (medicine_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    conn = create_connection()
    create_table(conn)
    insert_initial_data(conn)
    
    # Example usage
    medicine_name = "Ciprofloxacin"
    medicine_id = update_or_insert_medicine(conn, medicine_name)
    print(f"Updated/Inserted medicine with ID: {medicine_id}")
    
    medicine_info = get_medicine_info(conn, medicine_id)
    print(f"Medicine Info: {medicine_info}")
    
    conn.close()