import calendar
from datetime import datetime
from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv 
from flask_cors import CORS
load_dotenv()
app = Flask(__name__)

cors = CORS(app)

# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'host': os.getenv('DB_HOST')
}

def get_db_connection():
    conn = psycopg2.connect(**db_params)
    return conn

#  http://127.0.0.1:5000/applications/search?applicantId=7

# @app.route('/applications/search', methods=['GET'])
# def search_applications():
#     applicant_id = request.args.get('applicantId', type=int)

#     if not applicant_id:
#         return jsonify({'error': 'Applicant ID is required'}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute('SELECT * FROM application WHERE applicant_id = %s', (applicant_id,))
#     applications = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return jsonify(applications)


@app.route('/applications/search', methods=['GET'])
def search_applications():
    applicant_id = request.args.get('applicantId', type=int)

    if not applicant_id:
        return jsonify({'error': 'Applicant ID is required'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT app.application_id, app.applicant_id, ap.applicant_name, app.category, app.load_applied, 
                   app.date_of_application, app.date_of_approval, app.modified_date, app.status, 
                   ap.govtid_type, rev.review_id, revr.reviewer_name, rev.reviewer_comments
            FROM application app
            JOIN applicant ap ON app.applicant_id = ap.applicant_id
            LEFT JOIN review rev ON app.application_id = rev.application_id
            LEFT JOIN reviewer revr ON rev.reviewer_id = revr.reviewer_id
            WHERE app.applicant_id = %s
            ORDER BY app.application_id
        """, (applicant_id,))
        applications = cursor.fetchall()

        cursor.close()
        conn.close()

        applications_data = [
            {
                "application_id": app[0],
                "applicant_id": app[1],
                "applicant_name": app[2],
                "category": app[3],
                "load_applied": app[4],
                "date_of_application": app[5].strftime("%Y-%m-%d") if app[5] else None,
                "date_of_approval": app[6].strftime("%Y-%m-%d") if app[6] else None,
                "modified_date": app[7].strftime("%Y-%m-%d") if app[7] else None,
                "status": app[8],
                "govt_id_type": app[9],
                "review_id": app[10],
                "reviewer_name": app[11],
                "reviewer_comments": app[12]
            }
            for app in applications
        ]

        return jsonify(applications_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# http://localhost:5000/applications/filter?startDate=2021-01-01&endDate=2021-02-02
@app.route('/applications/filter', methods=['GET'])
def filter_applications():
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    if not start_date or not end_date:
        return jsonify({'error': 'Both startDate and endDate are required'}), 400

    start_date = format_date(start_date)
    end_date = format_date(end_date)

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM application 
        WHERE date_of_application BETWEEN %s AND %s
    """
    cursor.execute(query, (start_date, end_date))
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(applications)


# http://127.0.0.1:5000/applications

# @app.route('/applications', methods=['GET'])
# def get_applications():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     offset = (page - 1) * per_page

#     cursor.execute('SELECT COUNT(*) FROM application')
#     total = cursor.fetchone()[0]

#     cursor.execute('SELECT * FROM application ORDER BY application_id LIMIT %s OFFSET %s', (per_page, offset))
#     applications = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return jsonify({
#         'total': total,
#         'page': page,
#         'per_page': per_page,
#         'data': applications
#     })


# @app.route('/applications', methods=['GET'])
# def get_applications():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     offset = (page - 1) * per_page

#     cursor.execute('SELECT COUNT(*) FROM application')
#     total = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT app.application_id, app.applicant_id, app.category, app.load_applied, app.date_of_application, app.date_of_approval, app.modified_date, app.status, ap.govtid_type
#         FROM application app
#         JOIN applicant ap ON app.applicant_id = ap.applicant_id
#         ORDER BY app.application_id 
#         LIMIT %s OFFSET %s
#     """, (per_page, offset))
#     applications = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     applications_data = [
#         {
#             "application_id": app[0],
#             "applicant_id": app[1],
#             "category": app[2],
#             "load_applied": app[3],
#             "date_of_application": app[4],
#             "date_of_approval": app[5],
#             "modified_date": app[6],
#             "status": app[7],
#             "govt_id_type": app[8]
#         }
#         for app in applications
#     ]

#     return jsonify({
#         'total': total,
#         'page': page,
#         'per_page': per_page,
#         'data': applications_data
#     })


@app.route('/applications', methods=['GET'])
def get_applications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * per_page

    cursor.execute('SELECT COUNT(*) FROM application')
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT app.application_id, app.applicant_id, ap.applicant_name, app.category, app.load_applied, 
               app.date_of_application, app.date_of_approval, app.modified_date, app.status, 
               ap.govtid_type, rev.review_id, revr.reviewer_name, rev.reviewer_comments
        FROM application app
        JOIN applicant ap ON app.applicant_id = ap.applicant_id
        LEFT JOIN review rev ON app.application_id = rev.application_id
        LEFT JOIN reviewer revr ON rev.reviewer_id = revr.reviewer_id
        ORDER BY app.application_id 
        LIMIT %s OFFSET %s
    """, (per_page, offset))
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    applications_data = [
        {
            "application_id": app[0],
            "applicant_id": app[1],
            "applicant_name": app[2],
            "category": app[3],
            "load_applied": app[4],
            "date_of_application": app[5].strftime("%Y-%m-%d") if app[5] else None,
            "date_of_approval": app[6].strftime("%Y-%m-%d") if app[6] else None,
            "modified_date": app[7].strftime("%Y-%m-%d") if app[7] else None,
            "status": app[8],
            "govt_id_type": app[9],
            "review_id": app[10],
            "reviewer_name": app[11],
            "reviewer_comments": app[12] 
        }
        for app in applications
    ]

    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'data': applications_data
    })


# @app.route('/applications', methods=['GET'])
# def get_applications():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     offset = (page - 1) * per_page

#     cursor.execute('SELECT COUNT(*) FROM application')
#     total = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT app.application_id, app.applicant_id, ap.applicant_name, app.category, app.load_applied, 
#                app.date_of_application, app.date_of_approval, app.modified_date, app.status, 
#                ap.govtid_type, rev.review_id, revr.reviewer_name
#         FROM application app
#         JOIN applicant ap ON app.applicant_id = ap.applicant_id
#         LEFT JOIN review rev ON app.application_id = rev.application_id
#         LEFT JOIN reviewer revr ON rev.reviewer_id = revr.reviewer_id
#         ORDER BY app.application_id 
#         LIMIT %s OFFSET %s
#     """, (per_page, offset))
#     applications = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     applications_data = [
#         {
#             "application_id": app[0],
#             "applicant_id": app[1],
#             "applicant_name": app[2],  # Added applicant_name
#             "category": app[3],
#             "load_applied": app[4],
#             "date_of_application": app[5].strftime("%Y-%m-%d") if app[5] else None,
#             "date_of_approval": app[6].strftime("%Y-%m-%d") if app[6] else None,
#             "modified_date": app[7].strftime("%Y-%m-%d") if app[7] else None,
#             "status": app[8],
#             "govt_id_type": app[9],
#             "review_id": app[10],
#             "reviewer_name": app[11]
#         }
#         for app in applications
#     ]

#     return jsonify({
#         'total': total,
#         'page': page,
#         'per_page': per_page,
#         'data': applications_data
#     })




# @app.route('/applications', methods=['GET'])
# def get_applications():
#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     offset = (page - 1) * per_page

#     cursor.execute('SELECT COUNT(*) FROM application')
#     total = cursor.fetchone()[0]

#     cursor.execute("""
#         SELECT app.application_id, app.applicant_id, app.category, app.load_applied, app.date_of_application, 
#                app.date_of_approval, app.modified_date, app.status, ap.govtid_type, 
#                rev.review_id, revr.reviewer_name
#         FROM application app
#         JOIN applicant ap ON app.applicant_id = ap.applicant_id
#         LEFT JOIN review rev ON app.application_id = rev.application_id
#         LEFT JOIN reviewer revr ON rev.reviewer_id = revr.reviewer_id
#         ORDER BY app.application_id 
#         LIMIT %s OFFSET %s
#     """, (per_page, offset))
#     applications = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     applications_data = [
#         {
#             "application_id": app[0],
#             "applicant_id": app[1],
#             "category": app[2],
#             "load_applied": app[3],
#             "date_of_application": app[4],
#             "date_of_approval": app[5],
#             "modified_date": app[6],
#             "status": app[7],
#             "govt_id_type": app[8],
#             "review_id": app[9],
#             "reviewer_name": app[10]
#         }
#         for app in applications
#     ]

#     return jsonify({
#         'total': total,
#         'page': page,
#         'per_page': per_page,
#         'data': applications_data
#     })


# for below API 

# {
#     "category": "Commercial",
#     "load_applied": 200,
#     "status": "Pending",
#     "date_of_application":"01-01-23"
# }
# {
#     "error": "Some fields cannot be changed"
# }


# {
#     "category": "Commercial",
#     "load_applied": 250,
#     "status": "Pending"
# }
# {
#     "error": "Load applied should not exceed 200 KV"
# }


# @app.route('/applications/edit/<int:id>', methods=['PUT'])
# def edit_application(id):
#     data = request.json
#     if 'load_applied' in data and data['load_applied'] > 200:
#         return jsonify({'error': 'Load applied should not exceed 200 KV'}), 400

#     # Fields that should not be changed
#     immutable_fields = ['date_of_application', 'govtid_type', 'id_number']
#     if any(field in data for field in immutable_fields):
#         return jsonify({'error': 'Some fields cannot be changed'}), 400

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     columns = ', '.join([f"{key} = %s" for key in data])
#     values = list(data.values()) + [id]

#     query = f'UPDATE application SET {columns} WHERE application_id = %s'
#     cursor.execute(query, values)

#     conn.commit()

#     cursor.close()
#     conn.close()

#     return jsonify({'success': 'Application updated successfully'})



@app.route('/applications/edit/<int:id>', methods=['PUT'])
def edit_application(id):
    data = request.json

    if 'load_applied' in data and data['load_applied'] > 200:
        return jsonify({'error': 'Load applied should not exceed 200 KV'}), 400

    # Fields that should not be changed
    immutable_fields = ['date_of_application', 'govtid_type', 'id_number']
    if any(field in data for field in immutable_fields):
        return jsonify({'error': 'Some fields cannot be changed'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update fields in the application table
        application_fields = ['category', 'load_applied', 'date_of_approval', 'modified_date', 'status']
        application_data = {key: data[key] for key in application_fields if key in data}
        if application_data:
            columns = ', '.join([f"{key} = %s" for key in application_data])
            values = list(application_data.values()) + [id]
            cursor.execute(f'UPDATE application SET {columns} WHERE application_id = %s', values)

        # Update fields in the applicant table
        applicant_fields = ['applicant_name', 'gender', 'district', 'state', 'pincode', 'ownership']
        applicant_data = {key: data[key] for key in applicant_fields if key in data}
        if applicant_data:
            columns = ', '.join([f"{key} = %s" for key in applicant_data])
            values = list(applicant_data.values()) + [id]
            cursor.execute(f'UPDATE applicant SET {columns} WHERE applicant_id = (SELECT applicant_id FROM application WHERE application_id = %s)', values + [id])

        review_fields = ['reviewer_comments']
        review_data = {key: data[key] for key in review_fields if key in data}
        if review_data:
            columns = ', '.join([f"{key} = %s" for key in review_data])
            values = list(review_data.values()) + [id]
            cursor.execute(f'UPDATE review SET {columns} WHERE application_id = %s', values)

        conn.commit()
        return jsonify({'success': 'Application updated successfully'})

    except Exception as e:
        print(f"An error occurred: {e}")  
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()




# http://localhost:5000/applications/stats?status=Approved
# http://localhost:5000/applications/stats

# For monthly dashboard


@app.route('/applications/stats', methods=['GET'])
def get_application_stats():
    status = request.args.get('status', default='All')
    conn = get_db_connection()
    cursor = conn.cursor()

    if status == 'All':
        cursor.execute("""
            SELECT EXTRACT(MONTH FROM date_of_application) AS month, COUNT(*) 
            FROM application 
            GROUP BY month
            ORDER BY month;
        """)
    else:
        cursor.execute("""
            SELECT EXTRACT(MONTH FROM date_of_application) AS month, COUNT(*) 
            FROM application 
            WHERE status = %s
            GROUP BY month
            ORDER BY month;
        """, (status,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Transform results into a more friendly format
    stats = {calendar.month_name[int(month)]: count for month, count in results}

    return jsonify(stats)

def format_date(date_str):
    if not date_str:
        return None
    return datetime.strptime(date_str, '%Y-%m-%d').date()

if __name__ == '__main__':
    app.run(debug=True)
