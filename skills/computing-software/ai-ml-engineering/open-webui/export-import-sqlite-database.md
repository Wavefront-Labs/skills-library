---
id: computing-software.ai-ml-engineering.open-webui.export-import-sqlite-database
name: export-import-sqlite-database
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [database-migration, sqlite, wal, migration, docker-cp, webui-db]
level: practitioner
status: docs-checked
description: "Move or back up an Open WebUI SQLite database safely: stop the container, checkpoint the WAL, docker cp webui.db, and import after clearing wal and shm files."
sources:
  - https://docs.openwebui.com/tutorials/maintenance/database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: copy `webui.db` from one Open WebUI server to another without losing recent writes. Applies only to the internal SQLite database, not PostgreSQL (use PostgreSQL tools there).

## What a move needs
`webui.db` holds accounts, chats, settings, file and knowledge records, but not the files. Uploads (`/app/backend/data/uploads`) and the vector store (`/app/backend/data/vector_db`) stay behind, so chats referencing files break. For a complete move copy the whole `/app/backend/data` directory and keep the same `WEBUI_SECRET_KEY` (the Docker image writes an auto-generated key to `/app/backend/.webui_secret_key`, outside that directory). With an external vector DB such as PGVector the vectors live there.

## Export (source)
SQLite runs in WAL mode, so recent commits sit in `webui.db-wal`. The Admin Settings > Database download omits it; do not use it.
```bash
docker stop open-webui
docker run --rm --volumes-from open-webui --entrypoint python3 "$(docker inspect -f '{{.Config.Image}}' open-webui)" -c "import sqlite3; db = sqlite3.connect('/app/backend/data/webui.db'); db.execute('PRAGMA wal_checkpoint(TRUNCATE)'); db.close()"
docker cp open-webui:/app/backend/data/webui.db ./webui.db
docker start open-webui
```
Transfer the file with any tool (the docs suggest FileZilla).

## Import (destination)
Install and start Open WebUI per the quick start, then stop it:
```bash
docker stop open-webui
docker run --rm --volumes-from open-webui --entrypoint rm "$(docker inspect -f '{{.Config.Image}}' open-webui)" -f /app/backend/data/webui.db-wal /app/backend/data/webui.db-shm
docker cp ./webui.db open-webui:/app/backend/data/webui.db
docker start open-webui
```

## Gotchas
- Never mix `webui.db-wal` or `webui.db-shm` from a different database copy; delete destination sidecar files before replacing `webui.db`.
- Do this before updates or modifications as a backup too.
- Related reference: the database schema page and the backups guide.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page tutorials/maintenance/database (read in full): SQLite-only scope, what webui.db holds and what stays behind (uploads, vector_db), same WEBUI_SECRET_KEY and the .webui_secret_key location, WAL mode and webui.db-wal, the Admin Settings Database download caveat, the stop, checkpoint, docker cp and start export commands, FileZilla suggestion, the import sequence with sidecar removal, the do-not-mix-sidecars note and the backup use. Nothing removed.
Method: documentation only; no commands were run.
