import psycopg2
from DatabaseFunctions.GenericFunctions import config


sql_command = """
INSERT INTO TrainWeather (train_id, weather_id)
SELECT 
    t.train_id as train_id,
    (
        SELECT w.weather_id
        FROM Weather w
        WHERE w.station = t.departure_station
        AND w.date_time <= (t.train_date + t.departure_time)
        ORDER BY (t.train_date + t.departure_time) - w.date_time
        LIMIT 1
    ) as weather_id
FROM Train t
WHERE NOT EXISTS (
    SELECT 1 
    FROM TrainWeather tw 
    WHERE tw.train_id = t.train_id
)
"""

def combine_train_weather():
    connection = None
    params = config()
    print("Connecting to postgresql database ...")

    connection = psycopg2.connect(**params, database="ashley_train_prj_db")
    connection.autocommit = True
    cur = connection.cursor()
    
    cur.execute(sql_command)
    row_count = cur.rowcount
    cur.close()
    
    
    print("Database connection terminated")
    return row_count