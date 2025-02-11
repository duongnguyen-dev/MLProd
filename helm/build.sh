group_name="docker"

# Check if the group exists
if getent group "$group_name" > /dev/null 2>&1; then
    echo "Group '$group_name' already exists."
    sudo usermod -aG docker ${USER}
    newgrp docker

    docker build -t debezium-postgres-connect -f debezium.dockerfile . 
    docker login
    docker tag debezium-postgres-connect duongnguyen2911/debezium-postgres-connect:latest
    docker push duongnguyen2911/debezium-postgres-connect:latest
else
    echo "Group '$group_name' does not exist. Adding the group..."
    sudo groupadd "$group_name"
    echo "Group '$group_name' has been added."
    sudo usermod -aG docker ${USER}
    newgrp docker

    docker build -t debezium-postgres-connect -f debezium.dockerfile . 
    docker login
    docker tag debezium-postgres-connect duongnguyen2911/debezium-postgres-connect:latest
    docker push duongnguyen2911/debezium-postgres-connect:latest
fi
