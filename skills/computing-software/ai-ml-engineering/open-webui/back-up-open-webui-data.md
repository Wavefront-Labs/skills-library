---
id: computing-software.ai-ml-engineering.open-webui.back-up-open-webui-data
name: back-up-open-webui-data
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [backups, rclone, rsync, sqlite, chromadb, snapshots]
level: practitioner
status: docs-checked
description: "Plan and script backups of the Open WebUI data directory (webui.db, uploads, vector_db) with rclone or rsync, cold versus live backups, and retention."
sources:
  - https://docs.openwebui.com/tutorials/maintenance/backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep independent, restorable copies of an Open WebUI instance. (The docs mark this tutorial as a community contribution, not supported by the Open WebUI team, and assume a Docker install.)

## What to back up
Data is persisted in the container at `/app/backend/data` (Docker volume `open-webui:/app/backend/data`; Ollama models use `ollama:/root/.ollama`). Find the host path with `docker volume inspect open-webui`, or note your fixed bind (for example `/opt/open-webui:/app/backend/data`). Contents:

| Item | Meaning |
|---|---|
| `webui.db` | SQLite database (users, chats, settings) |
| `uploads/` | user-uploaded files |
| `vector_db/` | ChromaDB vector database |
| `cache/` | cache, can be excluded |
| `audit.log` | audit log, can be excluded |

Confirm Compose uses a persistent volume before relying on any backup: containers are ephemeral.

## Do not use the admin download
Admin Settings > Database download streams `webui.db` as on disk; with SQLite WAL mode recent writes may sit in `webui.db-wal`, so the file can miss data. Copy the DB yourself (see the export/import skill) or use `pg_dump` for PostgreSQL.

## File-level job (rclone to Backblaze B2)
Sync `uploads`, `vector_db`, and `webui.db` separately, each to its own destination (`b2://OpenWebUI-backups/user_uploads`, `/ChromaDB`, `/main_database`), excluding `cache/` and `audit.log`, with `rclone sync "$SOURCE" "$DEST" --exclude ... --progress --transfers=32 --checkers=16`, and exit non-zero on failure.

## Cold backups for integrity
Run `docker compose -f docker-compose.yml down`, sync, then `docker compose up -d`. This costs downtime, so consider live "dailies" plus cold weeklies.

## Native-tool variant
Before copying: `sqlite3 "$SOURCE/webui.db" ".backup '$SOURCE/webui.db.backup'"` and `tar -czvf chromadb_backup.tar.gz -C "$SOURCE" vector_db`, then `rclone copy` into a dated directory `open-webui-backup-YYYY-MM-DD` with `--exclude audit.log --exclude cache/** --exclude uploads/** --exclude vector_db`; the page's script prunes older dated directories with `rclone purge` to keep 3 weekly snapshots. Note that this script's excludes leave out `uploads/`, so back that up separately.

## Point-in-time snapshots
`rsync -av --delete --link-dest="$SNAPSHOT_DIR/<latest>" "$SOURCE_DIR/" "$SNAPSHOT_DIR/snapshot_<timestamp>"` gives hard-linked incrementals. Schedule with cron and log the output; test restores.

## How many copies
Do not treat the running app (even in the cloud) as a copy. Plan 1: daily incremental to S3 or B2, weekly pull to a home NAS. Plan 2: daily to both S3 and B2 plus weekly NAS. Host/VM snapshots can be layered on top. Not covered but worth considering: encryption at rest, disaster-recovery tests, borgbackup or restic, failure notifications.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page tutorials/maintenance/backups (read in full): data path and volume mounts, the file table, the admin Database download caveat (WAL), the rclone/B2 job and its flags, cold backup with compose down/up, the sqlite3 .backup and tar variant, the rsync link-dest snapshot, backup plans 1 and 2, and the additional topics. Added: the native-tool script excludes uploads/. Removed: nothing else.
Method: documentation only; no commands were run.
