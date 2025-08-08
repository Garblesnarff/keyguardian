#!/usr/bin/env bash
set -euo pipefail

# This script bootstraps an Ubuntu EC2 instance for production deployment
# - Installs Docker, Docker Compose
# - Configures firewall
# - Pulls repo and launches stack

REPO_URL=${REPO_URL:?Set REPO_URL to your git repository}
DOMAIN=${DOMAIN:?Set DOMAIN to your domain}
LETSENCRYPT_EMAIL=${LETSENCRYPT_EMAIL:?Set LETSENCRYPT_EMAIL}
POSTGRES_DB=${POSTGRES_DB:-keyguardian}
POSTGRES_USER=${POSTGRES_USER:-keyguardian}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}
S3_BUCKET=${S3_BUCKET:?Set S3_BUCKET}
GRAFANA_USER=${GRAFANA_USER:-admin}
GRAFANA_PASSWORD=${GRAFANA_PASSWORD:-admin}

export DEBIAN_FRONTEND=noninteractive

sudo apt-get update
sudo apt-get install -y ca-certificates curl git gnupg awscli

# Docker
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER || true

# Clone repo
APP_ROOT=/opt/keyguardian
sudo mkdir -p "$APP_ROOT"
sudo chown "$USER":"$USER" "$APP_ROOT"
if [ ! -d "$APP_ROOT/.git" ]; then
  git clone "$REPO_URL" "$APP_ROOT"
else
  cd "$APP_ROOT" && git pull --rebase
fi

cd "$APP_ROOT/deploy"

# Create .env from example
if [ ! -f .env ]; then
  cp .env.example .env
  sed -i "" -e "s/example.com/$DOMAIN/g" .env || sed -i -e "s/example.com/$DOMAIN/g" .env
  sed -i "" -e "s/admin@example.com/$LETSENCRYPT_EMAIL/g" .env || sed -i -e "s/admin@example.com/$LETSENCRYPT_EMAIL/g" .env
  sed -i "" -e "s/replace_with_strong_password/$POSTGRES_PASSWORD/g" .env || sed -i -e "s/replace_with_strong_password/$POSTGRES_PASSWORD/g" .env
  sed -i "" -e "s/s3-bucket-name/$S3_BUCKET/g" .env || sed -i -e "s/s3-bucket-name/$S3_BUCKET/g" .env
fi

echo "Launching stack..."
docker compose up -d --build

echo "Requesting initial certificates..."
docker compose run --rm --service-ports certbot certbot certonly --webroot -w /var/www/certbot -d "$DOMAIN" --agree-tos --email "$LETSENCRYPT_EMAIL" --no-eff-email --non-interactive || true

echo "Reloading nginx..."
docker compose restart nginx

echo "Done. Access: https://$DOMAIN"


