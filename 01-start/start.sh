#!/bin/bash
set -e

NETWORK_NAME="pg_network"
docker network inspect $NETWORK_NAME >/dev/null 2>&1 || \
docker network create $NETWORK_NAME

POSTGRES_CONTAINER="postgres16"
docker rm -f $POSTGRES_CONTAINER >/dev/null 2>&1 || true
docker run -d \
  --name $POSTGRES_CONTAINER \
  --network $NETWORK_NAME \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin1617! \
  -e POSTGRES_DB=superstore\
  -p 5432:5432 \
  postgres:16

ADMINER_CONTAINER="adminer"
docker rm -f $ADMINER_CONTAINER >/dev/null 2>&1 || true
docker run -d \
  --name $ADMINER_CONTAINER \
  --network $NETWORK_NAME \
  -p 8080:8080 \
  adminer

PGADMIN_CONTAINER="pgadmin4"
docker rm -f $PGADMIN_CONTAINER >/dev/null 2>&1 || true
docker run -d \
  --name $PGADMIN_CONTAINER \
  --network $NETWORK_NAME \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com\
  -e PGADMIN_DEFAULT_PASSWORD=admin1617! \
  -p 5050:80 \
  dpage/pgadmin4

echo "Все контейнеры запущены:"
echo "- PostgreSQL 16: localhost:5432"
echo "- Adminer: http://localhost:8080"
echo "- pgAdmin 4: http://localhost:5050"
