from datetime import datetime
from datetime import timedelta

from Constants.StationInfo import get_station_info
import json


class TrainInfo:
    # Setting up class to contain info for input into train database
    # Data must be numeric to be compatible with machine learning
    # Except Date which is only used for linking purposes.
    def __init__(self, booked_departure, cancelled, delay,
                departure_station, destination_station, date):
        self.booked_departure = booked_departure
        self.delay = delay
        self.cancelled = cancelled
        self.departure_station = departure_station
        self.destination_station = destination_station
        self.date = date

skip_service = []
skip_name = 0

def parse_train_data(json_data, stations_info, tiploc_crs, name_crs):
    """Parse Train Data from API

    Args:
        json_data (JSON): Train Data itself
        stations_info (Dictionary): Stations info from constants
    """
    trains_info = []
    global skip_service, skip_name
    for service in json_data['services']:
        if service['serviceType'] != "train":
            skip_service.append(service['serviceType'])
            continue

        location_detail = service['locationDetail']

        # Example: 2025-01-22
        date = datetime.strptime(service['runDate'], "%Y-%m-%d")
        
        booked_dpt = location_detail.get('gbttBookedDeparture')
        realtime_dept = location_detail.get('realtimeDeparture')
        
        if not booked_dpt or not realtime_dept:
            continue
        
        booked_departure = datetime.strptime(location_detail.get('gbttBookedDeparture'), "%H%M")
        actual_departure = datetime.strptime(location_detail.get('realtimeDeparture'), "%H%M")
        
        actual_next_day = location_detail.get('realtimeDepartureNextDay')
        booked_next_day = location_detail.get('gbttBookedDepartureNextDay')

        if actual_next_day and booked_next_day == None:
            actual_departure += timedelta(days=1)

        delay = (actual_departure - booked_departure).total_seconds() / 60

        cancelled = True if location_detail['displayAs'] == "CANCELLED_CALL" or \
                            location_detail['displayAs'] == "CANCELLED_PASS" else False
        departure_station = stations_info[location_detail['crs']][1]

        crs_from_tiploc = tiploc_crs.get(location_detail['destination'][0]['tiploc'])
        crs_from_name = name_crs.get(location_detail['destination'][0]['description'].lower())

        name_test = stations_info.get(crs_from_name)
        tiploc_test = stations_info.get(crs_from_tiploc)

        if name_test == None and tiploc_test == None:
            skip_name += 1
            continue

        destination_station = tiploc_test[1] if tiploc_test != None else name_test[1]

        trains_info.append(TrainInfo(booked_departure=booked_departure,
                                    cancelled=cancelled, delay=delay, departure_station=departure_station,
                                    destination_station=destination_station, date=date))
    print(f"Skipped for service type being different: {str(len(skip_service))}")
    print(f"SKipped for the name for crs or tiploc not being found: {str(skip_name)}" )
    return trains_info


# Testing function with example train data.
def test_example_data():
    with open('exampletraindata.json') as f:
        d = json.load(f)
        stations = parse_train_data(d, get_station_info())
        print("Done")

# Useful for testing
# test_example_data()
