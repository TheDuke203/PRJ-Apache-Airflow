# my_dag.py
from airflow.decorators import task, dag
from datetime import datetime


from DatabaseFunctions.setup import setup_database
from DatabaseFunctions.WeatherTrainRun import update_train_weather
from Trains.TrainGather import train_gather
from Weather.WeatherGather import gather_weather_info

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
    
@dag(description="Adding weather info", schedule_interval="10 2 */5 * *", start_date=datetime(2021,1,1), catchup=False)
def update_weather_info():
    
    @task(task_id="gather_weather_info")
    def main_task():
        gather_weather_info()
    
    main_task()

@dag(description="", schedule_interval="10 2 */5 * *", start_date=datetime(2021,1,1), catchup=False)
def update_weather_info():
    
    @task(task_id="gather_weather_info")
    def main_task():
        gather_weather_info()
        
    @task
    def train_weather_update():
        update_train_weather()
    
    main_task()
    train_weather_update()


setup()
update_train_info()
update_weather_info()