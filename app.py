from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()
app = Flask(__name__)

print(f"Google Maps API Key loaded: {os.getenv('GOOGLE_MAPS_API_KEY') is not None}")


# Database connection function (same as before)
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

# Route to serve the HTML page
@app.route('/')
def index():
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Google Maps API key not found in environment variables")
    return render_template('index.html', google_maps_api_key=api_key)

# API endpoint for places data
@app.route('/api/places')
def get_places():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    cursor = conn.cursor()
    cursor.execute("SELECT prjname, latitude, longitude FROM projectmaster WHERE prjlocation IS NOT NULL")
    rows = cursor.fetchall()
    
    places = []
    for row in rows:
        prjname, latitude, longitude = row
        places.append({
            "prjname": prjname,
            "latitude": float(latitude),  # Ensure these are numbers, not strings
            "longitude": float(longitude)  
        })
    
    cursor.close()
    conn.close()
    return jsonify(places)

if __name__ == '__main__':
    app.run(debug=True)