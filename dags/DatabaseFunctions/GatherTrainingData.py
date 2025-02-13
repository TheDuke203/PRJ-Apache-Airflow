import psycopg2
# from DatabaseFunctions.GenericFunctions import config
from DatabaseFunctions.GenericFunctions import config



sql_command = """
SELECT *
FROM train t
INNER JOIN trainweather tw ON t.train_id = tw.train_id
INNER JOIN weather w ON w.weather_id = tw.weather_id
"""


def get_combined_data():
    connection = None
    params = config()
    print("Connecting to postgresql database ...")
    try:
        connection = psycopg2.connect(**params, database="ashley_train_prj_db")
        connection.autocommit = True
        cur = connection.cursor()
        
        cur.execute(sql_command)
        output = cur.fetchall()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        connection.close() if connection is not None else None
        print("Database connection terminated")
    
    return output

