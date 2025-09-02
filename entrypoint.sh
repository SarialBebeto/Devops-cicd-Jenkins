#!/bin/sh
set -e

echo "Waiting for Postgres.."
# wait until pg_isready confirms DB is accepting connections
until pg_isready -h db -p 5432 -U "${POSTGRES_USER:fastapi_traefik_prod}"; do
   echo "Postgres is unavailable - sleeping"
   sleep 1
done

echo "Postgres is up - starting server"
exec uvicorn app.main:app --host 0.0.0.0 --port 80