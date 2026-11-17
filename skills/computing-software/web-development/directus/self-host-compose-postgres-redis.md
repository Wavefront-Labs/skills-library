---
id: computing-software.web-development.directus.self-host-compose-postgres-redis
name: self-host-compose-postgres-redis
category: computing-software
field: web-development
product: directus
tags: [self-host-compose, postgres-redis, initial-admin-user, persistence-volumes]
level: practitioner
status: docs-checked
description: "Deploy self-hosted Directus with Docker Compose, PostgreSQL and Redis cache, persistent volumes, scripted first admin and health-gated startup."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/self-hosting/3.deploying.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
At minimum configure a database and a `SECRET`. Containers are ephemeral, so mount volumes for uploads and extensions (or use external storage) and persist the database.

Compose outline (replace placeholders):

```yaml
services:
  database:
    image: postgis/postgis:17-3.5
    volumes: [ "./data/database:/var/lib/postgresql/data" ]
  cache:
    image: redis:7
  directus:
    image: directus/directus:REPLACE_WITH_VERSION
    ports: [ "8055:8055" ]
    volumes: [ "./uploads:/directus/uploads", "./extensions:/directus/extensions" ]
    environment:
      SECRET: "REPLACE_WITH_YOUR_SECRET"
      DB_CLIENT: "pg"
      DB_HOST: "database"
      DB_PORT: "5432"
      DB_DATABASE: "directus"
      DB_USER: "directus"
      DB_PASSWORD: "REPLACE"
      CACHE_ENABLED: "true"
      CACHE_AUTO_PURGE: "true"
      CACHE_STORE: "redis"
      REDIS: "redis://cache:6379"
      ADMIN_EMAIL: "REPLACE_WITH_YOUR_EMAIL"
      ADMIN_PASSWORD: "REPLACE_WITH_YOUR_PASSWORD"
      PUBLIC_URL: "REPLACE_WITH_YOUR_URL"
```

Add health checks and `depends_on` with `condition: service_healthy` on database and cache (the docs example includes them).

First admin: either use the Studio onboarding screen, or script it with the `ADMIN_*` variables and a static token.

## Checked

2026-11-04: minimum configuration (database and SECRET), ephemeral containers and volumes, the Postgres, Redis and Directus compose example, health-gated depends_on and the first-admin options confirmed against the Directus Deploying page. Removed an unsupported Verify line.

Method: documentation only; no commands were run.
