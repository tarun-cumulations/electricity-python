import psycopg2
from psycopg2 import sql


db_params = {
    'dbname': 'postgres', 
    'user': 'postgres', 
    'password': 'postgres', 
    'host': 'postgres.cox4boq5aldo.ap-south-1.rds.amazonaws.com' 
}


conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Create tables
try:
    # Applicant Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applicant (
        applicant_id SERIAL PRIMARY KEY,
        applicant_name VARCHAR(255),
        gender VARCHAR(50),
        district VARCHAR(255),
        state VARCHAR(255),
        pincode INTEGER,
        ownership VARCHAR(255),
        govtid_type VARCHAR(255),
        id_number VARCHAR(255)
    );
    """)

    # Application Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS application (
        application_id SERIAL PRIMARY KEY,
        applicant_id INTEGER REFERENCES applicant(applicant_id),
        category VARCHAR(255),
        load_applied INTEGER,
        date_of_application DATE,
        date_of_approval DATE,
        modified_date DATE,
        status VARCHAR(255)
    );
    """)

    # Reviewer Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviewer (
        reviewer_id SERIAL PRIMARY KEY,
        reviewer_name VARCHAR(255)
    );
    """)

    # Review Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review (
        review_id SERIAL PRIMARY KEY,
        application_id INTEGER REFERENCES application(application_id),
        reviewer_id INTEGER REFERENCES reviewer(reviewer_id),
        reviewer_comments TEXT
    );
    """)

    conn.commit()
    print("Tables created successfully")
except Exception as e:
    print("An error occurred:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()

