import calendar
from datetime import datetime
from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv 
load_dotenv()
app = Flask(__name__)

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

@app.route('/applications/search', methods=['GET'])
def search_applications():
    applicant_id = request.args.get('applicantId', type=int)

    if not applicant_id:
        return jsonify({'error': 'Applicant ID is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM application WHERE applicant_id = %s', (applicant_id,))
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(applications)



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

@app.route('/applications', methods=['GET'])
def get_applications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * per_page

    cursor.execute('SELECT COUNT(*) FROM application')
    total = cursor.fetchone()[0]

    cursor.execute('SELECT * FROM application ORDER BY application_id LIMIT %s OFFSET %s', (per_page, offset))
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({
        'total': total,
        'page': page,
        'per_page': per_page,
        'data': applications
    })


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


@app.route('/applications/edit/<int:id>', methods=['PUT'])
def edit_application(id):
    data = request.json
    if 'load_applied' in data and data['load_applied'] > 200:
        return jsonify({'error': 'Load applied should not exceed 200 KV'}), 400

    # Fields that should not be changed
    immutable_fields = ['date_of_application', 'govtid_type', 'id_number']
    if any(field in data for field in immutable_fields):
        return jsonify({'error': 'Some fields cannot be changed'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    columns = ', '.join([f"{key} = %s" for key in data])
    values = list(data.values()) + [id]

    query = f'UPDATE application SET {columns} WHERE application_id = %s'
    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'success': 'Application updated successfully'})



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
