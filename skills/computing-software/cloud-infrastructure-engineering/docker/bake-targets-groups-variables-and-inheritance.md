---
id: computing-software.cloud-infrastructure-engineering.docker.bake-targets-groups-variables-and-inheritance
name: bake-targets-groups-variables-and-inheritance
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bake, docker-bake, buildx-bake, bake-targets, bake-groups, bake-variables, bake-functions, bake-inherits, hcl]
level: advanced
description: "Write docker-bake.hcl with targets, the default group, variables overridable from env, user functions and inherits to drive many image builds from one command."
sources: ["https://docs.docker.com/build/bake/targets/", "https://docs.docker.com/build/bake/variables/", "https://docs.docker.com/build/bake/funcs/", "https://docs.docker.com/build/bake/inheritance/", "https://docs.docker.com/build/bake/overrides/", "https://docs.docker.com/build/bake/reference/", "https://github.com/docker/metadata-action"]
status: docs-checked
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Bake targets, groups, variables and inheritance

**Goal:** replace a shell script of five `docker build` lines with a declarative file that
CI and developers run the same way: `docker buildx bake`.

## Skeleton
```hcl
# docker-bake.hcl
variable "REGISTRY" { default = "registry.example.com/shop" }
variable "TAG"      { default = "dev" }

function "img" {
  params = [name]
  result = ["${REGISTRY}/${name}:${TAG}"]
}

group "default" { targets = ["api", "worker"] }
group "all"     { targets = ["default", "docs"] }

target "_common" {
  platforms  = ["linux/amd64", "linux/arm64"]
  args       = { GO_VERSION = "1.23" }
  labels     = { "org.opencontainers.image.source" = "https://github.com/org/shop" }
  cache-from = ["type=registry,ref=${REGISTRY}/cache:main"]
}

target "api" {
  inherits   = ["_common"]
  context    = "."
  dockerfile = "services/api/Dockerfile"
  tags       = img("api")
}

target "worker" {
  inherits = ["_common"]
  target   = "worker"              # Dockerfile stage
  tags     = img("worker")
}

target "docs" {
  context = "docs"
  tags = img("docs")
  platforms = ["linux/amd64"]
}
```
```sh
docker buildx bake                 # group "default"
docker buildx bake api             # one target
TAG=1.4.0 docker buildx bake all --push
```

## Rules worth knowing
- With no target named, Bake builds the `default` group (or the target named `default`).
- Only `variable` blocks can be overridden by **environment variables of the same name**
  (`TAG=1.4.0`); values are coerced to the variable's type. Variables can also be given an
  explicit `type` and `validation` blocks.
- A target can override anything it inherits. With several entries in `inherits`, the target
  listed last wins on a conflict.
- Underscore-prefixed targets (`_common`) are the naming convention the Docker docs use for
  shared attributes; keep them out of groups.
- Bake ships the HCL standard library (`upper`, `split`, `formatdate`, `timestamp`, `equal`,
  `notequal`, `coalesce`, `replace` are all in the buildx stdlib reference).
- `docker/metadata-action` writes a `docker-metadata-action` target (name set by its
  `bake-target` input); inherit it to get CI tags and labels.
- With no `-f`, Bake loads and merges every file it finds in this order: `compose.yaml`,
  `compose.yml`, `docker-compose.yml`, `docker-compose.yaml`, `docker-bake.json`,
  `docker-bake.hcl`, `docker-bake.override.json`, `docker-bake.override.hcl`; later files win.

## Verify
`docker buildx bake --print` prints the fully resolved JSON (tags, args, platforms) without
building; check inheritance and variable substitution there before pushing.

## Checked

Checked 2026-10-23 against the Docker docs Bake pages (targets, variables, inheritance, funcs, overrides), docker/buildx `docs/bake-reference.md` and `docs/bake-stdlib.md`, and the docker/metadata-action README (main branch).

- The `default` group/target behaviour, the file lookup and merge order, `function` blocks with `params`/`result`.
- Variable override by same-name environment variable (only `variable` blocks), explicit typing and `validation`.
- `inherits` precedence (last listed wins) and the stdlib functions named above.
- Removed the unconfirmed map-merge versus list-replace rule and the claim that underscore targets are unspecial.

Method: documentation only; no commands were run.
