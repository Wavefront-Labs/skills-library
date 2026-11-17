---
id: computing-software.rpa-and-low-code.n8n.install-with-docker
name: install-with-docker
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, docker, install, postgresql, timezone, volumes]
level: intro
status: docs-checked
description: "Run self-hosted n8n with docker run: persistent n8n_data volume, timezone variables, optional PostgreSQL variables, and image update commands."
sources:
  - https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: start n8n in Docker with persistent data. The page is marked outdated in favour of the Docker Compose guide, but the commands still describe the container's essential settings.

```shell
docker volume create n8n_data

docker run -it --rm \
 --name n8n \
 -p 5678:5678 \
 -e GENERIC_TIMEZONE="<YOUR_TIMEZONE>" \
 -e TZ="<YOUR_TIMEZONE>" \
 -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true \
 -v n8n_data:<node-user-home>/.n8n \
 n8nio/n8n
```
Port `5678` is published; `TZ` sets the system timezone (what `date` returns), `GENERIC_TIMEZONE` sets the timezone for schedule nodes such as Schedule Trigger; `N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true` enforces secure permissions on the config file; the volume persists the `.n8n` folder in the node user home directory (the mount target in the command above). Open `http://localhost:5678`. `N8N_RUNNERS_ENABLED` is deprecated from n8n 2.0 (set `true` on 1.x to enable task runners).

## PostgreSQL
Default storage is SQLite. Add to the same command: `-e DB_TYPE=postgresdb`, `DB_POSTGRESDB_DATABASE`, `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_SCHEMA`, `DB_POSTGRESDB_PASSWORD`. Keep the volume anyway: `.n8n` still holds encryption keys, instance logs and source control assets (the alternative is setting `N8N_ENCRYPTION_KEY`).

## Updating
```shell
docker pull n8nio/n8n            # latest stable
docker pull n8nio/n8n:1.81.0     # specific version
docker pull n8nio/n8n:next       # unstable
docker ps -a
docker stop <container_id>
docker rm <container_id>
docker run --name=<container_name> [options] -d n8nio/n8n
```
After pulling, stop and remove the old container, then start again with the same options.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/install-options/install-with-docker

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
