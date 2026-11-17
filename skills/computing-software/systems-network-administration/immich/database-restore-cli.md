---
id: computing-software.systems-network-administration.immich.database-restore-cli
name: database-restore-cli
category: computing-software
field: systems-network-administration
product: immich
tags: [pg-dump, psql, db-skip-migrations, docker-compose, restore]
level: advanced
status: docs-checked
description: "Back up Immich Postgres with pg_dump in the container and restore into a fresh stack with psql in a single transaction, including DB_SKIP_MIGRATIONS."
sources:
  - https://docs.immich.app/administration/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: dump and restore the database by command line on a Linux Docker Compose host.

Backup:

```bash
docker exec -t immich_postgres pg_dump --clean --if-exists --dbname=<DB_DATABASE_NAME> --username=<DB_USERNAME> | gzip > "/path/to/backup/dump.sql.gz"
```

Defaults are usually username `postgres` and database `immich` unless you changed them.

Restore requires a completely fresh install: the server must never have run since the containers were created, or you get Postgres conflicts such as "relation already exists".

```bash
docker compose down -v   # CAUTION: deletes all Immich data
# rm -rf DB_DATA_LOCATION  # CAUTION: only to permanently reset Postgres
docker compose pull
docker compose create
docker start immich_postgres
sleep 10
gunzip --stdout "/path/to/backup/dump.sql.gz" \
| sed "s/SELECT pg_catalog.set_config('search_path', '', false);/SELECT pg_catalog.set_config('search_path', 'public, pg_catalog', true);/g" \
| docker exec -i immich_postgres psql --dbname=<DB_DATABASE_NAME> --username=<DB_USERNAME> --single-transaction --set ON_ERROR_STOP=on
docker compose up -d
```

`--single-transaction --set ON_ERROR_STOP=on` commits everything or nothing, so the database is never left half-restored. Remove those flags only if you want partial progress.

If your platform cannot start the database without also starting the server, set `DB_SKIP_MIGRATIONS=true` before starting so the server does not run migrations that interfere.

For backups made by older releases, use the documentation version selector to find the older manual restore steps.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/backup-and-restore (Restore via Command Line).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
