#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h db -p 5432 -U postgres; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running init_db.py to create/check database tables..."
python init_db.py

echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:5000 app:app
