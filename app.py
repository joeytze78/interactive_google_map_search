from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
import os
import googlemaps
import psycopg2

load_dotenv()
app = Flask(__name__)

print(f"Google Maps API Key loaded: {os.getenv('GOOGLE_MAPS_API_KEY') is not None}")
master_table = os.getenv("MASTER_TABLE")
google_map_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
gmaps = googlemaps.Client(key=google_map_api_key)

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
    cursor.execute(f"SELECT prjname, prjlocation, latitude, longitude FROM {master_table} WHERE prjlocation IS NOT NULL AND prjlocation != ''")
    rows = cursor.fetchall()
    
    places = []
    for row in rows:
        prjname, prjlocation, latitude, longitude = row
        
        # If latitude or longitude is missing, fetch it using Google Maps Geocoding API
        # print(f"Processing {prjname} with location {prjlocation}")
        if latitude is None or longitude is None:
            # Use the geocode API to get lat, long
            geocode_result = gmaps.geocode(prjlocation)
            if geocode_result:
                latitude = geocode_result[0]['geometry']['location']['lat']
                longitude = geocode_result[0]['geometry']['location']['lng']
                # print(f"Updated lat/long for {prjname}: {latitude}, {longitude}")
            else:
                latitude = None
                longitude = None

        places.append({
            "prjname": prjname,
            "prjlocation": prjlocation,
            "latitude": float(latitude) if latitude is not None else None,  # Ensure these are numbers, not strings
            "longitude": float(longitude) if longitude is not None else None
        })
    
    cursor.close()
    conn.close()
    print("Done processing places")
    return jsonify(places)

if __name__ == '__main__':
    app.run(debug=True)