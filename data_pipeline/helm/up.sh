#!/bin/sh

set -euo pipefail

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${BASE_DIR}/.."
(
cd ${REPO_DIR}
kubectl create namespace trino
kubectl create secret generic redis-table-definition --from-file=trino-on-kubernetes/redis/test.json -n trino || true

# Adding Helm repos and ignoring errors if the repo already exists
helm repo add bitnami https://charts.bitnami.com/bitnami || true
helm repo add trino https://trinodb.github.io/charts/ || true

kubectl minio init -n trino
kubectl minio tenant create tenant-1 --servers 2 --volumes 4 --capacity 4Gi -n trino
helm upgrade --install hive-metastore-postgresql bitnami/postgresql -n trino -f trino-on-kubernetes/hive-metastore-postgresql/values.yaml
helm upgrade --install my-hive-metastore -n trino -f trino-on-kubernetes/hive-metastore/values.yaml trino-on-kubernetes/charts/hive-metastore
helm upgrade --install my-redis bitnami/redis -n trino -f trino-on-kubernetes/redis/values.yaml
helm upgrade --install my-trino trino/trino --version 0.7.0 --namespace trino -f trino-on-kubernetes/trino/values.yaml

kubectl create -n trino -f debezium/secret.yaml
kubectl create -n trino -f debezium/role.yaml
kubectl create -n trino -f debezium/rolebinding.yaml
kubectl create -n trino -f kafka/kafka_cluster.yaml
kubectl create -n trino -f mysql/values.yaml

docker build -t debezium-postgres-connect -f debezium.dockerfile . 
docker login
docker tag debezium-postgres-connect duongnguyen2911/debezium-postgres-connect:latest
docker push duongnguyen2911/debezium-postgres-connect:latest

kubectl create -n trino -f kafka/connect.yaml
kubectl create -n trino -f kafka/connector.yaml
)
