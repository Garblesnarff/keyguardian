#!/usr/bin/env bash
set -euo pipefail

# Automates local or server setup using Docker Compose

cd "$(dirname "$0")/deploy"

if [ ! -f .env ]; then
  echo "Creating .env from example..."
  if [ -f .env.example ]; then
    cp .env.example .env
  else
    cp env.example .env
  fi
  # Generate secrets if not set
  SECRET=$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
)
  sed -i "" -e "s/replace_with_secure_random/$SECRET/g" .env || sed -i -e "s/replace_with_secure_random/$SECRET/g" .env
fi

echo "Building and starting services..."
docker compose up -d --build

echo "Stack is up. To request certificates run:"
echo "  docker compose run --rm --service-ports certbot certbot certonly --webroot -w /var/www/certbot -d \"\${DOMAIN}\" --agree-tos --email \"\${LETSENCRYPT_EMAIL}\" --no-eff-email --non-interactive"
echo "Then: docker compose restart nginx"


