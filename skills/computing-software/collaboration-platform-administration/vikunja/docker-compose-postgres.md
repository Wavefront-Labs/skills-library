---
id: computing-software.collaboration-platform-administration.vikunja.docker-compose-postgres
name: docker-compose-postgres
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, docker-compose, postgres-container, service-secret, healthcheck-depends-on]
level: practitioner
status: docs-checked
description: "Run Vikunja with a PostgreSQL container under Docker Compose: required environment variables, volumes, health-gated startup and the first-run checks."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/docker-start-to-finish.mdx
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/full-docker-example.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The reference compose file defines two services: `vikunja` (image `vikunja/vikunja`, API plus frontend) and `db` (`postgres:18`).

Vikunja environment:
- `VIKUNJA_SERVICE_PUBLICURL`: the public URL, including a non-standard port, otherwise creating a user gives an "unauthorized" error.
- `VIKUNJA_SERVICE_SECRET`: a long random secret.
- `VIKUNJA_DATABASE_TYPE=postgres`, `VIKUNJA_DATABASE_HOST` (must equal the db service name), `VIKUNJA_DATABASE_USER`, `VIKUNJA_DATABASE_PASSWORD`, `VIKUNJA_DATABASE_DATABASE`.

Mount `./files:/app/vikunja/files`, publish `3456:3456`, set `restart: unless-stopped`, and use `depends_on` with `condition: service_healthy` against a `pg_isready` healthcheck on the db.

Run `docker compose up`, then look for the "http server started on [::]:3456" log line. Check `/api/v1/info` in a browser, then the root URL for the login page. Switch to `docker compose up -d` to run in the background.

Once all users are registered you may disable registration with `service.enableregistration`.

## Checked

2026-11-04. Confirmed against the Vikunja Docker Walkthrough (setup/docker-start-to-finish) and Full docker example (setup/full-docker-example): the two services, postgres:18, environment variables, publicurl port warning, files mount, port 3456, restart policy, health-gated depends_on, startup log line, /api/v1/info, up -d, and service.enableregistration. Nothing removed.

Method: documentation only; no commands were run.
