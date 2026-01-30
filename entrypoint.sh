#!/bin/bash

echo "Creating media directories..."
mkdir -p /app/media/documents
chmod -R 777 /app/media

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
