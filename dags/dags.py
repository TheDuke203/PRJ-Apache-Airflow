# my_dag.py
from airflow.decorators import task, dag
from datetime import datetime


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