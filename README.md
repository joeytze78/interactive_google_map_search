# interactive_google_map_search 

## Property Search Web Application

This is a simple web application that allows users to search for the nearest properties based on a location they type in. The application integrates with the Google Maps API and PostgreSQL database to show the property locations on a map. Users can click on the markers to view the location details.

## Requirements

Before running the application, make sure you have the required dependencies installed.

1. Clone the repository or download the project files.
2. Create an `.env` file to store the PostgreSQL database keys and google map api key. 
3. Navigate to the project folder in your terminal.

## Installation

1. **Create a Virtual Environment** (optional but recommended)
   ```bash
   python -m venv venv

2. **Install the Required Dependencies**
    Run the following command to install all dependencies listed in requirements.txt:
    ```bash
    pip install -r requirements.txt

## Running the Application

1. **Run the Flask Application**
    After installing the dependencies, start the Flask server by running the following command:
    ```bash
    python app.py

2. **Open the Website**
    Once the Flask server starts, you will see a message in the terminal with a URL.  
    Click on the URL in the terminal (or copy and paste it into your browser) to open the web application.

## Using the Application
Search for a Location:

In the search bar, type the name of the location you want to search for (e.g., "Kuala Lumpur").

Click the `Search` button.

## View Property Locations:

The map will center on the searched location, and a blue marker will appear at that location.

Red markers represent properties from the database and will remain visible on the map.

To view more details, click on the markers (both red and blue) on the map. An info window will pop up displaying the property’s name, latitude, and longitude.

## Notes
The application fetches location data from a PostgreSQL database and displays it on the map.

The markers are dynamically added based on the database and the user's search location.
