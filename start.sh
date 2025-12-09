#!/usr/bin/env bash
set -e
# Detect Django project package by looking for wsgi.py
PROJ=""
if [ -f "./dondever/wsgi.py" ]; then
  PROJ=dondever
elif [ -f "./dondeverapp/wsgi.py" ]; then
  PROJ=dondeverapp
else
  # fallback: try to find first folder in root that contains wsgi.py
  candidate=$(find . -maxdepth 2 -type f -name wsgi.py | head -n1 | sed 's|^\./||' | sed 's|/wsgi.py$||')
  if [ -n "$candidate" ]; then
    PROJ=$candidate
  fi
fi
if [ -z "$PROJ" ]; then
  echo "Could not detect Django project package (no wsgi.py found)." >&2
  exit 1
fi

echo "Starting gunicorn for project: $PROJ"
# Default to $PORT or 8000
PORT=${PORT:-8000}
exec gunicorn "$PROJ.wsgi:application" --bind 0.0.0.0:"$PORT"
