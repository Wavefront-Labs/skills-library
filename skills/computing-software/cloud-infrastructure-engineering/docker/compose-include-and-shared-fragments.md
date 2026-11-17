---
id: computing-software.cloud-infrastructure-engineering.docker.compose-include-and-shared-fragments
name: compose-include-and-shared-fragments
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-include, include-top-level, include-path, include-conflicts, project-directory, compose-library, shared-compose, compose-fragments]
level: advanced
description: "Compose multi-team stacks with the top-level include element (path, project_directory, env_file, remote sources), resolve include conflicts, and share fragments across repos."
sources: ["https://docs.docker.com/compose/how-tos/multiple-compose-files/include/", "https://docs.docker.com/reference/compose-file/include/"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose include and shared fragments

## include (Compose 2.20+)
```yaml
# compose.yaml of the app team
include:
  - ../platform/postgres/compose.yaml                 # short form
  - path: ../platform/observability/compose.yaml
    project_directory: ../platform/observability       # resolve its relative paths there
    env_file: ../platform/observability/.env
services:
  api:
    build: .
    depends_on: [postgres]                              # service defined in the included file
```
- Each included file is loaded as its own Compose application **with its own relative path
  base and .env**, then its resources are added to this project. Interpolation variables are not isolated, though: on Compose v2.39 the parent's shell environment and the parent's project `.env` also applied inside the included file and **won** over the include's own `.env` and over the `env_file:` given on the include (checked, see below). That's the difference from
  `-f` merging, where all paths are relative to the first file and attributes merge.
- `path` may be a list (the included app's own override files).
- Remote includes: `include: [oci://registry.example.com/compose/postgres:16]` or a Git URL
  (`https://github.com/org/stacks.git#v1.2:postgres/compose.yaml`) - pin tags.

## Conflicts
Include does **not** merge: if the included file and the including file both define service
`postgres` (or a network/volume of the same name), Compose errors
(`services.postgres conflicts with imported resource`; the docs describe a warning, v2.39 failed `config` with this error). Options:
- rename in one place;
- customise via the including side using an override file loaded with `-f` after
  resolution, or a `compose.override.yaml` next to the include target listed in `path`;
- keep included fragments narrowly scoped (one dependency each).

## Shared fragment library across repos
```
platform-compose/                  # versioned repo or OCI artifacts
  postgres/compose.yaml            # service + volume + healthcheck, env via ${PG_*:-defaults}
  redis/compose.yaml
  observability/compose.yaml
```
- Parameterise with interpolation defaults (`image: postgres:${PG_VERSION:-16}`) so consumers
  set `.env` values, not edit YAML.
- Publish fragments as OCI artifacts with `docker compose publish` (newer Compose releases;
  run in the fragment's directory with the target repo:tag) and include via `oci://`.
- Version fragments (tags) and changelog breaking changes; consumers pin.

## Verify
`docker compose config` shows included services with paths resolved to their own directories;
`docker compose config --services` lists the union.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon): two includes (short form and long form with `project_directory` and `env_file`) producing one project with their relative paths resolved in their own directories (`platform/postgres/pgdata`, `platform/obs/conf`) and `config --services` listing the union; interpolation precedence inside includes: parent shell > parent `.env` > include `env_file` > include's own `.env` (parent `.env` `PG_VERSION=15` reached the include; an `OBS_TAG` in both the parent `.env` and the include's `env_file` resolved to the parent's); an include with its own `.env` and no parent value used it; `env_file` on the include replaced the include's own `.env`; a duplicate service name erroring with `services.postgres conflicts with imported resource`; `path:` as a list merging the second file onto the first; a profiled included service hidden until the profile is enabled. Fetched: the Compose `include` docs (`Requires: Docker Compose 2.20.0 and later`). Not run: remote `oci://` and Git includes, `docker compose publish`, Linux.
