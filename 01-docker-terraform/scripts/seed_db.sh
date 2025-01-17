#!/bin/bash

# Carrega os dados do taxi verde de outubro 2019
python scripts/ingest.py \
    --user=$POSTGRES_USER \
    --password=$POSTGRES_PASSWORD \
    --host=$POSTGRES_HOST \
    --port=$POSTGRES_PORT \
    --db=$POSTGRES_DB \
    --table_name=green_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

# Carrega os dados das zonas
python scripts/ingest.py \
    --user=$POSTGRES_USER \
    --password=$POSTGRES_PASSWORD \
    --host=$POSTGRES_HOST \
    --port=$POSTGRES_PORT \
    --db=$POSTGRES_DB \
    --table_name=taxi_zones \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv