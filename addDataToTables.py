import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv 


load_dotenv()


db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST')
}



# # Sample data to be inserted
# applicants = [
#     ("John Doe", "Male", "North", "Delhi", 110001, "Individual", "Aadhar", "123456789012"),
#     ("Jane Smith", "Female", "South", "Delhi", 110002, "Joint", "Voter ID", "V1234567")
# ]

# reviewers = [
#     ("Reviewer A",),
#     ("Reviewer B",)
# ]

# # Connect to the database
# conn = psycopg2.connect(**db_params)
# cursor = conn.cursor()

# try:
#     # Insert data into applicant table and retrieve the generated IDs
#     applicant_ids = []
#     for applicant in applicants:
#         cursor.execute("""
#             INSERT INTO applicant (applicant_name, gender, district, state, pincode, ownership, govtid_type, id_number)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING applicant_id;
#         """, applicant)
#         applicant_ids.append(cursor.fetchone()[0])

#     # Now that we have applicant IDs, we can insert data into the application table
#     applications = [
#         (applicant_ids[0], "Residential", 10, datetime(2021, 1, 15), datetime(2021, 1, 20), datetime(2021, 1, 18), "Approved"),
#         (applicant_ids[1], "Commercial", 15, datetime(2021, 2, 10), None, datetime(2021, 2, 12), "Pending")
#     ]

#     for application in applications:
#         cursor.execute("""
#             INSERT INTO application (applicant_id, category, load_applied, date_of_application, date_of_approval, modified_date, status)
#             VALUES (%s, %s, %s, %s, %s, %s, %s);
#         """, application)

#     # Insert data into reviewer table
#     for reviewer in reviewers:
#         cursor.execute("""
#             INSERT INTO reviewer (reviewer_name)
#             VALUES (%s);
#         """, reviewer)

#     # Commit the transaction
#     conn.commit()
#     print("Data inserted successfully")
# except Exception as e:
#     print("An error occurred:", e)
#     conn.rollback()
# finally:
#     cursor.close()
#     conn.close()



# Expanded sample data to be inserted
# applicants = [
#     ("John Doe", "Male", "North", "Delhi", 110001, "Individual", "Aadhar", "123456789012"),
#     ("Jane Smith", "Female", "South", "Delhi", 110002, "Joint", "Voter ID", "V1234567"),
#     ("Alice Johnson", "Female", "East", "Delhi", 110003, "Individual", "PAN", "ABCDE1234F"),
#     ("Bob Brown", "Male", "West", "Delhi", 110004, "Individual", "Passport", "P12345678")
# ]

# applications = [
#     (1, "Residential", 10, datetime(2021, 1, 15), datetime(2021, 1, 20), datetime(2021, 1, 18), "Approved"),
#     (2, "Commercial", 15, datetime(2021, 2, 10), None, datetime(2021, 2, 12), "Pending"),
#     (3, "Residential", 5, datetime(2021, 3, 22), None, datetime(2021, 3, 24), "Pending"),
#     (4, "Industrial", 50, datetime(2021, 4, 5), None, datetime(2021, 4, 7), "KYC failed")
# ]

# reviewers = [
#     ("Rahul singh",),
#     ("hem chand",),
#     ("vinod gupta",),
#     ("Manoj pandey",)
# ]

# applicants = [
#     ("Michael Johnson", "Male", "Central", "Delhi", 110001, "Individual", "Aadhar", "111122223333"),
#     ("Sara Khan", "Female", "North", "Delhi", 110005, "Individual", "Voter ID", "BBBCC1234"),
#     ("Raj Malhotra", "Male", "South", "Delhi", 110017, "Joint", "PAN", "ABCDE1234F"),
#     ("Anita Desai", "Female", "East", "Delhi", 110019, "Individual", "Passport", "K12345678")
# ]

