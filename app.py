from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import cloudinary
import cloudinary.uploader
import pandas as pd
import google.generativeai as genai
import duckdb
import requests  # For downloading files
import io
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Cloudinary Configuration (Directly using API keys)
cloudinary.config(
    cloud_name="dudenrb",  # Replace with your Cloudinary Cloud Name
    api_key="225868964835855",  # Replace with your Cloudinary API Key
    api_secret="rwz6RMDbQbihwYoIoqGZ8kh-l98",  # Replace with your Cloudinary API Secret
    secure=True
)

# Google API key for AI
google_api_key = "AIzaSyBi1wQcpPlCAfP9MSHgLSO90WcHBmRnnYI"  # Replace with your Google API Key

# Flask App Setup
app = Flask(__name__)
CORS(app, origins="*")  # Allow cross-origin requests

# Global variable to store the uploaded IMDb file (if any)
imdb_df = None


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Server running successfully"})


@app.route("/upload_imdb", methods=["POST"])
def upload_imdb():
    global imdb_df  # Use the global variable to store the uploaded IMDb file

    if "file" not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400

    try:
        # Log the upload attempt
        logging.info(f"Uploading file: {file.filename}")

        imdb_df = pd.read_csv(file)
        logging.info(f"File uploaded successfully")
        return jsonify({"File uploaded successfully!"}), 200  # Updated message here
    except Exception as e:
        # Log the error
        logging.error(f"Error uploading file: {str(e)}")
        imdb_df = None  # Reset imdb_df on error
        return jsonify({"error": f"Error uploading file: {str(e)}"}), 500


@app.route("/generate_sql", methods=["POST"])
def generate_sql():
    if imdb_df is None:
        return jsonify({"error": "file not uploaded yet."}), 400

    genai.configure(api_key=google_api_key)
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing text input."}), 400

    text_input = data["text"]

    # Prepare prompt with more context for better query generation
    prompt = f"""
    You are an expert SQL generator specializing in DuckDB queries. 

    Given the following natural language request: "{text_input}" 

    and the structure of this CSV file: {imdb_df.head().to_string(index=False)}, 

    generate a valid DuckDB query to retrieve the requested information. 

    Use the table name 'uploaded_csv' and ensure the column names are used correctly. 

    Example: 

    Request: "Show me the name and release year of all shows with a rating above 9.0." 
    Query: SELECT `Name`, `Year` FROM uploaded_csv WHERE `Rating` > 9.0;

    Return only the SQL query without any additional text. 
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        sql_query = response.text.strip()

    except Exception as e:
        return jsonify({"error": f"Error generating SQL: {str(e)}"}), 500

    # Execute the SQL query using DuckDB
    try:
        conn = duckdb.connect()
        conn.register("uploaded_csv", imdb_df)
        output_table = conn.execute(sql_query).fetchdf() 
    except Exception as e:
        return jsonify({"error": f"Error executing SQL: {str(e)} - {sql_query}"}), 500 

    # Convert output to CSV
    csv_data = output_table.to_csv(index=False)
    return Response(
        csv_data, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=output.csv"}
    )


if __name__ == "__main__":
    port = 8080  # Port set directly to 8080, matching the Flask server output
    app.run(host="0.0.0.0", port=port)