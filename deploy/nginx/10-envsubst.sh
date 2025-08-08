#!/usr/bin/env sh
set -e

echo "Rendering nginx.conf from template using DOMAIN=$DOMAIN"
envsubst '${DOMAIN}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf


