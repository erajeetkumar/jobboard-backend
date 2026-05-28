#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Starting Django Backend Entrypoint ==="

# Wait for PostgreSQL database to be ready
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database at ${DB_HOST}:${DB_PORT:-5432} to become ready..."
    until pg_isready -h "$DB_HOST" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}" > /dev/null 2>&1; do
        echo "PostgreSQL is unavailable - sleeping..."
        sleep 1
    done
    echo "PostgreSQL is up and running!"
fi

# Run Django migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Run any other commands passed to docker container
echo "Running application: $@"
exec "$@"
