

import psycopg2
from datetime import datetime

# Database connection parameters
db_params = {
    
}

# Hardcoded data for applicants
applicants = [
    (1, "MICHAEL", "Male", "North", "DELHI", 110028, "JOINT", "AADHAR"),
    (2, "DAVID", "Male", "South", "DELHI", 110007, "INDIVIDUAL", "VOTER_ID"),
    (3, "JOHN", "Male", "East", "DELHI", 110065, "INDIVIDUAL", "PAN"),
    # ... add more rows as needed
]

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

try:
    # Insert data into the applicant table
    for applicant in applicants:
        cursor.execute("""
            INSERT INTO applicant (applicant_id, applicant_name, gender, district, state, pincode, ownership, govtid_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (applicant_id) DO NOTHING;
        """, applicant)

    # Commit the transaction
    conn.commit()
    print("Applicant data inserted successfully")

except Exception as e:
    print("An error occurred:", e)
    conn.rollback()
finally:
    cursor.close()
    conn.close()
