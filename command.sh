cd terraform
terraform init
terraform plan
terraform apply -auto-approve 
cd ..

docker-compose up airflow-init -d 
docker-compose up -d

## Start connection to debezium
# docker-compose run --rm debezium-init
# docker-compose --profile cdc-init up


## Stream Data
docker-compose run --rm datagen
docker-compose --profile datagen up

## Run Once Interative
docker-compose run --rm datagen --once
docker-compose --profile datagen up --once



# docker-compose build datagen
docker-compose exec -it postgres psql -U postgres -d banking

docker compose restart airflow-webserver airflow-scheduler

## clear mounted volumn
rm -rf docker/postgres/data/*
rm -rf docker/minio/data/*

# import airflow variable
docker exec -it airflow-webserver \
  airflow variables import /opt/airflow/config/airflow_variables.json