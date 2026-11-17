---
id: computing-software.cloud-infrastructure-engineering.docker.compose-extends-and-extension-fields
name: compose-extends-and-extension-fields
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, extends, extends-file, extends-service, x-fields, extension-fields, yaml-anchors, compose-fragments]
level: practitioner
description: "Remove duplication in Compose files with extends (same file or another file), x- extension fields, YAML anchors and merge keys, and know what extends does not copy."
sources: ["https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/", "https://docs.docker.com/reference/compose-file/extension/", "https://docs.docker.com/reference/compose-file/fragments/"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose extends and extension fields

## x- extension fields + YAML anchors
```yaml
x-app-defaults: &app
  image: registry.example.com/app:${TAG:-dev}
  restart: unless-stopped
  env_file: [common.env]
  logging: &logging
    driver: json-file
    options: { max-size: "10m", max-file: "3" }

x-healthcheck: &hc
  interval: 10s
  timeout: 3s
  retries: 5

services:
  api:
    <<: *app
    command: ["serve"]
    healthcheck: { <<: *hc, test: ["CMD", "/app/healthcheck", "api"] }
  worker:
    <<: *app
    command: ["work"]
    environment: { QUEUES: "default,mail" }
  nginx:
    image: nginx:1.27
    logging: *logging
```
- Top-level keys starting with `x-` are ignored by Compose (also allowed inside services,
  networks, volumes) - a place to park anchors. They are not stripped from `docker compose config` output (checked: top-level `x-*` blocks and a service-level `x-note` were printed).
- `<<:` merge is **shallow**: a service that sets `environment:` replaces the anchor's
  `environment` entirely; merge maps one level down explicitly (`environment: { <<: *env, X: 1 }`).
- Anchors work only within one file.

## extends
```yaml
services:
  web:
    extends:
      file: common-services.yaml     # omit file to extend a service in the same file
      service: webapp
    environment:
      - DEBUG=1
```
- Works across files (unlike anchors) and merges using Compose merge rules (maps merge,
  ports append, command replaces) instead of YAML's shallow merge.
- Relative paths in the extended service (build context, bind mounts, env_file) resolve
  relative to **its** file.
- `depends_on` targets must exist in the final file (checked: `service "web" depends on undefined service "dbx"` when the extended file's `dbx` was not also defined in the extending file). On Compose v2.39 `links` and `volumes_from` **were** copied into the extending service (older docs say they are not inherited; check your version). Extending a service that itself uses `extends` is fine; cycles error with `Circular reference`.

## Which to use
| Need | Use |
|---|---|
| Same defaults for several services in one file | x- + anchors |
| Share a base service definition across files/projects | extends |
| Pull whole dependency stacks in | include |
| Environment-specific changes | override files |

## Verify
`docker compose config` shows the expanded services - check that maps you expected merged
(environment, labels) actually did.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon): YAML anchors with `<<` (the worker's own `environment` replaced the anchor's: `FROM_ANCHOR` was lost, `env_file` values stayed); anchors not usable across `-f` files (`yaml: unknown anchor 'a' referenced`); `extends` from another file and in the same file; merge rules in `extends` (ports appended, `command` replaced, environment list merged with the map: A=1, B=2, DEBUG=1); relative paths (build context, bind source, env_file) resolving against the extended file's directory (`sub/`); chained extends; the circular-reference error; the `depends_on` error; `links` and `volumes_from` inheritance. Not run: Compose versions older than 2.39, `docker compose up`, Linux.
