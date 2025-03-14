import os
import sys
# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
from Constants.StationInfo import interest_stations, get_station_info
from dotenv import load_dotenv
from datetime import datetime

from DatabaseFunctions.WeatherDataInput import push_weather_data

stations_info = get_station_info()

weather_dir = os.path.dirname(__file__)
load_dotenv(os.path.join(weather_dir, ".env"))
api_key = os.getenv("API_KEY")

class WeatherInfo:
    def __init__(self, temperature, weather, wind_speed, date, station):
        self.temperature = temperature
        self.weather = weather
        self.wind_speed = wind_speed
        self.date = date
        self.station = station
        


def gather_weather_info():
    """
    Gather the weather information from yesterday for all interest stations
    """
    
    weather_data_info = []
    
    for station in interest_stations:
        (lat, lon) = stations_info[station][2] 
        stationNum = stations_info[station][1]
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
        
        list_items = requests.get(url).json().get('list')
        for item in list_items:
            temperature = item.get('main').get('temp')
            weather = item.get('weather')[0].get('id')
            wind_speed = item.get('wind').get('speed')
            date = datetime.strptime(item.get('dt_txt'), "%Y-%m-%d %H:%M:%S")
            weather_data_info.append(WeatherInfo(temperature, weather, wind_speed, date, stationNum))
    
    print("Unique rows added to weather: " + str(push_weather_data(weather_data_info)))


    
