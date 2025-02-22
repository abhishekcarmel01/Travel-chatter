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
    #response.raise_for_status()
    print(response.json())
    #return response.json()

if __name__ == "__main__":
    get_place_info("London")
