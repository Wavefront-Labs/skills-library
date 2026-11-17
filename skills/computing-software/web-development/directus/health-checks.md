---
id: computing-software.web-development.directus.health-checks
name: health-checks
category: computing-software
field: web-development
product: directus
tags: [health-checks, server-ping, server-health, container-healthcheck]
level: practitioner
status: docs-checked
description: "Use Directus /server/ping for liveness and the authenticated /server/health for dependency checks in Docker and monitoring."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/self-hosting/3.deploying.md
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/database.md
  - https://raw.githubusercontent.com/directus/docs/main/content/configuration/cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two endpoints:

- `/server/ping`: returns `pong` while the HTTP server runs, regardless of dependencies, no auth needed. Use for liveness, load balancer probes and container health checks.
- `/server/health`: reports dependencies (database, Redis, storage, email). Returns `503` if any is unhealthy (e.g. missing email transport config). It is resource intensive, so use only when you need dependency verification.

`/server/health` needs authentication and returns `403` unauthenticated. Non-admins see only the overall `status`; admins see each check. For a monitoring tool, create a dedicated user and send its static token.

Compose health check:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget --spider -q http://localhost:8055/server/ping || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 5
```

Other services can then wait with `depends_on: { directus: { condition: service_healthy } }`.

Tuning: `DB_HEALTHCHECK_THRESHOLD` and `CACHE_HEALTHCHECK_THRESHOLD` (ms, default 150); see the Health Check config page for caching.

## Checked

2026-11-04: /server/ping and /server/health behaviour, 503 and 403 responses, admin versus non-admin output, compose health check and depends_on, and both 150 ms thresholds confirmed against the Directus Deploying, Database and Cache pages. Removed a Verify line the pages do not state.

Method: documentation only; no commands were run.
