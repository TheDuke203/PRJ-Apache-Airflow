import psycopg2


from DatabaseFunctions.GenericFunctions import config

weather_table = """
CREATE TABLE IF NOT EXISTS weather (
    weather_id SERIAL PRIMARY KEY,
    temperature DECIMAL(5, 2),   -- e.g., 23.45
    weather integer,
    wind_speed integer,
    date_time timestamp,
    station integer,
    UNIQUE(weather_id, temperature, weather, wind_speed, date_time, station)
);
"""

train_weather_table = """
CREATE TABLE IF NOT EXISTS TrainWeather (
trainWeather_id SERIAL PRIMARY KEY,
train_id integer references train(train_id),
weather_id integer references weather(weather_id)
)
"""

train_table = """
CREATE TABLE IF NOT EXISTS train (
    train_id SERIAL PRIMARY KEY,
    train_delay integer,
    train_cancelled boolean,
    departure_station integer,
    destination_station integer,
    departure_time time,
    train_date date
);
"""

event_table = """
CREATE TABLE IF NOT EXISTS event (
    event_id SERIAL PRIMARY KEY,
    event_type text,
    event_date date,
    locations text[]
);
"""

train_event_table = """
CREATE TABLE IF NOT EXISTS TrainEvent (
    trainEvent_id SERIAL PRIMARY KEY,
    train_id integer references train(train_id),
    event_id integer references event(event_id)
);
"""

results_table = """
CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    test_date date,
    test_rows_num integer,
    r_squared_regression decimal,
    true_ratio_classification decimal,
    accuracy_classification decimal,
    UNIQUE(test_date, test_rows, r_squared_regression, true_ratio_classification, accuracy_classification)
);
"""

tables_to_setup = [
    weather_table,
    train_table,
    event_table,
    train_event_table,
    train_weather_table,
    results_table,
]


def setup_database():
    connection = None
    params = config()
    print("Connecting to postgresql database ...")
    try:
        connection = psycopg2.connect(**params)
        connection.autocommit = True
        cur = connection.cursor()

        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ashley_train_prj_db'"
        )
        exists = cur.fetchone()
        if not exists:
            print("Creating new database ashley_train_prj_db")
            cur.execute("CREATE DATABASE ashley_train_prj_db")

        # Connet to the new database
        connection = psycopg2.connect(**params, database="ashley_train_prj_db")
        connection.autocommit = True
        cur = connection.cursor()

        for i in tables_to_setup:
            cur.execute(i)
        print("Completed table setup.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        connection.close() if connection is not None else None
        print("Database connection terminated")
