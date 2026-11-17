---
id: computing-software.systems-network-administration.healthchecks.docker-postgres-upgrade
name: docker-postgres-upgrade
category: computing-software
field: systems-network-administration
product: healthchecks
tags: [healthchecks, postgres-upgrade, pgautoupgrade, docker-volume, database-backup]
level: sme
status: docs-checked
description: "Upgrade the PostgreSQL major version behind a Docker Healthchecks stack using the pgautoupgrade container against the data volume, with backup first."
sources:
  - https://raw.githubusercontent.com/healthchecks/healthchecks/master/templates/docs/self_hosted_docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The docs example upgrades from `postgres:12` to `postgres:16`.

1. Take a full database backup first.
2. Stop the containers: `docker compose stop`
3. Find the Postgres data volume name: `docker volume ls`
4. Run pgautoupgrade against that volume (replace the placeholder and the example password):

```
docker run --rm --name pgauto -it \
   --mount type=volume,source=<pg-volume-name-here>,target=/var/lib/postgresql/data \
   -e POSTGRES_PASSWORD=password \
   -e PGAUTO_ONESHOT=yes \
   pgautoupgrade/pgautoupgrade:16-bookworm
```

5. Change the database image in `docker-compose.yml` to `postgres:16`.
6. Start the containers: `docker compose up`

## Checked

2026-11-04. Confirmed against the Healthchecks Docker documentation: the postgres:12 to postgres:16 example, backup first, docker compose stop, docker volume ls, the pgautoupgrade command, updating the compose image and starting the containers. Removed three notes (what PGAUTO_ONESHOT does, a same-major-version rule and a keep-the-backup check) that the page does not state.

Method: documentation only; no commands were run.
