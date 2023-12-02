# Electricity Connection Application API

### This project is a Flask-based API for managing electricity connection applications. It provides functionalities to view, search, filter, and edit application requests.


## Prerequisites

### Python 3.8 or later
### PostgreSQL

## Installation

### pip install -r requirements.txt

### Setup a .env file with database credentials like DB_HOST , DB_PASS , DB_USER and DB_NAME

## API Endpoints

### Get Applications

    Endpoint: /applications
    Method: GET
    Description: Retrieves a paginated list of all electricity connection applications. Supports pagination through query parameters.
    Query Parameters:
        page (optional): The page number in the pagination sequence.
        per_page (optional): The number of records per page.
    Example Request: GET /applications?page=2&per_page=10

### Filter Applications by Date Range

    Endpoint: /applications/filter
    Method: GET
    Description: Filters applications within a specified date range. Both startDate and endDate query parameters are required.
    Query Parameters:
        startDate: The start date for the date range filter.
        endDate: The end date for the date range filter.
    Example Request: GET /applications/filter?startDate=2021-01-01&endDate=2021-02-02

### Edit Application

    Endpoint: /applications/edit/<int:id>
    Method: PUT
    Description: This endpoint allows editing details of a specific application. It enforces data validation, such as ensuring the load applied does not exceed 200 KV.
    URL Parameters:
        id: The unique identifier of the application to be edited.
    Request Body: JSON object containing the fields to be updated.
    Example Request: PUT /applications/edit/1 with a JSON body.

### Search Applications by Applicant ID

    Endpoint: /applications/search
    Method: GET
    Description: Searches for applications by the applicant ID. Returns a list of applications that match the provided ID.
    Query Parameters:
        applicantId: The unique ID of the applicant.
    Example Request: GET /applications/search?applicantId=7

### Get Application Statistics

    Endpoint: /applications/stats
    Method: GET
    Description: This endpoint provides statistical data about the applications. It can return counts of applications grouped by status (e.g., 'Pending', 'Approved'). The status can be specified as a query parameter; if no status is provided, statistics for all statuses will be returned.
    Query Parameters:
        status (optional): The status of the applications to filter by (e.g., 'Pending', 'Approved'). Default is 'All'.
    Example Request: GET /applications/stats?status=Pending


