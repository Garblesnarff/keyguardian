#!/usr/bin/env sh
set -e

echo "Starting KeyGuardian app entrypoint..."

if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database to be reachable..."
  python - <<'PY'
import os, time
import sqlalchemy as sa
url = os.environ['DATABASE_URL']
for i in range(60):
    try:
        sa.create_engine(url).connect().close()
        print("Database is reachable")
        break
    except Exception as e:
        time.sleep(2)
else:
    raise SystemExit("ERROR: Database not reachable after waiting")
PY
fi

if [ -d "migrations" ]; then
  echo "Applying database migrations..."
  flask db upgrade || true
fi

echo "Launching Gunicorn..."
exec gunicorn --config deploy/app/gunicorn.conf.py app:app


