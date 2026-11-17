---
id: computing-software.data-engineering.metabase.running-on-docker
name: running-on-docker
category: computing-software
field: data-engineering
product: metabase
tags: [docker, container, docker-secrets, plugins-directory, h2-recovery, healthcheck]
level: practitioner
status: docs-checked
description: "Run Metabase in Docker: images, port mapping, external Postgres app database, plugins mount, _FILE secrets, MB_DB_FILE, H2 recovery from a stopped container."
sources:
  - https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Images: `metabase/metabase:latest` (open source) and `metabase/metabase-enterprise:latest` (needs a license token). Basic run: `docker run -d -p 3000:3000 --name metabase metabase/metabase`. Logs: `docker logs -f metabase`. Remap the port with `-p 12345:3000`.

Production app database: the default H2 database lives inside the container, so `docker rm` loses all questions, dashboards and collections. Create a Postgres database and pass `MB_DB_TYPE=postgres`, `MB_DB_DBNAME`, `MB_DB_PORT=5432`, `MB_DB_USER`, `MB_DB_PASS`, `MB_DB_HOST`. Metabase connects from inside the container, so the host must resolve there.

Useful settings:
- `MUID` and `MGID` match file permissions; `JAVA_TIMEZONE` sets the timezone.
- `MB_DB_FILE=/metabase-data/metabase.db` with `-v ~/metabase-data:/metabase-data` keeps H2 on a volume.
- Mount drivers with `--mount type=bind,source=/path/to/plugins,destination=/plugins`; the directory must be readable and writable.
- Secrets: append `_FILE`, such as `MB_DB_PASS_FILE=/run/secrets/db_password`. Supported: `MB_DB_USER`, `MB_DB_PASS`, `MB_DB_CONNECTION_URI`, `MB_EMAIL_SMTP_USERNAME`, `MB_EMAIL_SMTP_PASSWORD`, `MB_LDAP_PASSWORD`, `MB_LDAP_BIND_DN`.

Compose healthcheck: `curl --fail -I http://localhost:3000/api/health || exit 1`, interval 15s, timeout 5s, retries 5. The docs call their compose file an example, not production.

Recovery: H2 sits at `/metabase.db/metabase.db.mv.db`; copy out with `docker cp CONTAINER_ID:/metabase.db ./`. For a stopped container, `docker commit <id> <image-name>` then run that image.

## Checked
2026-11-03. Confirmed against the Metabase docs page Installation and operation, Running Metabase on Docker: images and quick start, port remap, MB_DB_* Postgres example, MUID/MGID, JAVA_TIMEZONE, MB_DB_FILE volume, plugins bind mount, _FILE secrets and the supported variable list, compose healthcheck, docker cp recovery and docker commit steps. Nothing removed.
Method: documentation only; no commands were run.
