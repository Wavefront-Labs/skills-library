---
id: computing-software.cloud-infrastructure-engineering.docker.compose-env-precedence-escaping-and-env-files
name: compose-env-precedence-escaping-and-env-files
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, dotenv, env-precedence, compose-variables, precedence-order, shell-vs-env-file, dollar-escaping, double-dollar, multiple-env-files, env-file-syntax]
level: practitioner
description: "Predict which value a Compose container gets: interpolation .env vs env_file vs environment precedence, escaping $ as $$, and multiple env files with their syntax rules."
sources: ["https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/", "https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/", "https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose env precedence, $ escaping and env files

## Two separate mechanisms
1. **Interpolation**: `${VAR}` in the YAML is replaced when Compose parses the file. Sources:
   shell environment > `--env-file` / project `.env`.
2. **Container environment**: what the process sees. Sources: `environment:`, `env_file:`,
   image `ENV`.

The project `.env` feeds interpolation only - its variables are **not** injected into
containers unless referenced (`environment: [DB_HOST]` or `env_file: .env`).

## Container env precedence (highest first)
1. `docker compose run -e KEY=val`
2. `environment:` attribute (values may themselves be interpolated from shell/.env)
3. `env_file:` attribute
4. Image `ENV`

```yaml
services:
  api:
    env_file: [defaults.env, { path: local.env, required: false }]   # later files win
    environment:
      LOG_LEVEL: ${LOG_LEVEL:-info}     # interpolated from shell/.env
      DB_PASSWORD:                      # no value: pass through from the shell running compose
```

## Interpolation precedence (highest first)
Shell environment > `--env-file` files (later wins). Passing `--env-file` replaces the project-directory `.env` instead of layering over it (checked); without it, the project `.env` is used.
```sh
LOG_LEVEL=debug docker compose up -d                      # beats .env
docker compose --env-file .env --env-file .env.prod config
```
Debug: `docker compose config --environment` (lists resolved interpolation variables; first in Compose v2.27.2 per the release notes),
`docker compose run --rm api env`.

## Escaping $
```yaml
    command: ["sh", "-c", "echo $$HOME && exec app"]   # $$ -> literal $, expanded by the shell in the container
    environment:
      PASSWORD_HASH: "$$2y$$10$$abc..."                # bcrypt hashes
      TEMPLATE: "$${user}"
```
A single `$` followed by a name is interpolated (unset -> empty + warning). Literal `$`
values in `.env` files: `.env` itself supports `'single quotes'` to suppress expansion.

## env file syntax
```sh
# comment
KEY=value
QUOTED="value with spaces and \n escapes"
LITERAL='no $expansion here'
EXPANDED=${OTHER:-default}       # interpolation inside .env/env_file works in Compose v2
export KEY2=value                # 'export ' prefix tolerated
```
- Lines are `KEY=VALUE`; no spaces around `=`.
- `docker run --env-file` (not Compose) does **no** quote processing: `KEY="x"` yields `"x"` with quotes.

## Verify
`docker compose config` shows interpolated YAML; `docker compose exec api printenv LOG_LEVEL`
matches the expected source.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon): shell beating `.env`; `--env-file` replacing `.env` and a second `--env-file` winning; `environment:` literal beating `env_file:`; `required: false` for a missing env file; `DB_PASSWORD:` pass-through (null when unset); `$$HOME` in `command` and `$$` in values; `${OTHER:-default}`, `${TAG}` and earlier-key references inside env files; single quotes literal, double quotes processing `\n` and `${}`; `export` prefix accepted; an unset `$NAME` giving a blank value plus the warning. Not run: `docker compose run -e` and `docker run --env-file` quote behaviour (need the daemon), image `ENV`, `printenv` in a container, Linux.
