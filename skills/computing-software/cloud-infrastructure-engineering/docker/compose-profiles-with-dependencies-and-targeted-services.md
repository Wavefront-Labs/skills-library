---
id: computing-software.cloud-infrastructure-engineering.docker.compose-profiles-with-dependencies-and-targeted-services
name: compose-profiles-with-dependencies-and-targeted-services
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-profiles, profile-dependencies, depends-on, compose-run, one-off-container]
level: practitioner
status: verified
description: "Combine Compose profiles with depends_on correctly: auto-enabling a targeted service's profile, dependencies across profiles, --profile '*', and errors from disabled dependencies."
sources: ["https://docs.docker.com/compose/how-tos/profiles/", "https://docs.docker.com/reference/compose-file/services/#profiles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiles with dependencies and targeted services

## Rules
1. Services **without** `profiles` are always enabled.
2. Services with `profiles` start only when a listed profile is active (`--profile x`,
   `COMPOSE_PROFILES=x,y`) or when the service is **explicitly targeted** on the command line.
3. Targeting a profiled service enables it (and its `depends_on` services that are always-on) without enabling the
   rest of that profile (checked with `config seed`, which listed `seed` and `db` only).
4. An always-enabled service must not `depends_on` a service whose profile is inactive:
   Compose errors (`service "x" depends on undefined service` or a disabled-service error).

## Example
```yaml
services:
  web:
    image: web:1.0
    depends_on: [db]
  db:
    image: postgres:17
  migrate:
    image: web:1.0
    command: ["./manage", "migrate"]
    profiles: [tools]
    depends_on:
      db: { condition: service_healthy }
  adminer:
    image: adminer
    profiles: [debug]
    depends_on: [db]
  mailhog:
    image: mailhog/mailhog
    profiles: [debug]
```
```bash
docker compose up -d                      # web, db
docker compose run --rm migrate           # targets migrate: runs it (and db) without --profile tools
docker compose up -d adminer              # adminer + db; mailhog (same profile) NOT started
docker compose --profile debug up -d      # web, db, adminer, mailhog
docker compose --profile '*' up -d        # every profile
COMPOSE_PROFILES=debug,tools docker compose up -d
```

## Patterns
- `tools` profile for one-offs (migrations, seeders, linters) run via `compose run`.
- `debug` profile for admin UIs and mail catchers.
- Never put core dependencies (database) behind a profile if non-profiled services depend on
  them.

## Inspect
```bash
docker compose config --profiles           # list defined profiles
docker compose --profile debug config --services
```

## Gotchas
- `docker compose down` only removes containers of **active** profiles; add `--profile '*'` (or
  the same profiles you started with) to clean everything.
- A `depends_on` from a profiled service to a service in a **different** profile did **not** work when targeting on Compose v2.39: `docker compose up a` and `config a` failed with `no such service: b` (service `b` in another inactive profile), and `--profile p1 up` failed with `service "a" depends on undefined service "b"`. Put both services in a common profile (a service may list several profiles) or enable both profiles.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config` and `--dry-run`, no daemon needed): an always-on service depending on a profiled one failing with `service "web" depends on undefined service "adminer": invalid compose project` and succeeding once `--profile debug` is set; default, `--profile debug`, `COMPOSE_PROFILES` and `'*'` service lists; `config --profiles`; targeting a profiled service (`config seed`, `config adminer`); the cross-profile dependency failures above, via both `config` and `--dry-run up`. Not run: `docker compose run --rm migrate` against containers, `service_healthy` conditions, `down` with profiles, Linux.
