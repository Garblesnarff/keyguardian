FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application code and deployment assets needed at runtime
COPY apikeywallet-main /app
COPY deploy/app/requirements.txt /app/requirements.txt
COPY deploy/app/gunicorn.conf.py /app/deploy/app/gunicorn.conf.py
COPY scripts /app/scripts
COPY deploy/app/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

ENV FLASK_APP=app.py
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["/entrypoint.sh"]


