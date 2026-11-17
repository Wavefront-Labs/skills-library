---
id: computing-software.collaboration-platform-administration.vikunja.docker-troubleshooting
name: docker-troubleshooting
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, scratch-image, docker-logs, db-connection-refused, commands-out-of-sync, testmail-noop]
level: practitioner
status: docs-checked
description: "Diagnose common Vikunja Docker start-up failures: database not ready, hostname mismatch, MySQL out-of-sync migration, harmless cache warning and SMTP test errors."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/docker-start-to-finish.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The image is built on `scratch`: there is no shell, so `docker exec -it vikunja sh` fails. Read `docker logs vikunja` instead.

Known failures:
- `Migration failed: dial tcp ... connection refused`: PostgreSQL was not ready on first start. `restart: unless-stopped` lets the container retry until the db is up.
- `lookup db on 127.0.0.11:53: server misbehaving`: `VIKUNJA_DATABASE_HOST` must match the db service name in the compose file.
- `Migration failed: commands out of sync` (MySQL): the docs offer no better fix than wiping the database files and starting over (`docker compose down`, remove `db/`, `docker compose up -d`). This wipes the database.
- `failed to create modcache index dir: mkdir /.cache: permission denied`: a known Go runtime warning, harmless.
- `testmail` fails with "not connected to SMTP server": Vikunja sends an SMTP `NOOP`, which minimal relays such as `msmtpd` do not support. Also keep SMTP settings in one place only; environment variables override the config file.

## Checked

2026-11-04: every error string and remedy checked against the Docker walkthrough page (troubleshooting section).

Method: documentation only; no commands were run.
