---
id: computing-software.cloud-infrastructure-engineering.docker.compose-env-interpolation-and-precedence
name: compose-env-interpolation-and-precedence
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, env-interpolation, dotenv, env-precedence, compose-variables, env-file, environment, default-values, required-variables, compose-config, env-file-flag]
level: practitioner
status: verified
description: "How Compose resolves ${VAR}: the .env file vs env_file: vs environment: distinction, the precedence order, ${VAR:-default} and ${VAR:?err} syntax, escaping $$, and debugging with compose config."
sources: ["https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/", "https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/", "https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/", "https://docs.docker.com/reference/compose-file/interpolation/", "https://docs.docker.com/reference/compose-file/services/#env_file"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose .env interpolation and variable precedence

**Goal:** know exactly which value a `${VAR}` in the Compose file and an env var inside a
container will have, and make missing config fail at `up` time rather than at runtime.

## Two different jobs, three different mechanisms
1. **Interpolation** — substituting `${VAR}` *in the Compose file itself* (image tags,
   ports, paths). Sources: your shell environment, then the project `.env` file (or
   `--env-file`). **`env_file:` and `environment:` do NOT feed interpolation.**
2. **Container environment** — what the process sees. Sources: `environment:`, `env_file:`,
   and the image's `ENV`. The `.env` file does *not* go into containers unless you also
   write `env_file: .env`.

```yaml
services:
  app:
    image: app:${TAG:-latest}          # interpolated from shell or .env
    env_file: [.env.app]               # lines go into the container, no interpolation of the file
    environment:
      DB_HOST: db                      # into the container
      API_KEY: ${API_KEY:?API_KEY must be set}   # interpolated, then into the container
      HOME_SHELL: ${HOME}              # value from *your* shell, passed in
      PASS_THROUGH:                    # no value: forwards from the shell if set, else unset
```

## Precedence (highest first) for a variable inside the container
1. `docker compose run -e VAR=x`
2. `environment:` with a literal value in the Compose file
3. `environment:` with `${VAR}` — resolved via the interpolation order below
4. `env_file:` entries (later files override earlier)
5. Image `ENV`
Interpolation sources, highest first: `docker compose --env-file`/shell environment of the
process running compose, then `.env` in the project directory. Shell beats `.env`, which
is why `export TAG=dev` silently overrides what a teammate wrote in `.env`.

## `.env` file rules
- Looked up in the **project directory** (where the Compose file is, or `--project-directory`),
  not the cwd. `--env-file path` replaces it (can be repeated; later wins).
- Syntax: `KEY=value`, `#` comments, blank lines. Unquoted values keep inner spaces and are trimmed at the ends, but a space followed by `#` starts an inline comment (`A=unquoted with spaces  # x` gave `unquoted with spaces`; `F=a#b` kept the `#`); single quotes are literal; double quotes process `\n` escapes and
  `${OTHER}` references to earlier keys in the same file. `export KEY=v` is accepted.
- `env_file:` files are interpolated too on current Compose (v2.39: `E_REF=${TAG}` resolved from the project `.env`, `K=${SHELLV}-x` from the shell, `L=${K}` from an earlier key in the same file; single-quoted values stay literal). Which release introduced this was not verified. The long form `env_file: [{path: .env.opt, required: false}]` makes a missing file optional (checked).
- `.env` is committed by mistake constantly: keep `.env.example` in git, `.env` in
  `.gitignore` and `.dockerignore`.

## Interpolation syntax
| Form | Meaning |
|---|---|
| `${VAR}` / `$VAR` | value, empty string if unset (with a warning) |
| `${VAR:-def}` | `def` if unset **or empty** |
| `${VAR-def}` | `def` only if unset |
| `${VAR:?msg}` | error at `up`/`config` if unset or empty |
| `${VAR?msg}` | error only if unset |
| `${VAR:+alt}` | `alt` if set and non-empty (feature toggles) |
| `$$` | literal `$` (needed for `command:` strings with shell vars, cron, Prometheus) |
Nested defaults work: `${A:-${B:-fallback}}`. No arithmetic, no command substitution.

Literal `$` trap: a `command: sh -c "echo $HOME"` is interpolated by Compose **before** the
shell runs it; write `$$HOME` for the container's shell to see `$HOME`. Same for
healthcheck commands and Traefik label rules.

## Profiles / multiple environments
`COMPOSE_PROFILES`, `COMPOSE_PROJECT_NAME`, `COMPOSE_FILE` (colon- or semicolon-separated
on Windows) may all be set in `.env`, which is the usual way to pin a project name and
override-file stack per checkout. `COMPOSE_PATH_SEPARATOR` changes the separator.

## Debug
```bash
docker compose config                  # fully interpolated file; secrets included, don't paste it
docker compose config --environment    # Compose v2.27.2+: the interpolation env it used (release notes)
docker compose config --variables      # lists every ${VAR} with default / required flag
docker compose run --rm app env | sort # what the container actually gets
```
Warnings like `The "FOO" variable is not set. Defaulting to a blank string.` are printed
to stderr on every command — treat them as errors in CI by using `:?`.

## Verify
`API_KEY= docker compose config` should fail with your `:?` message; with it set,
`docker compose config | grep image:` shows the resolved tag, and `docker compose run --rm
app sh -c 'echo $API_KEY'` prints the value (note the single quotes: the shell, not Compose,
expands it).

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (Docker Desktop CLI plugin, `docker compose config` only, no daemon needed): interpolation from `.env` and shell (shell wins), `--env-file` (replaces `.env`; a second `--env-file` wins), `.env` taken from the project directory (the compose file's directory) rather than the cwd and from `--project-directory`; every row of the syntax table (`:-`, `-`, `:?`, `?`, `:+`, `+`, `$$`, nested defaults; `${VAR?msg}` does not fire for a set-but-empty variable; `:?` fires for empty) and the unset-variable warning text (`The "X" variable is not set. Defaulting to a blank string.`); `command: sh -c "echo $HOME"` interpolated by Compose and `$$HOME` preserved; `$(date)` and `$((1+1))` in `command` make `config` fail (`invalid command line string`); `environment:` beating `env_file:`; `PASS_THROUGH:` with no value becomes null when unset and the shell value when set; `config --variables` and `--environment`; `.env` quoting rules (double quotes process `\n` and `${}`, single quotes literal, `export` accepted). Fetched: GitHub release notes (`--environment` first listed in v2.27.2). Not run: `docker compose run -e` (needs the daemon), image `ENV` precedence, `COMPOSE_PROFILES` from `.env`, Linux.
