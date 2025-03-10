from datetime import datetime
from typing import List
import psycopg2
from DatabaseFunctions.GenericFunctions import config


from Trains.TrainParser import TrainInfo

sql = """
INSERT INTO train(
    train_delay, 
    train_cancelled, 
    departure_station,
    destination_station, 
    departure_time, 
    train_date
)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def push_data(stations_data):
    connection = None
    params = config()
    print("Connecting to postgresql database ...")

    connection = psycopg2.connect(**params, database="ashley_train_prj_db")
    connection.autocommit = True
    cur = connection.cursor()
    rowCount = 0
    trains_data: List[TrainInfo]
    for trains_data in stations_data:
        for trains in trains_data:
            cur.execute(
                sql,
                (
                    trains.delay,
                    trains.cancelled,
                    trains.departure_station,
                    trains.destination_station,
                    datetime.strftime(trains.booked_departure, "%H:%M"),
                    datetime.strftime(trains.date, "%Y-%m-%d"),
                ),
            )
            rowCount += cur.rowcount
    
    cur.close()
    print("Database connection terminated")
    return rowCount