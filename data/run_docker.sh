#!/bin/bash

# Ensure a command is provided
if [ -z "$1" ]; then
    echo "Usage: $0 {up|down|up-without-build}"
    exit 1
fi

COMMAND=$1

# Execute the Docker Compose command
case "$COMMAND" in
    up)
        docker compose -f docker-compose.cdc.yaml up -d
        bash source_registration.sh register_connector configs/source-connector.json

        # Initialize Conda for the current shell session
        eval "$(conda shell.bash hook)"
        conda activate mlprod
        python utils/create_table.py
        python utils/insert_to_source.py

        docker compose -f docker-compose.lakehouse.yaml up -d

        # docker build -f dockerfile.spark -t spark-image:latest .
        docker compose -f docker-compose.spark.yaml up -d

        docker compose -f docker-compose.airflow.yaml build
        docker compose -f docker-compose.airflow.yaml up -d --no-build
        docker compose -f docker-compose.feast.yaml up -d
        ;;
    down)
        docker compose -f docker-compose.airflow.yaml down
        docker compose -f docker-compose.cdc.yaml down
        docker compose -f docker-compose.feast.yaml down
        docker compose -f docker-compose.lakehouse.yaml down
        docker compose -f docker-compose.spark.yaml down
        ;;
    up-without-build)
        docker compose -f docker-compose.cdc.yaml up -d
        bash source_registration.sh register_connector configs/source-connector.json

        eval "$(conda shell.bash hook)"
        conda activate mlprod
        python utils/create_table.py
        python utils/insert_to_source.py

        docker compose -f docker-compose.lakehouse.yaml up -d
        docker compose -f docker-compose.spark.yaml up -d
        docker compose -f docker-compose.airflow.yaml up -d --no-build
        docker compose -f docker-compose.feast.yaml up -d
        ;;
    *)
        echo "Invalid command: $COMMAND"
        exit 1
        ;;
esac
