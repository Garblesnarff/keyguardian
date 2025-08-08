#!/usr/bin/env bash
set -euo pipefail

# Requires: awscli, pg_dump

DATE=$(date +"%Y%m%d-%H%M%S")
S3_BUCKET=${S3_BUCKET:?S3_BUCKET is required}
POSTGRES_HOST=${POSTGRES_HOST:-localhost}
POSTGRES_DB=${POSTGRES_DB:?POSTGRES_DB is required}
POSTGRES_USER=${POSTGRES_USER:?POSTGRES_USER is required}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}
RETENTION_DAYS=${RETENTION_DAYS:-14}

export PGPASSWORD="$POSTGRES_PASSWORD"

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "Dumping Postgres database..."
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f "$TMP_DIR/db.dump"

echo "Archiving app config and dumps..."
tar czf "$TMP_DIR/keyguardian_backup_$DATE.tgz" -C "$TMP_DIR" db.dump -C /etc/letsencrypt . || true

echo "Uploading to S3 s3://$S3_BUCKET/backups/keyguardian/$DATE.tgz"
aws s3 cp "$TMP_DIR/keyguardian_backup_$DATE.tgz" "s3://$S3_BUCKET/backups/keyguardian/$DATE.tgz"

echo "Applying retention policy (older than $RETENTION_DAYS days)"
aws s3 ls "s3://$S3_BUCKET/backups/keyguardian/" | awk '{print $4, $1" "$2}' | while read -r key datetime; do
  ts=$(date -j -f "%Y-%m-%d %H:%M" "$datetime" +%s 2>/dev/null || date -d "$datetime" +%s 2>/dev/null || echo 0)
  if [ "$ts" -gt 0 ]; then
    age_days=$(( ( $(date +%s) - ts ) / 86400 ))
    if [ "$age_days" -gt "$RETENTION_DAYS" ]; then
      echo "Deleting s3://$S3_BUCKET/backups/keyguardian/$key (age ${age_days}d)"
      aws s3 rm "s3://$S3_BUCKET/backups/keyguardian/$key" || true
    fi
  fi
done

echo "Backup complete"


