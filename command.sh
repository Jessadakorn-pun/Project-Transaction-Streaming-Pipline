docker-compose up airflow-init -d 
docker-compose up -d

## Start connection to debezium
docker compose run --rm debezium-init
docker-compose --profile cdc-init up


## Stream Data
docker-compose run --rm datagen
docker-compose --profile datagen up

## Run Once Interative
docker-compose run --rm datagen --once
docker-compose --profile datagen up --once



# docker-compose build datagen
docker-compose exec -it postgres psql -U postgres -d banking