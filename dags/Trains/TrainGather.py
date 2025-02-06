from datetime import datetime, timedelta

from Constants.StationInfo import get_station_info, tiploc_crs, name_crs, interest_stations
from dotenv import load_dotenv
import requests
from Trains.TrainParser import parse_train_data
import os

from DatabaseFunctions.TrainDataInput import push_data

dag_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))


load_dotenv(os.path.join(dag_dir, "Constants", "data", ".trainEnv"))

USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASS")

base_url = "https://api.rtt.io/api/v1/json/search/"

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), "%Y/%m/%d")

def train_gather():
    # Has info on all train stations in UK
    stations_info = get_station_info()
    tiploc_to_crs = tiploc_crs()
    name_to_crs = name_crs()

    full_urls = []
    stations_data = []

    # Make all the URLS forstations that we are interested in
    for station in interest_stations:
        full_urls.append(base_url + station + "/" + yesterday_date)

    # Get the data for each station that we are interested in.
    for full_url in full_urls:
        contents = requests.get(full_url, auth=(USERNAME, PASSWORD)).json()
        stations_data.append(parse_train_data(contents, stations_info, tiploc_to_crs, name_to_crs))


    push_data(stations_data)
