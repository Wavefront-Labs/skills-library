---
id: computing-software.systems-network-administration.immich.environment-variables
name: environment-variables
category: computing-software
field: systems-network-administration
product: immich
tags: [env, db-hostname, redis-hostname, docker-secrets, timezone]
level: practitioner
status: docs-checked
description: "Key Immich environment variables for Docker Compose: version, locations, database, Redis, ports, workers, logging and _FILE secrets."
sources:
  - https://docs.immich.app/install/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: find and set the right variable in `.env`.

Docker Compose level (host paths):

- `IMMICH_VERSION`: image tag, for example `v3`.
- `UPLOAD_LOCATION`: host path for uploads.
- `DB_DATA_LOCATION`: host path for the Postgres database.

General (server): `TZ`; `IMMICH_ENV`; `IMMICH_LOG_LEVEL` (verbose, debug, log, warn, error); `IMMICH_LOG_FORMAT` (`console` or `json`); `IMMICH_CONFIG_FILE`; `IMMICH_TRUSTED_PROXIES` (comma-separated IPs); `IMMICH_ALLOW_SETUP` (`false` disables the admin sign-up and database restore start endpoints); `IMMICH_IGNORE_MOUNT_CHECK_ERRORS`; `IMMICH_MEDIA_LOCATION` (the docs say you probably should not set it).

Workers: `IMMICH_WORKERS_INCLUDE`, `IMMICH_WORKERS_EXCLUDE`.

Ports: `IMMICH_HOST` default `0.0.0.0`; `IMMICH_PORT` default `2283` for the server and `3003` for machine learning.

Database: `DB_URL`, or `DB_HOSTNAME` (default `database`), `DB_PORT` (`5432`), `DB_USERNAME` and `DB_PASSWORD` (default `postgres`), `DB_DATABASE_NAME` (`immich`), `DB_SSL_MODE`, `DB_SKIP_MIGRATIONS`, `DB_STORAGE_TYPE` (`SSD` or `HDD`).

Redis: `REDIS_URL`, `REDIS_SOCKET`, or `REDIS_HOSTNAME` (`redis`), `REDIS_PORT` (`6379`), `REDIS_USERNAME`, `REDIS_PASSWORD`, `REDIS_DBINDEX` (`0`).

Machine learning examples: `MACHINE_LEARNING_MODEL_TTL` (300), `MACHINE_LEARNING_WORKERS` (1), `MACHINE_LEARNING_DEVICE_IDS`, `MACHINE_LEARNING_CACHE_FOLDER` (`/cache`).

Telemetry: `IMMICH_TELEMETRY_INCLUDE`, `IMMICH_TELEMETRY_EXCLUDE`.

Secrets: `DB_HOSTNAME`, `DB_DATABASE_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_URL` and `REDIS_PASSWORD` accept `_FILE` variants, for example `DB_PASSWORD_FILE`, which read the value from a file such as a Docker secret.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: install/environment-variables (all sections).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
