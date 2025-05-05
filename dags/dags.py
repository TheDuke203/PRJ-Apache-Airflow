# my_dag.py
from airflow.decorators import task, dag
from datetime import datetime


from DatabaseFunctions.setup import setup_database
from DatabaseFunctions.GenericFunctions import config
from DatabaseFunctions.TrainWeatherCombine import combine_train_weather
from Trains.TrainGather import train_gather
from Weather.WeatherGather import gather_weather_info
from Training.TrainModels import run_general_models

@dag(description="Setting up the database", catchup=False)
def setup():
    
    @task(task_id="setup_datbase")
    def main_task():
        setup_database()
    main_task()

@dag(description="Adding train info", schedule_interval="30 2 * * *", start_date=datetime(2025,2,6), catchup=False)
def update_train_info():
    
    @task(task_id="gather_train_info")
    def main_task():
        train_gather()
    
    main_task()

@dag(description="Update weather info", schedule_interval="05 18 */4 * *", start_date=datetime(2025,2,13), catchup=False)
def update_weather_info():
    
    @task(task_id="gather_weather_info")
    def main_task():
        gather_weather_info()
    
    main_task()

@dag(description="combine trains to weather data", schedule_interval="50 2 * * *", start_date=datetime(2025,2,8), catchup=False)
def train_weather_combine():
    
    @task
    def main_task():
        row_count = combine_train_weather()
        print("Rows added: " + str(row_count))
    main_task()

@dag(description="update the results of testing the model", schedule="50 3 * * *", start_date=datetime(2025,2,8), catchup=False)
def model_results_update():
    
    @task
    def main_task():
        run_general_models()
    main_task()

@dag(description="Backup database", schedule="30 4 * * *", start_date=datetime(2025,2,16), catchup=False)
def run_backup_script():
    params = config()
    @task.bash(cwd="/opt/airflow/backup", env={"PGPASSWORD": params.get("password"), "SERVHOST": params.get("host"), \
        "SERVUSER": params.get("user")} )
    def main_task():
        return "DatabaseFunctions/backup.sh"
    main_task()

setup()
update_train_info()
update_weather_info()
train_weather_combine()
model_results_update()
run_backup_script()