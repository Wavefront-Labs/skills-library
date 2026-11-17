---
id: computing-software.cloud-infrastructure-engineering.docker.compose-service-build-command-and-ports
name: compose-service-build-command-and-ports
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-file, compose-build, build-context-compose, compose-command, compose-entrypoint, compose-ports, ports-long-syntax]
level: practitioner
description: "Write Compose service build sections (context, dockerfile, target, args, cache_from), override command/entrypoint correctly, and declare ports in long syntax with host_ip."
sources: ["https://docs.docker.com/reference/compose-file/build/", "https://docs.docker.com/reference/compose-file/services/#command", "https://docs.docker.com/reference/compose-file/services/#entrypoint", "https://docs.docker.com/reference/compose-file/services/#ports"]
status: verified
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compose service: build, command/entrypoint and ports

## build
```yaml
services:
  api:
    image: registry.example.com/api:${TAG:-dev}   # tag for the built image (and for push)
    build:
      context: ./services/api          # relative to the compose file's directory
      dockerfile: Dockerfile.prod      # relative to context
      target: runtime                  # multi-stage target
      args:
        GO_VERSION: "1.23"
        GIT_SHA: ${GIT_SHA}
      cache_from: ["type=registry,ref=registry.example.com/api:cache"]      # quote: an unquoted flow list splits at the comma
      cache_to: ["type=registry,ref=registry.example.com/api:cache,mode=max"]
      platforms: [linux/amd64, linux/arm64]
      secrets: [npm_token]
      ssh: [default]
      additional_contexts:
        shared: ../libs/shared
      labels:
        org.opencontainers.image.source: https://github.com/org/api
    pull_policy: build                 # always build, never pull this image
secrets:
  npm_token: { environment: NPM_TOKEN }
```
- `build: ./dir` short form = context only.
- `dockerfile_inline: |` embeds a Dockerfile.
- With both `image` and `build`, Compose builds and tags with `image`; `docker compose pull`
  tries to pull it (use `pull_policy: build` or `--ignore-buildable`).
- `docker compose build --no-cache --pull api`, `docker compose up --build` (all flags exist in `--help`; `pull --ignore-buildable` exists too).
- YAML trap (reproduced): `cache_from: [type=registry,ref=r/api:cache]` without quotes becomes two list items, `type=registry` and `ref=r/api:cache`; quoting keeps one item `type=registry,ref=r/api:cache`.

## command and entrypoint
```yaml
    entrypoint: ["/app/entrypoint.sh"]      # replaces image ENTRYPOINT, clears image CMD
    command: ["serve", "--port", "8080"]    # replaces image CMD
```
- Overriding `entrypoint` **resets the image CMD** - set `command` too if needed.
- String form `command: serve --port 8080` is split shell-like (not run through a shell);
  for shell features use `["sh", "-c", "exec serve --port $$PORT"]` (`$$` escapes Compose interpolation).
- To keep the image's ENTRYPOINT, omit the key; to bypass it, set an explicit exec array
  rather than relying on empty values.

## ports
```yaml
    ports:
      - "127.0.0.1:8080:8080"          # short form: always quote (YAML base-60 gotcha with xx:yy)
      - target: 9090
        published: "9090"
        host_ip: 127.0.0.1
        protocol: tcp
        app_protocol: http
        mode: host                      # Swarm: bypass routing mesh
        name: metrics
```
`expose: ["8080"]` documents ports to other services only; services on the same network reach
any listening port anyway.

## Verify
`docker compose config` shows the normalised build, command and ports;
`docker compose ps --format json | jq '.[].Publishers'` shows host bindings.

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config`, no daemon needed): normalised `build` (context, dockerfile, target, args, ssh, labels, additional_contexts, platforms, secrets), `pull_policy: build`, `dockerfile_inline`, short `build: ./dir`, `entrypoint` as an array, `command: serve --port 8080` split into `[serve, --port, 8080]` without a shell, `$$PORT` preserved in an exec array, port forms (short with host IP, long with `host_ip`, `app_protocol`, `mode: host`, `name`, a range `3000-3005:3000`, a bare container port; unquoted `22:22` stayed a string on this version, quote anyway), `expose`, an unset `${GIT_SHA}` giving a blank value plus a warning, the cache_from quoting bug. Not run: `docker compose build`, a build with `secrets`/`ssh`/`platforms`, `pull`, `ps --format json` publishers, Swarm `mode: host`, Linux.
