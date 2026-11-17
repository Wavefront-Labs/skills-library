---
id: computing-software.cloud-infrastructure-engineering.docker.compose-override-yaml-automatic-loading
name: compose-override-yaml-automatic-loading
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-override, compose-override-yaml, override-files, compose-file, local-dev]
level: practitioner
status: verified
description: "Know when Compose auto-loads compose.override.yaml, the supported file names and precedence, why -f or COMPOSE_FILE disables it, and patterns for dev overrides vs prod."
sources: ["https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/", "https://docs.docker.com/compose/intro/compose-application-model/#the-compose-file", "https://docs.docker.com/compose/how-tos/environment-variables/envvars/#compose_file"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compose.override.yaml automatic loading

## The rule
With **no** `-f` flag and **no** `COMPOSE_FILE`, Compose looks in the working directory (then
parents) for:
1. `compose.yaml` (preferred) or `compose.yml`, else `docker-compose.yaml` / `docker-compose.yml`
2. plus, if present, the matching override: `compose.override.yaml` / `.yml` (or
   `docker-compose.override.*`)

and merges the override on top.

As soon as you pass `-f` (or set `COMPOSE_FILE`), only the listed files are used. The override
is **not** added automatically:
```bash
docker compose up                                        # compose.yaml + compose.override.yaml
docker compose -f compose.yaml up                        # base only (prod-like)
docker compose -f compose.yaml -f compose.override.yaml up   # explicit
```

## Recommended split
```yaml
# compose.yaml: production-shaped, committed
services:
  web:
    image: reg.example.com/web:${TAG:-latest}
    restart: unless-stopped
```
```yaml
# compose.override.yaml: developer conveniences, committed (or gitignored for personal tweaks)
services:
  web:
    build: { context: ., target: dev }
    volumes: [".:/app"]
    ports: ["3000:3000"]
    environment: { DEBUG: "1" }
```
On servers run with explicit files (`-f compose.yaml -f compose.prod.yaml`) so a stray
override file in the directory cannot change production.

## Debug what was merged
```bash
docker compose config                       # merged result
docker compose config --format json | jq '.services.web.ports'
docker compose ls --format json | jq -r '.[0].ConfigFiles'    # files actually used by a running project
```

## Gotchas
- Having both `compose.yaml` and `docker-compose.yml` in one directory: Compose uses
  `compose.yaml` (and its `compose.override.yaml`, not `docker-compose.override.yml`) and prints warnings about the extra files (checked); delete the legacy files.
- Merge rules: lists like `ports` and `volumes` are **appended/merged by key**, not replaced; use
  `!reset` / `!override` tags to replace.
- A personal `compose.override.yaml` that is gitignored still affects CI if CI runs plain
  `docker compose up` in a workspace containing it.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (Docker Desktop CLI plugin, `docker compose config` only, no daemon needed): `compose.yaml` plus `compose.override.yaml` merged without flags; `compose.yml` plus `compose.override.yml` also auto-loaded; with both naming styles present the `compose.*` pair was used and warnings were printed; running from a child directory found the parent's file; `-f compose.yaml` ignored the override; `config --format json` output. Not run: `docker compose ls` `ConfigFiles` (needs the daemon), a running project, Linux (same search rules documented, not run).
