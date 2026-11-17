---
id: computing-software.cloud-infrastructure-engineering.docker.docker-compose-for-local-dev
name: docker-compose-for-local-dev
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-compose, compose-v2, compose-yaml, compose-spec, local-development, dev-environment, depends-on, service-healthy, healthcheck, bind-mounts, named-volumes, compose-watch, hot-reload, profiles, override-file, compose-override, env-file, interpolation, include, extends, init-scripts, seed-data]
level: practitioner
status: docs-checked
description: "One-command local dev stack with Docker Compose: healthcheck-gated depends_on, compose watch hot reload, profiles, override files, env interpolation, seeding and file-ownership gotchas."
sources: ["https://docs.docker.com/reference/compose-file/", "https://docs.docker.com/compose/how-tos/file-watch/", "https://docs.docker.com/compose/how-tos/profiles/", "https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/", "https://docs.docker.com/compose/how-tos/startup-order/", "https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/", "https://github.com/docker-library/docs/tree/master/postgres"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker Compose for local development: `docker compose up` and you are working

**Goal:** a new developer clones the repo, runs one command, and has the app plus its
databases and queues running with live code reload, seeded data and no manual steps.
Compose here is a **dev tool**; production orchestration belongs in Kubernetes (see
`computing-software.cloud-infrastructure-engineering.kubernetes.deployments-services-and-probes`).
Network internals (DNS, published ports) are in
`computing-software.cloud-infrastructure-engineering.docker.container-networking`.

## 1. The base file
```yaml
# compose.yaml  (no top-level "version:": it is obsolete and only produces a warning)
name: shop
services:
  api:
    build: {context: ., target: dev}          # dev stage of the multi-stage Dockerfile
    ports: ["127.0.0.1:8080:8080"]            # bind to localhost, not all interfaces
    env_file: [.env]
    environment:
      DATABASE_URL: postgres://app:app@db:5432/app
    depends_on:
      db: {condition: service_healthy}
      migrate: {condition: service_completed_successfully}
    develop:
      watch:
        - {action: sync, path: ./src, target: /app/src}
        - {action: rebuild, path: package-lock.json}
  migrate:
    build: {context: ., target: dev}
    command: ["npm", "run", "migrate"]
    depends_on: {db: {condition: service_healthy}}
  db:
    image: postgres
    environment: {POSTGRES_USER: app, POSTGRES_PASSWORD: app, POSTGRES_DB: app}
    volumes:
      - dbdata:/var/lib/postgresql/data
      - ./dev/seed:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 2s
      timeout: 3s
      retries: 30
  cache:
    image: redis
    profiles: [extras]
volumes:
  dbdata: {}
```

## 2. Startup order that actually works
- `depends_on` with a plain list controls creation order only; use `condition:
  service_healthy` (needs a `healthcheck` on the dependency) to wait until it is healthy.
- One-shot jobs (migrations, seeding) use `condition: service_completed_successfully`.
- Compose conditions are `service_started`, `service_healthy` and
  `service_completed_successfully`. Applications should still retry connections on boot.

## 3. Live reload
- **`docker compose watch`** (or `up --watch`): `sync` copies changed files into the
  container (pair with the framework's own reloader), `rebuild` rebuilds the image on
  dependency manifest changes, `sync+restart` handles config files. Watch works for
  services built from local source with `build:`.
- **Bind mounts** (`./src:/app/src`) are the older approach. Watch rules can ignore files
  and directories within the tree, which a bind mount cannot.
- Do not let a bind mount shadow `node_modules` or a venv built in the image; if you mount
  the repo root, add an anonymous volume such as `/app/node_modules` for that path.

## 4. Layering config
- `compose.override.yaml` is loaded automatically next to `compose.yaml` when you do not
  pass `-f`; put dev-only tweaks there and keep `compose.yaml` the shared baseline.
  Explicit files: `docker compose -f compose.yaml -f compose.ci.yaml up`.
- Check merge results with `docker compose config`; the merge guide documents how
  attributes combine, and that relative paths resolve against the first (base) file.
- `include:` loads other Compose files (local paths, Git or OCI references); `extends`
  reuses a service definition.
- **Profiles** keep optional services off by default: `docker compose --profile extras up`
  (or `COMPOSE_PROFILES=extras`). A service with profiles runs without enabling the profile
  when you target it explicitly.
- Interpolation: `${PORT:-8080}` defaults, `${API_KEY:?message}` fails with the message when
  `API_KEY` is unset or empty. The project `.env` feeds interpolation of the Compose file;
  `env_file:` feeds the container, so they are separate mechanisms. Commit a
  `.env.example` and git-ignore `.env`.

## 5. Daily commands
```bash
docker compose up -d --build && docker compose logs -f api
docker compose ps                        # status per service
docker compose exec db psql -U app app
docker compose run --rm api npm test     # one-off container with the service's config
docker compose config                    # resolved, merged model: debug here first
docker compose down                      # keeps named volumes;  down -v removes them
```

## Gotchas
- Files created inside a container on a Linux bind mount are owned by the container's user;
  run the dev stage with a `user:` that matches yours.
- The official postgres image runs `/docker-entrypoint-initdb.d` scripts only when its data
  directory is empty; to re-seed, remove the data volume (`down -v`).
- `ports: ["5432:5432"]` collides with a Postgres already using that host port; pick other
  host ports.
- Use the `docker compose` plugin (Compose V2 syntax).
- Container names default to `<project>-<service>-<n>`; the project name comes from `-p`,
  `COMPOSE_PROJECT_NAME`, or `name:`, so scripts that hard-code names break when it changes.

## Verify
- [ ] Fresh clone, `docker compose up`: the app answers with seeded data, no manual step.
- [ ] Editing a source file is reflected within seconds without rebuilding.
- [ ] `docker compose down -v && docker compose up` recreates a clean state reproducibly.
- [ ] `docker compose config` resolves with no missing-variable warnings from `.env.example`.
- [ ] No service publishes ports on all interfaces unless deliberately shared on the LAN.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main), Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose file reference, how-tos and CLI reference: obsolete `version`
warning, `depends_on` conditions, `develop.watch` actions and scope, `compose.override.yaml`
auto-loading, base-file path resolution in merges, `include` remote sources, profiles
behaviour and `--profile`/`COMPOSE_PROFILES`, interpolation syntax including `:?`,
`.env` versus `env_file`, `down -v`, project-name precedence, and `ports` host-IP behaviour.
Confirmed in the postgres Docker Official Image docs (docker-library/docs): scripts under
`/docker-entrypoint-initdb.d` only run when the data directory is empty. Removed: macOS
file-sharing performance claims, the Compose V1 end-of-life remark, shell `UID` export
advice, the mailpit image, Testcontainers advice and the `postgres:16` tag.
