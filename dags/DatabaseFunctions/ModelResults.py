from DatabaseFunctions.GenericFunctions import config

import psycopg2
from datetime import datetime

sql = """
INSERT INTO results(
    test_date,
    test_rows_num,
    model,
    r_squared_regression,
    true_ratio_classification,
    accuracy_classification
)
VALUES (%s, %s ,%s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def push_model_results(model ,rows, accuracy, r_squared, true_ratio):
    connection = None
    params = config()
    print("Connecting to postgresql database ...")
    
    connection = psycopg2.connect(**params, database="ashley_train_prj_db")
    connection.autocommit = True
    cur = connection.cursor()
    
    cur.execute(
        sql,
        (
            datetime.today().strftime("%Y-%m-%d"),
            rows,
            model,
            r_squared,
            true_ratio,
            accuracy
        )
    )
    
    cur.close()
    print("Database connection terminated")
