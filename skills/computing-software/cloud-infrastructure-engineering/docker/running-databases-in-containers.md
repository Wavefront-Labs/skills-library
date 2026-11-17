---
id: computing-software.cloud-infrastructure-engineering.docker.running-databases-in-containers
name: running-databases-in-containers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, stateful, database-container, postgres-container, mysql-container, data-persistence, named-volume, pgdata, init-scripts, docker-entrypoint-initdb, shm-size, stop-grace-period, major-upgrade, pg-upgrade]
level: practitioner
status: docs-checked
description: "Postgres, MySQL, Redis and Mongo in Docker without losing data: volume paths (Postgres 18 change), init scripts, shm, healthchecks and major upgrades."
sources: ["https://hub.docker.com/_/postgres", "https://hub.docker.com/_/mysql", "https://hub.docker.com/_/redis", "https://hub.docker.com/_/mongo", "https://www.postgresql.org/docs/current/pgupgrade.html", "https://github.com/compose-spec/compose-spec/blob/main/spec.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running databases in containers

**Goal:** a containerised database that survives `docker compose down`, image upgrades and
host reboots, starts healthy before its clients, and can be upgraded across major versions.

## Persist to a named volume at the image's data path
| Image | Data path | Init-script dir |
|---|---|---|
| `postgres` 17 and below | `/var/lib/postgresql/data` (`PGDATA`) | `/docker-entrypoint-initdb.d/` (`.sql`, `.sql.gz`, `.sh`) |
| `postgres` 18 and above | volume at `/var/lib/postgresql`; `PGDATA` is `/var/lib/postgresql/<major>/docker` | same |
| `mysql` | `/var/lib/mysql` | `/docker-entrypoint-initdb.d/` |
| `mongo` | `/data/db` | `/docker-entrypoint-initdb.d/` (`.sh`, `.js`) |
| `redis` | `/data` (written when persistence is enabled, for example `--save 60 1`) | n/a |

```yaml
services:
  db:
    image: postgres:17
    restart: unless-stopped
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/pg_pw     # *_FILE form documented in the postgres README
      POSTGRES_USER: app
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
      - ./init:/docker-entrypoint-initdb.d:ro
    secrets: [pg_pw]
    shm_size: 256m
    stop_grace_period: 1m
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 3s
      retries: 20
volumes:
  pgdata: {}
secrets:
  pg_pw: {file: ./pg_pw.txt}
```
- **Named volume, not anonymous.** The postgres README: the image declares a volume at the
  data path, so without a data volume at that exact path the runtime creates an anonymous
  volume that is not reused when the container is re-created. For 17 and below, mount at
  `/var/lib/postgresql/data`, not `/var/lib/postgresql`.
- **PostgreSQL 18 and above:** `PGDATA` became version specific (`/var/lib/postgresql/18/docker`)
  and the declared `VOLUME` moved to `/var/lib/postgresql`; target mounts there. This lets
  `pg_upgrade --link` work across majors when `/var/lib/postgresql` is mounted.
- On Docker Desktop prefer named volumes for database data (see the Windows share
  permission notes: shared volumes get a fixed `0777` mode).

## Init scripts run exactly once
The postgres README: `/docker-entrypoint-initdb.d` scripts and the Docker-specific variables
(`POSTGRES_PASSWORD`, ...) only take effect when the container starts with an **empty** data
directory; an existing database is left untouched. So "I changed init.sql and nothing
happened" means the change must be applied manually or against a fresh volume (which
destroys data). The mysql and mongo READMEs describe the same first-start behaviour.

## Settings that bite
- `shm_size`: the postgres README notes the container default `/dev/shm` is 64 MB and that
  exhausting it produces `could not resize shared memory segment ... No space left on
  device`; Compose's `shm_size` raises it.
- `stop_grace_period` / `docker stop -t`: give a busy database more time than the default to
  shut down cleanly, so it does not need crash recovery on the next start.
- Memory limits: set a container limit and size the database's own buffers to fit.
- Redis: persistence must be enabled (for example `redis-server --save 60 1`) for data to
  be written to `/data`.
- Publish database ports on loopback only on a dev box (`127.0.0.1:5432:5432`; compose-spec
  short syntax accepts a host IP).

## Clients must wait on health, not on start
`depends_on: {db: {condition: service_healthy}}` in the app service. Use `pg_isready` with the app user and database rather than a bare TCP check.

## Major version upgrade (Postgres)
PostgreSQL data directories are not compatible across major versions (see the PostgreSQL
`pg_upgrade` documentation). Procedure with a logical dump:
```bash
docker compose exec db pg_dumpall -U app > dump.sql     # 1. logical dump on the OLD version
docker compose down
# 2. edit image tag to postgres:17 and the volume name to pgdata17 (keep the old volume intact)
docker compose up -d db
cat dump.sql | docker compose exec -T db psql -U app    # 3. restore
# 4. verify, then docker volume rm <project>_pgdata when confident
```
For large datasets, `pg_upgrade` is the documented route (the 18+ volume layout exists to
allow `--link`). For MySQL and MongoDB, follow the upgrade section of each product's own
documentation and take a dump first.

## Backups
See `volume-tar-backup-clone-migrate-and-verify`; prefer logical dumps of a running database
over copying its live volume.

## Verify
```bash
docker compose down && docker compose up -d && docker compose exec db psql -U app -c '\dt'   # tables survive down/up
docker inspect -f '{{json .State.Health.Status}}' $(docker compose ps -q db)                  # "healthy"
docker compose exec db df -h /dev/shm                                                         # reflects shm_size
```

## Checked
Date: 2026-10-26. Documentation: docker-library postgres, mysql, mongo and redis READMEs (postgres tags at 18.6). Confirmed: data paths, the postgres 18 `PGDATA`/`VOLUME` change and the 17-and-below mount warning, init scripts only on empty data directories (postgres, mysql, mongo), `_FILE` password form, 64 MB `/dev/shm` default and its error text, redis `--save`. Removed as unconfirmed or wrong: the old single `/var/lib/postgresql/data` path for all versions, uid 999 column, the "server restarts once during init" claim, MySQL authentication-plugin advice, Redis sysctl and THP advice, the pg_upgrade error message, `pgautoupgrade` and `tianon` images, MySQL and Mongo upgrade specifics, the pinned `postgres:16` tag, the OOM and bind-mount explanations. Sources were also corrected (the `pgupgrade` URL is replaced by the PostgreSQL pgupgrade page).
Method: documentation only; no commands were run.
