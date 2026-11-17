---
id: computing-software.collaboration-platform-administration.vikunja.docker-sqlite-volume
name: docker-sqlite-volume
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, sqlite-container, database-path-preset, env-beats-config, bind-mount-db]
level: practitioner
status: docs-checked
description: "Persist Vikunja's SQLite database in Docker: the preset database path, why a mounted config.yml cannot move it, and when to prefer MySQL or PostgreSQL."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/config.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The official image presets two environment variables: `VIKUNJA_SERVICE_ROOTPATH=/app/vikunja/` and `VIKUNJA_DATABASE_PATH=/db/vikunja.db`. So SQLite lives at `/db/vikunja.db` unless you override it.

Persist it by mounting `./db:/db` (and `./files:/app/vikunja/files`), after `mkdir $PWD/files $PWD/db` and `chown 1000 $PWD/files $PWD/db`.

Environment variables take precedence over the config file, so setting `service.rootpath` or `database.path` in a mounted `config.yml` has no effect in the official container. To store the database elsewhere, change the host side of the bind mount (for example `./my-db:/db`) or override the environment variable.

A relative `files.basepath` resolves against `service.rootpath`, so uploads default to `/app/vikunja/files`.

Set `VIKUNJA_DATABASE_TYPE` to `sqlite` or remove it (sqlite is the default type), and drop the db service.

The docs recommend MySQL or PostgreSQL once the instance has more than a handful of users.

## Checked

2026-11-04. Confirmed against the Vikunja Configuration page (setup/config: preset rootpath and database path, env precedence, relative files.basepath), the Full docker example (mounts, mkdir and chown, MySQL or PostgreSQL recommendation) and config-raw.json (sqlite as default database.type). Nothing removed.

Method: documentation only; no commands were run.
