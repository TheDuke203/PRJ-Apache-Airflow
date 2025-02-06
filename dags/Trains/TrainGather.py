import os
from datetime import datetime, timedelta

from Trains.StationInfo import get_station_info, tiploc_crs, name_crs
from dotenv import load_dotenv
import requests
from Trains.TrainParser import parse_train_data
from airflow.decorators import task
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DatabaseFunctions.TrainDataInput import push_data

# List of station names to gather info for used only for searching.
interest_stations = [
    "AAP",
    "AWM",
    "BFR",
    "BTN",
    "CBG",
    "CMB",
    "CTK",
    "ELY",
    "FPK",
    "FXN",
    "GTW",
    "HIT",
    "HRH",
    "HUN",
    "KGX",
    "KLN",
    "LET",
    "LTP",
    "PBO",
    "PBR",
    "RDH",
    "RYS",
    "STH",
    "STP",
    "SVG",
    "WBC",
    "WGC",
    "ZFD",
]

Trains_dir = os.path.dirname(os.path.abspath(__file__))


load_dotenv(os.path.join(Trains_dir,"data", ".trainEnv"))

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
