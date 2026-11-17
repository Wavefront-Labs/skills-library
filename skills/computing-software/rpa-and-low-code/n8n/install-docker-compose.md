---
id: computing-software.rpa-and-low-code.n8n.install-docker-compose
name: install-docker-compose
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, docker-compose, env-file, postgres, sandbox, healthz]
level: practitioner
status: docs-checked
description: "Build an n8n Docker Compose setup by hand with the sandbox stack, .env secrets, health checks and the optional Postgres 18 service with the PGDATA warning."
sources:
  - https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: a hand-built Compose project for n8n plus the sandbox services behind n8n Assistant. Needs Docker Engine, Compose v2 (`docker compose version`), at least 4 GB RAM and 2 vCPUs (the Docker-in-Docker sandbox runner needs headroom). On Windows use WSL and keep the project inside the WSL filesystem, not `/mnt/c/...`.

1. `mkdir n8n && cd n8n`.
2. Create `.env` with `N8N_VERSION`, `N8N_SANDBOX_VERSION`, `N8N_RUNNERS_AUTH_TOKEN`, `SANDBOX_API_KEYS`, `SANDBOX_API_RUNNER_REGISTRATION_TOKEN`, `SANDBOX_API_RUNNER_API_KEY`, `N8N_SANDBOX_SERVICE_API_KEY` (must match a value in `SANDBOX_API_KEYS`), `SEARXNG_SECRET`, and `N8N_INSTANCE_AI_SEARXNG_URL=http://searxng:8080`. Keep it out of version control.
3. Create `searxng-settings.yml` (`use_default_settings: true`, `search.formats: [html, json]`), because n8n's web search needs the JSON API.
4. Create `compose.yml` as the page shows (it names `get-n8n-compose.yml`; the embedded file did not load when checked, so take it from the live page).
5. `docker compose up -d` then `docker compose ps`; wait until `sandbox-api` is `healthy`.
6. Verify: `docker compose exec n8n wget -qO- http://sandbox-api:8080/healthz`, `docker compose logs sandbox-api | grep -i runner`, `curl -sf http://localhost:5678/healthz`.

With no database service n8n uses SQLite; the `n8n-data` volume holds the database and encryption key.

## Postgres instead of SQLite (fresh instance only)
Add `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` to `.env`; add a `postgres:18` service with a health check `pg_isready -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}` and `PGDATA: /var/lib/postgresql/data`. Do not remove `PGDATA`: Postgres 18 would otherwise write outside the volume and start empty. Moving an older Postgres straight to 18 fails with `database files are incompatible with server`; back up with `pg_dumpall` first. In the n8n service set `DB_TYPE: postgresdb`, `DB_POSTGRESDB_HOST: postgres`, `DB_POSTGRESDB_PORT: '5432'` and the database/user/password variables, with `depends_on` postgres `service_healthy`. SQLite data does not migrate automatically.

## Troubleshooting
`sandbox-api`/runner cert errors: check `docker compose logs sandbox-certs`. Runner crash-looping with `... must be set`: missing `SANDBOX_RUNNER_API_KEYS` or `SANDBOX_RUNNER_REGISTRATION_TOKEN`. The privileged `sandbox-runner-1` is equivalent to root on the host: never expose it; the mTLS certs do not auto-renew.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/install-options/install-using-docker-compose

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Removed the unconfirmed repository path `docker/get-n8n-compose.yml`.

Method: documentation only; no commands were run.
