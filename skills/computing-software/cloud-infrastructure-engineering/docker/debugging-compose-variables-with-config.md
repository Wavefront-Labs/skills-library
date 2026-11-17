---
id: computing-software.cloud-infrastructure-engineering.docker.debugging-compose-variables-with-config
name: debugging-compose-variables-with-config
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-variables, compose-config-environment, compose-config-validate, env-interpolation, troubleshooting]
level: practitioner
status: docs-checked
description: "Debug resolved Compose values: config --environment, --variables, --no-interpolate, --format json, --resolve-image-digests, --hash, and diffing models between environments."
sources: ["https://docs.docker.com/reference/cli/docker/compose/config/", "https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/", "https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/", "https://github.com/docker/compose/blob/main/pkg/api/labels.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging Compose variables with compose config

`docker compose config` renders the data model that will be applied to the engine: it merges
the Compose files set by `-f`, resolves variables, and expands short notation into the
canonical format.

## Flags that matter
```bash
docker compose config                              # merged + interpolated YAML
docker compose config --environment                # environment used for interpolation
docker compose config --variables                  # model variables and their default values
docker compose config --no-interpolate             # see raw ${VAR} expressions
docker compose config --format json                # yaml (default) or json
docker compose config --services                   # service names (also --volumes, --networks, --profiles, --models)
docker compose config --images                     # image names, one per line
docker compose config --resolve-image-digests      # pin image tags to digests
docker compose config --lock-image-digests         # produce an override file with image digests
docker compose config --hash '*'                   # config hash per service, one per line
docker compose config -q                           # validate only, exit code
docker compose config -o resolved.yaml             # write to a file instead of stdout
```
Related: `--no-env-resolution` (do not resolve service env files), `--no-path-resolution`,
`--no-normalize`, `--no-consistency`.

## Typical investigations
**Wrong tag deployed**
```bash
docker compose --env-file .env.prod config --images
env | grep TAG             # a TAG exported in the shell wins over the .env file
```

**Where did this value come from?**
Interpolation precedence, highest first: variables from your shell environment, then a file
set with `--env-file`, then (when `--env-file` is not set) the `.env` file in the project
directory (`--project-directory`, else the directory of the first `-f` file, else the current
directory). For a container's environment, the order is: `docker compose run -e`, then values
set with `environment` or `env_file` that are interpolated from the shell or an env file,
then plain `environment` values, then `env_file` contents, then the image's `ENV`. Compare
`config --environment` with the `config` output for the service.

**Diff two environments**
```bash
diff <(docker compose --env-file .env.staging config) <(docker compose --env-file .env.prod config)
```

**Why is a service recreated on every `up`?**
```bash
docker compose config --hash web
docker inspect -f '{{index .Config.Labels "com.docker.compose.config-hash"}}' shop-web-1
```
Compose records the config hash in the `com.docker.compose.config-hash` container label; a
value that changes every run changes the hash.

## Commit a resolved model for deploys
```bash
docker compose --env-file .env.prod config --resolve-image-digests -o deploy/compose.resolved.yaml
docker compose -f deploy/compose.resolved.yaml up -d
```

## Gotchas
- `config` output includes values from env files in plain text; do not paste it into tickets.
- Some flags exist only in newer Compose releases; check `docker compose config --help`.

## Checked
Date 2026-10-23. Documentation release: Compose v5.6.1 CLI reference and Docker docs
(docker/docs main). Method: documentation only; no commands were run.
Confirmed the full `config` option list and descriptions (CLI reference), interpolation and
container-environment precedence orders (interpolation how-to and environment-variable
precedence page), the project-directory rule for `.env`, and the
`com.docker.compose.config-hash` label name (Compose source `pkg/api/labels.go`). Removed:
JSON-processing pipelines, the "writes a lockable model" description of
`--resolve-image-digests`. The secrecy gotcha follows from `--no-env-resolution` ("don't
resolve service env files") being the opt-out.
