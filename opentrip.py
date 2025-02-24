import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENTRIPMAP_API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

def get_place_info(place_name):
    url = "https://api.opentripmap.com/0.1/en/places/geoname"
    params = {
        "name": place_name,
        "apikey": OPENTRIPMAP_API_KEY
    }
    response = requests.get(url, params=params)
    data=response.json()
    lat=data.get("lat") #response.json()["lat"]
    lon=data.get("lon")
    main_url="https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        "radius": 10000,
        "kinds": "museums, monuments, parks, churches, art, architecture, history, culture",
        "lon": lon,
        "lat": lat,
        "limit": 5,
        "apikey": OPENTRIPMAP_API_KEY
    }
    #response.raise_for_status()
    #print(response.json())
    place_response = requests.get(main_url, params=params)
    return place_response.json()

# if __name__ == "__main__":
#     get_place_info("London")
