#!/bin/bash

docker build -t theduke203/prj-airflow:latest .

docker compose up -d

