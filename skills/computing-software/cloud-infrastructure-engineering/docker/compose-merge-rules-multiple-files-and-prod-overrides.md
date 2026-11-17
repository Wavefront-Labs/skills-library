---
id: computing-software.cloud-infrastructure-engineering.docker.compose-merge-rules-multiple-files-and-prod-overrides
name: compose-merge-rules-multiple-files-and-prod-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, override-files, compose-override, compose-merge-rules, reset-tag, override-tag, compose-file-env, multiple-compose-files, compose-prod-override, override-prod]
level: advanced
description: "Layer compose.yaml with override and environment files via -f and COMPOSE_FILE, predict merge results per attribute, and remove or replace values with !reset and !override."
sources: ["https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/", "https://docs.docker.com/reference/compose-file/merge/", "https://docs.docker.com/compose/how-tos/production/"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose merge rules, multiple files and production overrides

## Loading files
- No `-f`: `compose.yaml` (or `docker-compose.yml`) **plus** `compose.override.yaml` if present.
- Explicit: `docker compose -f compose.yaml -f compose.prod.yaml up -d` - the default
  override is **not** loaded then.
- `COMPOSE_FILE=compose.yaml:compose.prod.yaml` (`;` on Windows; or `COMPOSE_PATH_SEPARATOR`)
  in `.env` or the shell.
- Paths in later files are relative to the **first** file's directory (checked with files in `a/` and `b/`: bind sources and build contexts from `b/compose.yaml` resolved under `a/`).

## Merge rules
| Attribute kind | Result |
|---|---|
| scalars (`image`, `command`, `restart`) | later file wins |
| maps (`environment`, `labels`, `deploy.resources`) | merged by key; later wins per key |
| `ports`, `expose`, `dns`, `external_links` | **concatenated** (only identical entries are de-duplicated: `8080:8080` plus `8080:9999` gave two entries that both publish host port 8080) - overrides can't remove a port |
| `volumes`, `devices` | merged by **container target path** |
| `command`, `entrypoint`, `healthcheck.test` | replaced entirely |
| `depends_on` | merged |

## Removing and replacing
```yaml
# compose.prod.yaml
services:
  api:
    ports: !reset []                     # drop all dev ports
    volumes: !reset []                   # no source bind mounts in prod
    environment:
      DEBUG: !reset null                 # remove one key
    build: !reset null                   # use image only
    command: !override ["serve", "--workers", "4"]
    labels: !override                    # replace the whole map instead of merging
      com.example.tier: prod
```
`!reset` removes the value; `!override` replaces instead of merging. The Compose docs require 2.24.4 or later for `!override`. The value written after `!reset` is ignored: `ports: !reset ["127.0.0.1:8080:8080"]` produced a service with **no** ports (checked), so use `!override` to replace and `!reset null` / `!reset []` to clear.

## A production override checklist
```yaml
services:
  api:
    image: registry.example.com/api:${TAG:?TAG required}
    restart: unless-stopped
    ports: !override ["127.0.0.1:8080:8080"]   # !reset would drop ports entirely
    environment: { APP_ENV: production }
    deploy:
      resources: { limits: { cpus: "2", memory: 1g } }
    logging:
      driver: json-file
      options: { max-size: "20m", max-file: "5" }
    volumes: !reset []
```
Keep dev conveniences (bind mounts, debug ports, `build:`) in `compose.override.yaml`, which
prod never loads because it uses explicit `-f`.

## Verify
`docker compose -f compose.yaml -f compose.prod.yaml config` shows no dev ports/binds;
diff it against the dev config to review exactly what changes.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (Docker Desktop CLI plugin, `docker compose config` only, no daemon needed): default loading (base plus `compose.override.yaml`), `-f compose.yaml` alone (override ignored), `-f` with a prod file, `COMPOSE_FILE` with `;` (works; `:` fails with a CreateFile error until `COMPOSE_PATH_SEPARATOR=':'` is set), the merge table (scalars later wins; `environment` and `labels` merged by key; `ports`, `expose`, `dns` concatenated; `volumes` merged by target path, so `./other:/app` replaced `./src:/app`; `command` and `healthcheck.test` replaced while `healthcheck.interval` survived; `depends_on` list merged with map form; `deploy.resources` merged), `!reset []` for volumes, `!reset null` for one environment key and for `build`, `!override` for `command` and `labels`, `${TAG:?msg}` failing both when unset and when empty. Fetched: the Compose merge docs (`!reset` ignores the value; `!override` needs 2.24.4+). Not run: `docker compose up`, the logging and `deploy` runtime effects, Linux (`COMPOSE_FILE` uses `:` there; paths in output are Windows paths here).
