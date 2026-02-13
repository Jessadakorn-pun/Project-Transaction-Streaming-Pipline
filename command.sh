docker-compose up airflow-init -d 
docker-compose up -d


docker compose build datagen

## Stream Data
docker compose run --rm datagen

## Run Once Interative
docker compose run --rm datagen --once


docker-compose exec -it postgres psql -U postgres -d banking