# PRJ-Apache-Airflow
Instructions for setup and cleaning and re-setup encase anything failing can be found:
# PRE-REQUISITES
[Docker](https://www.docker.com/)
[Docker compose](https://docs.docker.com/compose/)
Enviroment Variables see below

# Running the docker container
- The docker image is pre-built and hosted on dockerhub
- Simply run
  - docker compose up -d
- To setup and run the docker compose file


# Enviroment variables
This server relies upon various enviorment variables to be set in order to make queries to api's etc.
Create a .env file at the root containing 
```
AIRFLOW_UID: User id that container should run a
```

Inside dags/DatabaseFunctions
create database.ini using this format
```
[postgresql]
host=host_address
user=postgres_username
password=postgres_password
```

In dags/Trains create a .env using [RTT API ](https://api.rtt.io/)
```
USER_TRAIN=RTT api username
PASS_TRAIN=RTT api password
```

In dags/Weathe create a .env for the [openWeatherApi](https://openweathermap.org/api)
```
API_KEY=API key for openweather api
```
