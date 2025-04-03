let map;
let markers = [];  
let infoWindow;
let searchMarker = null;  
let places = [];  

async function initMap() {
    // Create initial map centered on the default location (Kuala Lumpur)
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 3.1390, lng: 101.6869 },
        zoom: 12,
    });

    infoWindow = new google.maps.InfoWindow();

    // Load places from backend and add initial markers
    try {
        const response = await fetch('/api/places');
        const fetchedPlaces = await response.json();

        places = fetchedPlaces.map(place => ({
            type: "from_db",
            prjname: place.prjname,
            latitude: place.latitude,
            longitude: place.longitude
        }));

        addMarker(places, 'from_db');  

    } catch (error) {
        console.error('Error loading places:', error);
    }

    document.getElementById('search-button').addEventListener('click', async () => {
        if (document.getElementById('search-input').value) {
            const lastPlace = places[places.length - 1];

            // Remove the search_input from showing
            if (lastPlace.type === "search_input") {
                places.pop();
            }

            const searchPlace = await searchLocation(document.getElementById('search-input').value);

            // Add the new search marker
            places.push(searchPlace); 
            addMarker(places, 'search_input');  

            map.setCenter({
                lat: searchPlace.latitude,
                lng: searchPlace.longitude
            });
        }
    });
}

function addMarker(places, type) {
    // Remove all markers from the map before adding new ones
    markers.forEach(marker => marker.setMap(null));

    places.forEach(place => {
        const markerColor = place.type === "search_input" ? 'blue' : 'red'; // Blue for search, Red for db

        const marker = new google.maps.Marker({
            position: { lat: parseFloat(place.latitude), lng: parseFloat(place.longitude) },
            map: map,
            title: place.prjname,
            icon: {
                url: `http://maps.google.com/mapfiles/ms/icons/${markerColor}-dot.png`
            }
        });

        // Add click event to show info window
        marker.addListener('click', () => {
            infoWindow.setContent(`
                <div class="info-window">
                    <h3>${place.prjname}</h3>
                    <p><strong>Latitude:</strong> ${place.latitude}</p>
                    <p><strong>Longitude:</strong> ${place.longitude}</p>
                </div>
            `);
            infoWindow.open(map, marker);
        });

        markers.push(marker);  // Add marker to the markers array
    });
}

async function searchLocation(input) {
    return new Promise((resolve, reject) => {
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ address: input }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const searchPlace = {
                    type: "search_input",  // Mark this place as coming from search input
                    prjname: input,
                    latitude: results[0].geometry.location.lat(),
                    longitude: results[0].geometry.location.lng()
                };
                resolve(searchPlace);
            } else {
                alert('Location not found: ' + status);
                reject(status);
            }
        });
    });
}
