import os
import sys

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from Constants.StationInfo import interest_stations, get_station_info
from dotenv import load_dotenv
from datetime import datetime

stations_info = get_station_info()

weather_dir = os.path.dirname(__file__)
load_dotenv(os.path.join(weather_dir, ".env"))
api_key = os.getenv("API_KEY")


def gather_weather_info():
    """
    Gather the weather information from yesterday for all interest stations
    """
    weather_data_5_days = []
    for station in interest_stations:
        (lat, lon) = stations_info[station][2] 
        location = stations_info[station][1]
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        
        list_items = requests.get(url).json().get('list')
        for item in list_items:
            temperature = item.get('main').get('temp')
            weather = item.get('weather')[0].get('id')
            date = datetime.strptime(item.get('dt_text'), "%Y-%m-%d %H:%M:%S")

        
gather_weather_info()