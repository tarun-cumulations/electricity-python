import psycopg2
import os
from dotenv import load_dotenv 
from datetime import datetime

load_dotenv()

db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST')
}

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Sample data for each table
applicants = [
    ("Amanoj", "Male", "Central", "Delhi", 110021, "Individual", "Aadhar", "AADHAR1237"),
    ("Sharadha", "Female", "North", "Delhi", 110022, "Joint", "Voter ID", "VOTER1238"),
    ("Acikas", "Male", "South", "Delhi", 110023, "Individual", "Aadhar", "AADHAR1239"),
    ("Vimala", "Female", "East", "Delhi", 110024, "Individual", "Voter ID", "VOTER1240")
]

reviewers = [
    ("Rajesh Kumar",),
    ("Priya Singh",),
    ("Amit Verma",),
    ("Neeta Gupta",)
]

# Create tables and insert data
try:
    
    applicant_ids = []
    for applicant in applicants:
        cursor.execute("""
            INSERT INTO applicant (applicant_name, gender, district, state, pincode, ownership, govtid_type, id_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING applicant_id;
        """, applicant)
        applicant_id = cursor.fetchone()[0]
        applicant_ids.append(applicant_id)

    # Prepare applications data with actual applicant_ids
    applications = [
        (applicant_ids[0], "Residential", 10, "2021-01-15", "2021-01-20", "2021-01-18", "Approved"),
        (applicant_ids[1], "Commercial", 15, "2021-02-10", None, "2021-02-12", "Pending"),
        (applicant_ids[2], "Commercial", 200, "2021-01-15", "2021-01-20", "2021-01-18", "Pending"),
        (applicant_ids[3], "Commercial", 15, "2021-02-10", None, "2021-02-12", "Pending")
    ]

    # Insert data into the application table
    application_ids = []
    for application in applications:
        cursor.execute("""
            INSERT INTO application (applicant_id, category, load_applied, date_of_application, date_of_approval, modified_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING application_id;
        """, application)
        application_id = cursor.fetchone()[0]
        application_ids.append(application_id)

    # Insert data into the reviewer table
    for reviewer in reviewers:
        cursor.execute("""
            INSERT INTO reviewer (reviewer_name)
            VALUES (%s);
        """, reviewer)

    # Prepare reviews data
    reviews = [
    (application_ids[0], 1, "Application complete and approved."),
    (application_ids[1], 2, "Application pending, awaiting additional documentation."),
    (application_ids[2], 3, "Application under review, site inspection pending."),
    (application_ids[3], 4, "Application pending further review.")
    ]

    # Insert data into the review table
    for review in reviews:
        cursor.execute("""
            INSERT INTO review (application_id, reviewer_id, reviewer_comments)
            VALUES (%s, %s, %s);
        """, review)

    # Commit the transaction
    conn.commit()
    print("Data inserted successfully")

except Exception as e:
    print("An error occurred:", e)
    conn.rollback()

finally:
    cursor.close()
    conn.close()
