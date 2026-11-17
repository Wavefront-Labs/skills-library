---
id: computing-software.cloud-infrastructure-engineering.docker.backing-up-all-volumes-of-a-compose-project
name: backing-up-all-volumes-of-a-compose-project
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, volume-backup, compose-volume-backup, compose-volumes, offen-docker-volume-backup, restore-test, labels]
level: practitioner
status: docs-checked
description: "Back up every named volume of a Compose project: find them by project label, stop or quiesce services, tar each one, restore into fresh volumes, or use a sidecar."
sources: ["https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes", "https://docs.docker.com/reference/compose-file/volumes/", "https://offen.github.io/docker-volume-backup/", "https://github.com/offen/docker-volume-backup"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backing up all volumes of a Compose project

Compose names project volumes `<project>_<volume>` (unless a volume sets `name:` or is
`external`) and labels them `com.docker.compose.project` and `com.docker.compose.volume`,
which makes them easy to enumerate.

## Script
```bash
#!/usr/bin/env bash
set -euo pipefail
PROJECT=${1:?project name}; DEST=${2:-/backups}/$PROJECT/$(date +%F_%H%M)
mkdir -p "$DEST"
cd /srv/$PROJECT

docker compose config --volumes                    # declared volume names, one per line
vols=$(docker volume ls -q --filter label=com.docker.compose.project="$PROJECT")

docker compose stop                                # consistency: nothing writing
for v in $vols; do
  docker run --rm -v "$v":/v:ro -v "$DEST":/b alpine \
    tar czf "/b/$v.tgz" -C /v .
done
docker compose start

cp compose*.yaml .env "$DEST"/ 2>/dev/null || true   # config travels with the data
ls -lh "$DEST"
```
This follows the pattern in the Docker volumes documentation: mount the volume and a host
directory into a throwaway container and run `tar`. Databases: prefer a logical dump taken
with the database's own tool while it runs, or do both.

## Restore into fresh volumes
```bash
for f in "$DEST"/shop_*.tgz; do
  v=$(basename "$f" .tgz); nv=${v/shop_/shop-restore_}
  docker volume create "$nv"
  docker run --rm -v "$nv":/v -v "$DEST":/b alpine sh -c "cd /v && tar xzf /b/$v.tgz"
done
```
Point a test project at the restored volumes with `external: true` and `name:` in its
Compose file (the Compose file reference defines both) and start it. Restoring under
different volume names proves the backup works without touching production.

## Sidecar alternative
`offen/docker-volume-backup` runs as a container with the volumes mounted read-only under
`/backup` (its default `BACKUP_SOURCES`), stops containers carrying the label
`docker-volume-backup.stop-during-backup=true` while it archives, and can write to a local
`/archive` mount or upload to S3, WebDAV or SSH targets. Settings are environment variables
such as `BACKUP_CRON_EXPRESSION` and `BACKUP_RETENTION_DAYS`:
```yaml
services:
  app:
    image: app:1.0
    volumes: [pgdata:/var/lib/data]
    labels:
      - docker-volume-backup.stop-during-backup=true   # label goes on the container to stop
  backup:
    image: offen/docker-volume-backup:v2
    environment:
      BACKUP_CRON_EXPRESSION: "0 3 * * *"
      BACKUP_RETENTION_DAYS: "14"
    volumes:
      - pgdata:/backup/pgdata:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro   # needed to stop labelled containers
      - /srv/backups:/archive
volumes:
  pgdata:
```

## Gotchas
- External volumes (`external: true`) are managed outside the project; add them to the list
  explicitly.
- Bind mounts are not volumes; back them up from the host path.
- Stopping services means downtime; schedule it or use application-level dumps.

## Checked
Date 2026-10-23. Method: documentation only; no commands were run.
Docker docs (docker/docs main): volume backup and restore with a throwaway container and
`tar`; Compose file reference for `volumes` (labels `com.docker.compose.project` and
`com.docker.compose.volume`, `external`, `name`); `docker compose config --volumes` option
(Compose v5.6.1 CLI reference). offen/docker-volume-backup (latest release v2.49.3): the
`/backup` default for `BACKUP_SOURCES`, the `/archive` local mount, `BACKUP_CRON_EXPRESSION`,
`BACKUP_RETENTION_DAYS`, the `docker-volume-backup.stop-during-backup=true` label and the
`:v2` image tag, and S3, WebDAV and SSH storage options. Removed: the `compose create`
restore trick and exact volume-label claims for restored volumes, which no documentation
covers.
