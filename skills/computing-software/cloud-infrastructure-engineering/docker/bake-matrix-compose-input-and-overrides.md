---
id: computing-software.cloud-infrastructure-engineering.docker.bake-matrix-compose-input-and-overrides
name: bake-matrix-compose-input-and-overrides
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bake, buildx-bake, bake-matrix, bake-compose, bake-compose-file, bake-set, bake-print, x-bake]
level: advanced
description: "Fan out Bake builds with matrix targets, reuse compose.yaml as Bake input with x-bake, and override or debug any attribute via --set and --print."
sources: ["https://docs.docker.com/build/bake/matrices/", "https://docs.docker.com/build/bake/compose-file/", "https://docs.docker.com/build/bake/overrides/", "https://docs.docker.com/reference/cli/docker/buildx/bake/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bake matrix targets, Compose input and overrides

## Matrix targets
```hcl
target "app" {
  name     = "app-${replace(ver, ".", "-")}-${variant}"
  matrix   = { ver = ["3.11", "3.12"], variant = ["slim", "alpine"] }
  args     = { PY_VERSION = ver, VARIANT = variant }
  tags     = ["registry.example.com/app:${ver}-${variant}"]
}
```
- Every generated target must have a unique name; use `name` to say how names resolve. The
  dots in the version values are replaced here to keep each generated name distinct and plain.
- `docker buildx bake app` builds all 4 combinations; `bake app-3-12-slim` builds one.
- Matrix values may be maps: `matrix = { item = [{ tgt = "foo", version = "1.0" }, ...] }`,
  accessed with dot notation as `item.tgt` and `item.version`.

## Compose file as Bake input
```sh
docker buildx bake -f compose.yaml            # each service with build: becomes a target
```
Each service becomes a target; `build:` keys map to the matching Bake attributes. Fields the
Compose specification lacks go in `x-bake`. The documented `x-bake` fields are `cache-from`,
`cache-to`, `contexts`, `no-cache`, `no-cache-filter`, `output`, `platforms`, `pull`, `secret`,
`ssh` and `tags`:
```yaml
services:
  api:
    build:
      context: .
      x-bake:
        platforms: [linux/amd64, linux/arm64]
        cache-to: ["type=registry,ref=registry.example.com/cache:api,mode=max"]
        output: ["type=registry"]
```
A `.env` file in the working directory supplies defaults for interpolation (system environment
variables take precedence). Compose input cannot declare variables or global attributes, and
has no `inherits` (use YAML anchors instead). Pass several files with
`-f compose.yaml -f docker-bake.override.hcl` to add CI-only settings; with no `-f`, Bake merges
whatever it finds in this order: `compose.yaml`, `compose.yml`, `docker-compose.yml`,
`docker-compose.yaml`, `docker-bake.json`, `docker-bake.hcl`, `docker-bake.override.json`,
`docker-bake.override.hcl`.

## --set overrides
```sh
docker buildx bake --set api.platform=linux/arm64
docker buildx bake --set '*.cache-from=type=gha' --set '*.cache-to=type=gha,mode=max'
docker buildx bake --set api.args.VERSION=1.4.0 --set api.tags=reg/api:1.4.0
docker buildx bake --set 'api.output=type=docker'      # load locally
```
Targets are matched with Go `path.Match` patterns (`*`, `foo*`). `--push` / `--load` are
conditional shorthands for `*.output` (they leave `local` and `tar` outputs alone). For list
fields, repeat `--set` or use `+=` to append (`--set api.tags+=reg/api:latest`); an empty
non-append value such as `--set api.tags=` clears the list. Array literals like `[a,b]` are not
supported.

## --print and --list
```sh
docker buildx bake --print app            # resolved JSON, no build
docker buildx bake --list=targets
docker buildx bake --list=variables
```
Always `--print` after editing a matrix: it shows every generated target name, which is
where typos surface.

## Gotchas
- Quote `--set` values containing `*` or `,` so the shell does not glob/split them.

## Checked

Checked 2026-10-23 against the Docker docs Bake pages (matrices, compose-file, overrides), docker/buildx `docs/bake-reference.md` and `docs/reference/buildx_bake.md` (main branch).

- Matrix: unique target names via `name`, multiple axes, map values with dot notation.
- Compose input: service-to-target translation, `.env` handling, the `x-bake` field list, the limits (no variables, no `inherits`).
- Default file lookup order and `--set` semantics (patterns, `+=`, clearing, `--list=targets|variables`).
- Removed unconfirmed claims about services without `build:`, image-to-tag naming, matrix with `inherits`, and the name character rules.

Method: documentation only; no commands were run.
