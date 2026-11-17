---
id: computing-software.software-engineering.deno.docker-compose-and-workspaces
name: docker-compose-and-workspaces
category: computing-software
field: software-engineering
product: deno
tags: [docker, docker-compose, workspaces, build-context, dockerignore, postgres]
level: advanced
status: docs-checked
description: "Run a Deno app with Docker Compose (watch mode, Postgres with health checks) and containerize workspaces fully or with a minimal build context."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/reference/docker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Compose with a database; `depends_on` waits for the health check, and permissions are scoped to the service:

```yaml
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgres://deno:${POSTGRES_PASSWORD}@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    command: ["deno", "run", "--allow-net=db:5432", "--allow-env=DATABASE_URL", "main.ts"]
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U deno"]
```

Put secrets in a `.env` beside the compose file (loaded automatically; do not commit). Dev variant: mount `.:/app` and use `deno run --watch --allow-net main.ts`.

Workspace, full: copy root `deno.json` plus every member, then `WORKDIR /app/project-a`.

Workspace, minimal: build from a temporary context holding only the root `deno.json`, the target member and members it imports, with a deny-all `.dockerignore`:

```text
*
!deno.json
!project-a/**
!project-b/**
```

A script copies the needed folders into `tmp-build-context`, then `docker build -t project-a -f Dockerfile tmp-build-context`, then remove the folder. Keep the same directory structure as development, always include the root `deno.json`, and update `.dockerignore` when dependencies change.

## Checked

2026-11-04. Confirmed against docs runtime/reference/docker.md (Deno and Docker): Compose example with Postgres and health check, .env loading, dev watch variant, full and minimal workspace containerization, deny-all .dockerignore, build-context steps and best practices.

Method: documentation only; no commands were run.
