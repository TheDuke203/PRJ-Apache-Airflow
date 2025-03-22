#!/bin/bash
date=$(date '+%Y-%m-%d')

pg_dump --dbname=ashley_train_prj_db --host=$SERVHOST --username=$SERVUSER --password > "prj-database-${date}"

if [ "$?"-ne 0]; then exit 1; fi