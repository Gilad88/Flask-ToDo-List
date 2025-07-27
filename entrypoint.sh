#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."
# Loop until PostgreSQL is ready
# This part is crucial for ensuring the DB is fully up before the app tries to connect
while ! pg_isready -h db -p 5432 -U postgres; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running init_db.py to create/check database tables..."
python init_db.py

echo "Starting Gunicorn server..."
# Execute the original command (CMD from Dockerfile)
exec gunicorn --bind 0.0.0.0:5000 app:app
