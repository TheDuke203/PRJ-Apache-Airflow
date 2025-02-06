from datetime import datetime
from typing import List
import psycopg2
from airflow.decorators import task
from DatabaseFunctions.GenericFunctions import config

import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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
VALUES (%s, %s, %s, %s, %s, %s);
"""

def push_data(stations_data):
    connection = None
    params = config()
    print("Connecting to postgresql database ...")
    try:
        connection = psycopg2.connect(**params, database="ashley_train_prj_db")
        connection.autocommit = True
        cur = connection.cursor()

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

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        connection.close() if connection is not None else None
        print("Database connection terminated")
