#!/bin/bash
# Nightly Postgres dump for the SAFE app. Runs via backup-db.timer (see
# backup-db.service). Keeps 14 days locally in /opt/backups; syncing that
# directory off-box is a separate step (rclone/rsync to remote storage).
set -euo pipefail

COMPOSE_DIR="/opt/safe"
BACKUP_DIR="/opt/backups"
RETENTION_DAYS=14
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT="$BACKUP_DIR/safe_db_$STAMP.sql.gz"

mkdir -p "$BACKUP_DIR"

cd "$COMPOSE_DIR"
set -a
source .env
set +a

docker compose exec -T db pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip > "$OUT"

find "$BACKUP_DIR" -name 'safe_db_*.sql.gz' -mtime "+$RETENTION_DAYS" -delete

echo "Backed up to $OUT ($(du -h "$OUT" | cut -f1))"