# applications = [
#     (1, "Residential", 10, datetime(2021, 1, 15), datetime(2021, 1, 20), datetime(2021, 1, 18), "Approved"),
#     (2, "Commercial", 20, datetime(2021, 2, 5), None, datetime(2021, 2, 7), "Pending"),
#     (3, "Industrial", 50, datetime(2021, 3, 10), None, datetime(2021, 3, 12), "Pending"),
#     (4, "Residential", 15, datetime(2021, 4, 1), datetime(2021, 4, 5), datetime(2021, 4, 3), "Denied")
# ]

# reviewers = [
#     ("Rajesh Kumar",),
#     ("Priya Singh",),
#     ("Amit Verma",),
#     ("Neeta Gupta",)
# ]


# # Connect to the database
# conn = psycopg2.connect(**db_params)
# cursor = conn.cursor()

# try:
#     # Insert data into applicant table and retrieve the generated IDs
#     applicant_ids = []
#     for applicant in applicants:
#         cursor.execute("""
#             INSERT INTO applicant (applicant_name, gender, district, state, pincode, ownership, govtid_type, id_number)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING applicant_id;
#         """, applicant)
#         applicant_ids.append(cursor.fetchone()[0])

#     # Now that we have applicant IDs, we can insert data into the application table
#     for application in applications:
#         cursor.execute("""
#             INSERT INTO application (applicant_id, category, load_applied, date_of_application, date_of_approval, modified_date, govtstatus)
#             VALUES (%s, %s, %s, %s, %s, %s, %s);
#         """, (applicant_ids[application[0]-1],) + application[1:])

#     # Insert data into reviewer table
#     for reviewer in reviewers:
#         cursor.execute("""
#             INSERT INTO reviewer (reviewer_name)
#             VALUES (%s);
#         """, reviewer)

#     # Commit the transaction
#     conn.commit()
#     print("Data inserted successfully")
# except Exception as e:
#     print("An error occurred:", e)
#     conn.rollback()
# finally:
#     cursor.close()
#     conn.close()

# Sample data to be inserted
applicants = [
    ("Amanoj", "Male", "Central", "Delhi", 110021, "Individual", "Aadhar", "AADHAR1237"),
    ("sharadha", "Female", "North", "Delhi", 110022, "Joint", "Voter ID", "VOTER1238"),
    ("Acikas", "Male", "South", "Delhi", 110023, "Individual", "Aadhar", "AADHAR1239"),
    ("vimala", "Female", "East", "Delhi", 110024, "Individual", "Voter ID", "VOTER1240")
]


applications = [
    (7, "Residential", 10, datetime(2021, 1, 15), datetime(2021, 1, 20), datetime(2021, 1, 18), "Approved"),
    (8, "Commercial", 15, datetime(2021, 2, 10), None, datetime(2021, 2, 12), "Pending"),
    (9, "Commercial", 200, datetime(2021, 1, 15), datetime(2021, 1, 20), datetime(2021, 1, 18), "Pending"),
    (10, "Commercial", 15, datetime(2021, 2, 10), None, datetime(2021, 2, 12), "Pending")
]


reviewers = [
    ("Rajesh Kumar",),
    ("Priya Singh",),
    ("Amit Verma",),
    ("Neeta Gupta",)
]


reviews = [
    (5, 1, "Application complete and approved."),
    (6, 2, "Application pending, awaiting additional documentation."),
    (7, 3, "Application under review, site inspection pending."),
    (8, 4, "Application pending further review.")
]


# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

try:
    # Insert data into the applicant table
    for applicant in applicants:
        cursor.execute("""
            INSERT INTO applicant (applicant_name, gender, district, state, pincode, ownership, govtid_type, id_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING applicant_id;
        """, applicant)

    # Insert data into the application table
    for application in applications:
        cursor.execute("""
            INSERT INTO application (applicant_id, category, load_applied, date_of_application, date_of_approval, modified_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, application)

    # Insert data into the reviewer table
    for reviewer in reviewers:
        cursor.execute("""
            INSERT INTO reviewer (reviewer_name)
            VALUES (%s);
        """, reviewer)

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