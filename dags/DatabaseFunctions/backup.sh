#!/bin/bash
date=$(date '+%Y-%m-%d')

pg_dump ashley_train_prj_db > "prj-database-${date}"

if [ "$?"-ne 0]; then echo "Help" | mail -s "Backup failed" you@example.com; exit 1; fi