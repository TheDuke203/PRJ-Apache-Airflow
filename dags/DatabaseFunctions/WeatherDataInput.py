from datetime import datetime
import psycopg2
from DatabaseFunctions.GenericFunctions import config


sql = """
INSERT INTO weather(
    temperature,
    weather,
    wind_speed,
    date_time,
    station
)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def push_weather_data(weather_datas):
    connection = None
    params = config()
    print("Connecting to postgresql database ...")
    
    connection = psycopg2.connect(**params, database="ashley_train_prj_db")
    connection.autocommit = True
    cur = connection.cursor()
    
    for weather in weather_datas:
        cur.execute(
            sql,
            (
                weather.temperature,
                weather.weather,
                weather.wind_speed,
                datetime.strftime(weather.date, "%Y-%m-%d %H:%M:%S"),
                weather.station,
            ),
        )

    row_count = cur.rowcount
    
    cur.close()
    print("Database connection terminated")
    return row_count
    