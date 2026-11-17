---
id: computing-software.cloud-infrastructure-engineering.docker.compose-profiles-and-project-names
name: compose-profiles-and-project-names
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-profiles, profiles, compose-profiles-flag, compose-profiles-env, compose-project-name, project-name]
level: practitioner
description: "Make optional services opt-in with profiles (--profile, COMPOSE_PROFILES) and control the project name (-p, COMPOSE_PROJECT_NAME, top-level name) to run isolated copies."
sources: ["https://docs.docker.com/compose/how-tos/profiles/", "https://docs.docker.com/compose/how-tos/project-name/", "https://docs.docker.com/reference/compose-file/version-and-name/"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose profiles and project names

## Profiles
```yaml
services:
  api:      { image: app/api }                    # no profiles -> always started
  db:       { image: postgres:16 }
  adminer:  { image: adminer, profiles: [debug] }
  seed:     { image: app/seed, profiles: [tools], depends_on: [db] }
  mailhog:  { image: mailhog/mailhog, profiles: [debug, mail] }
```
```sh
docker compose up -d                              # api, db
docker compose --profile debug up -d              # + adminer, mailhog
COMPOSE_PROFILES=debug,mail docker compose up -d
docker compose --profile "*" up -d                # all profiles
docker compose run --rm seed                      # naming a service activates its profile
docker compose config --profiles                  # list defined profiles
```
Rules:
- Services without `profiles` are always enabled.
- Explicitly targeting a service (`run seed`, `up seed`) enables it regardless of profile (checked with `config seed`: the output contained `seed` and its always-on dependency `db` only),
  but its **dependencies** must be enabled too (in a profile that's active, or no profile; a dependency in another inactive profile failed with `no such service`).
- `down` only acts on services in active profiles - use the same `--profile` flags (or `"*"`)
  when tearing down, or profile containers stay running.

## Project name
Precedence (highest first): `-p name` > `COMPOSE_PROJECT_NAME` > top-level `name:` in the
file > directory name of the (first) compose file.
```yaml
name: shop                       # top-level in compose.yaml
```
```sh
docker compose -p shop-pr-123 up -d          # isolated copy: own networks, volumes, containers
COMPOSE_PROJECT_NAME=shop-ci-$CI_JOB_ID docker compose up -d --wait
docker compose ls                            # running projects
docker compose -p shop-pr-123 down -v
```
- Names: lowercase letters, digits, `-`, `_`, must start with a letter or digit (checked: `Shop`, `shop name`, `shop.x`, `-shop` and `_shop` are rejected for `-p`; `shop_1-a` and `1shop` accepted). A directory name like `Shop Dir_X` is lowercased and stripped of spaces to `shopdir_x`; with several `-f` files the name comes from the first file's directory.
- The project name prefixes containers (`shop-api-1`), networks (`shop_default`) and volumes
  (`shop_data`); renaming the directory silently "loses" volumes - pin `name:`.
- Label `com.docker.compose.project` is how Compose finds its containers; filtering on it is
  handy (`docker ps --filter label=com.docker.compose.project=shop`).

## Verify
`docker compose --profile debug config --services` lists the expected services;
`docker compose ls` shows the project under the intended name.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config` and `--dry-run`, no daemon needed): profile listing (`config --profiles`), default services, `--profile debug`, `COMPOSE_PROFILES=debug,mail`, `--profile '*'` (adds the `tools` profile too); project-name precedence (`-p` over `COMPOSE_PROJECT_NAME` over top-level `name:` over directory); the sanitising and rejection rules above; default network and volume prefixes. Not run: `docker compose up/down/run` against containers (the daemon is not running), `docker compose ls`, label filtering, the `down` behaviour with inactive profiles, Linux.
