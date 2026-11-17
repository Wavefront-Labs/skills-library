---
id: computing-software.cloud-infrastructure-engineering.docker.scheduled-database-dumps-from-a-sidecar
name: scheduled-database-dumps-from-a-sidecar
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, db-backup-cron, pg-dump-container, backup-sidecar, supercronic, ofelia, mysqldump, retention, restore-test, compose]
level: practitioner
status: draft
description: "Schedule logical database dumps in a Compose stack: host cron vs sidecar, supercronic/ofelia, client version matching, atomic files, retention, off-host copies, and restore tests."
sources: ["https://www.postgresql.org/docs/current/app-pgdump.html", "https://github.com/aptible/supercronic", "https://github.com/mcuadros/ofelia", "https://dev.mysql.com/doc/refman/8.4/en/mysqldump.html", "https://docs.docker.com/reference/compose-file/interpolation/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scheduled database dumps from a sidecar

**Goal:** a containerised database gets a consistent logical dump on a schedule, old dumps
expire, copies leave the host, and someone notices when it stops working.

## Three ways to schedule
1. **Host cron** + `docker compose exec -T db pg_dump ...`: simplest, but lives outside the
   stack's config and breaks if the project name or path changes.
2. **Sidecar with a cron runner** (below): versioned with the stack, portable.
3. **Scheduler that execs into the DB container** (ofelia): no extra client image, jobs
   declared as labels.

## Sidecar with supercronic (Postgres)
`crond` in containers fights with PID 1, env vars and logging; **supercronic** runs crontabs
in the foreground, passes the environment through and logs to stdout.
```dockerfile
# backup/Dockerfile
FROM postgres:16            # same major as the server (pg_dump must be >= server version)
ARG SUPERCRONIC_VERSION=v0.2.33
ADD https://github.com/aptible/supercronic/releases/download/${SUPERCRONIC_VERSION}/supercronic-linux-amd64 /usr/local/bin/supercronic
RUN chmod +x /usr/local/bin/supercronic
COPY crontab backup.sh /etc/backup/
USER postgres
ENTRYPOINT ["supercronic", "/etc/backup/crontab"]
```
```
# crontab
15 2 * * * /etc/backup/backup.sh
```
```sh
#!/bin/sh
set -eu
f="/backups/app-$(date +%Y%m%dT%H%M%S).dump"
pg_dump -Fc -f "$f.partial"          # -Fc = compressed, restorable with pg_restore -j
mv "$f.partial" "$f"                  # atomic: half-written dumps never look complete
find /backups -name 'app-*.dump' -mtime +14 -delete
```
```yaml
services:
  backup:
    build: ./backup
    environment:
      PGHOST: db
      PGUSER: app
      PGDATABASE: app
      PGPASSFILE: /run/secrets/pgpass          # "db:5432:app:app:<pw>", mode 0600
    secrets: [pgpass]
    volumes: [./backups:/backups]
    depends_on: { db: { condition: service_healthy } }
    restart: unless-stopped
```
Set the container `TZ` if schedules should follow local time.

## Inline loop (no extra binary)
```yaml
    command: ["sh", "-c", "while :; do /etc/backup/backup.sh; sleep 86400; done"]
```
Fine for dev; drifts and runs at container start time. Inside a Compose `command` string,
write `$$` for a literal `$`.

## ofelia: jobs as labels
```yaml
  ofelia:
    image: mcuadros/ofelia:latest
    command: daemon --docker
    volumes: [/var/run/docker.sock:/var/run/docker.sock:ro]
  db:
    labels:
      ofelia.enabled: "true"
      ofelia.job-exec.dump.schedule: "@every 24h"
      ofelia.job-exec.dump.command: "sh -c 'pg_dump -U app -Fc -f /backups/app.dump app'"
```
Needs the socket (high privilege) and a backup volume mounted in the DB container.

## Other engines
- MySQL/MariaDB: `mysqldump --single-transaction --routines --triggers --events` (InnoDB
  consistent without locks); MariaDB image ships `mariadb-dump`.
- MongoDB: `mongodump --archive --gzip`.
- Redis: `BGSAVE` then copy `dump.rdb`.

## Off-host and monitoring
- A dump on the same disk is not a backup: add `restic`/`rclone` to the job or a second
  service syncing `/backups` to object storage.
- Ping a dead-man switch (healthchecks.io-style URL) at the end of `backup.sh`; or a
  healthcheck that fails if the newest dump is older than 26 h:
  `test: ["CMD-SHELL", "find /backups -name 'app-*.dump' -mmin -1560 | grep -q ."]`.

## Verify (restore test)
```bash
docker compose run --rm backup /etc/backup/backup.sh
docker run --rm -d --name restore-test -e POSTGRES_PASSWORD=x postgres:16 && sleep 5
docker cp "$(ls -t backups/*.dump | head -1)" restore-test:/tmp/app.dump
docker exec restore-test sh -c 'createdb -U postgres app && pg_restore -U postgres -d app -j 4 /tmp/app.dump'
docker exec restore-test psql -U postgres -d app -c '\dt'; docker rm -f restore-test
```
