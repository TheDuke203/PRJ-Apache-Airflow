# my_dag.py
from airflow.decorators import task, dag
from datetime import datetime
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"PRJ-Train-Database")))


from DatabaseFunctions.setup import setup_database
from Trains.TrainGather import train_gather


@dag(description="Setting up the database")
def setup():
    
    @task(task_id="setup_datbase")
    def main_task():
        setup_database()
    main_task()

@dag(description="Adding train info", schedule_interval="30 2 * * *", start_date=datetime(2021,1,1), catchup=False)
def update_train_info():
    
    @task(task_id="gather_train_info")
    def main_task():
        train_gather()
    
    main_task()
    

setup()
update_train_info()