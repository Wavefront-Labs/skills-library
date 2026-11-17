---
id: computing-software.cloud-infrastructure-engineering.docker.compose-include-with-env-file-and-project-directory
name: compose-include-with-env-file-and-project-directory
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-include, include-env-file, project-directory, include-path, compose-file, monorepo]
level: advanced
status: verified
description: "Use include long syntax: path lists with overrides, per-include env_file and project_directory, how relative paths resolve, and conflicts between included resources."
sources: ["https://docs.docker.com/reference/compose-file/include/", "https://docs.docker.com/compose/how-tos/multiple-compose-files/include/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# include with env_file and project_directory

`include` pulls another Compose application into this one, each with its own relative-path
and variable context. That is the difference from `-f` merging, where all files share the
first file's directory.

## Long syntax
```yaml
include:
  - path:
      - ../platform/postgres/compose.yaml
      - ./overrides/postgres.override.yaml      # merged onto the included file only
    project_directory: ../platform/postgres     # base for relative paths and the default .env
    env_file:
      - ../platform/postgres/.env
      - ./env/postgres.local.env                # later file wins
  - ../platform/redis/compose.yaml               # short form
services:
  api:
    build: .
    depends_on: [postgres, redis]
```

## Resolution rules
- Relative paths inside an included file (build contexts, bind mounts, `env_file`) resolve
  against that file's directory, or `project_directory` when set.
- Variables for interpolation inside the included file come from its `env_file` list (default:
  `.env` in its project directory; an explicit `env_file` replaces that default), plus the shell environment **and the parent's `.env`, which take priority over both** (checked on v2.39: parent `.env` `C=appdotenv` beat the include's `env_file` `C=incenv`, while `B`, set only in the include's `env_file`, came through).
- The included model is merged into the parent: services, networks, volumes from it become
  part of one project (same project name, same default network).

## Conflicts
If an included file defines a resource (service, volume, network) with the same name as the
parent or another include, Compose errors rather than merging. Fix by renaming, or by moving
shared overrides into the `path` list of that include.

## Patterns
- Platform team publishes `postgres/compose.yaml`; app teams include it and supply their own
  env file for credentials.
- Monorepo: each service directory owns its compose.yaml; the root compose.yaml only includes
  them.

## Verify
```bash
docker compose config --services
docker compose config | yq '.services.postgres.volumes'   # absolute paths show which base was used
```

## Gotchas
- `include` needs a Compose v2 release that supports it (2.20+); old binaries fail on the key.
- Profiles in included files still apply; included services may stay disabled.
- The parent's `.env` and shell variables do reach the included file (and override its own env files), so a variable name used in both applications collides; namespace shared variables (`PG_VERSION`, not `VERSION`).

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon): long and short include forms, `path` as a list with a second file merged onto the first, `env_file` list with the later file winning, `project_directory` resolving relative paths of the included file, an explicit `env_file` replacing the include's own `.env`, parent `.env` and shell precedence over include env files, the same-name conflict error, and profiled services staying hidden. Fetched: Compose `include` docs (2.20.0+). `project_directory` pointing to a different directory moved both the relative bind source and the default `.env` lookup there. Not run: Linux.
