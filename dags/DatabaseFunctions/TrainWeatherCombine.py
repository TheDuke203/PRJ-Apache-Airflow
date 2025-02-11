import psycopg2
from DatabaseFunctions.GenericFunctions import config

"""
SQL Query to populate the trainweather combined table:

select the train_id and weather_id from the sub query table.

We create a new table adding in a row number partitioning over train_id with the order of the time between weather and train.
We maintain the constraints of the train not already being inside of the trainweather and the weather being beore the train
Finally we ensure that hte weather_id is not null to ensure that we make complete matches.

Then we simply return the rn of 1 which is the lowest time i.e closest weather row to the train.
"""

sql_command = """
INSERT INTO TrainWeather (train_id, weather_id)
SELECT train_id, weather_id
FROM (
    SELECT t.train_id, 
           w.weather_id,
           ROW_NUMBER() OVER (PARTITION BY t.train_id ORDER BY (t.train_date + t.departure_time) - w.date_time) as rn
    FROM Train t
    JOIN Weather w ON w.station = t.departure_station 
        AND w.date_time <= (t.train_date + t.departure_time)
    WHERE NOT EXISTS (
        SELECT 1 
        FROM TrainWeather tw 
        WHERE tw.train_id = t.train_id
    )
    AND w.weather_id IS NOT NULL
) ranked
WHERE rn = 1;
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