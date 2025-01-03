
# DuckDB Query Interface: Text-to-SQL

This project is a Flask-based web application that allows users to upload an IMDb dataset (CSV file) and generate SQL queries from natural language inputs. It utilizes DuckDB for efficient querying and supports downloading query results in CSV format.

## Features

- **File Upload**: Upload an IMDb dataset in CSV format.
- **Natural Language Query Interface**: Enter natural language queries (e.g., "average rating", "top movies") to generate corresponding SQL queries.
- **Query Execution**: The application executes the generated SQL on the uploaded dataset.
- **Query Output**: Shows the results of the query as a table.

## Requirements

1. Python 3.6+.
2. Install the following Python libraries:
    - Flask
    - DuckDB
    - Google Cloud Natural Language API (Optional for advanced NLP processing)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/duckdb-query-interface.git
    cd duckdb-query-interface
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up Google Cloud NLP API (Optional for advanced NLP):

    - Follow [Google Cloud NLP Setup](https://cloud.google.com/natural-language/docs/setup) and set up your `GOOGLE_APPLICATION_CREDENTIALS` environment variable.

## Running the Application

1. Start the Flask development server:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:8080/`.

## Endpoints

- `/upload_imdb`: POST request for uploading the IMDb CSV file.
  - **Request Body**: A CSV file (must have appropriate format).
  - **Response**: A message confirming the file upload and loading into DuckDB.

- `/generate_sql`: POST request for generating SQL from a natural language query.
  - **Request Body**: A JSON object with a "text" field containing the query (e.g., `{"text": "average rating"}`).
  - **Response**: The generated SQL query and a path to the output CSV file containing the query results.

## Example Usage

### 1. Uploading an IMDb CSV File

- Choose and upload an IMDb CSV file through the file upload form.

### 2. Generating SQL Queries

- After uploading the file, you can enter a natural language query, such as:
  - "Average rating"
  - "Top movies"
  - "Movies with highest rating"
  
  The application will generate and execute the corresponding SQL query on the dataset and show the SQL query in the output section.

### 3. Downloading Query Results

- After executing the query, the results are saved in a CSV file that can be downloaded via the frontend.

## Frontend

The front-end is a simple HTML form that includes:
- A file upload form for uploading the IMDb dataset.
- A text area for entering natural language queries.
- A display area for the generated SQL query.
- A button for downloading the query results as a CSV file.

## NAME - NIKHIL RAJ

