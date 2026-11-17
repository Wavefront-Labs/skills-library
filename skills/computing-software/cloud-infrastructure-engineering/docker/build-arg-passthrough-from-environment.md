---
id: computing-software.cloud-infrastructure-engineering.docker.build-arg-passthrough-from-environment
name: build-arg-passthrough-from-environment
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, build-args, build-arg-from-env, compose-build, bake-variables, ci-builds]
level: practitioner
status: docs-checked
description: "Pass build args from the shell environment: --build-arg NAME without a value, Compose args list form, Bake variables, and how unset values fall back to Dockerfile defaults."
sources: ["https://docs.docker.com/reference/cli/docker/buildx/build/#build-arg", "https://docs.docker.com/reference/dockerfile/#predefined-args", "https://docs.docker.com/reference/compose-file/build/#args", "https://docs.docker.com/build/bake/variables/", "https://docs.docker.com/build/bake/overrides/", "https://docs.docker.com/build/building/secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Passing build args from the environment

## docker build
```bash
export VERSION=1.4.2
docker build --build-arg VERSION .          # no "=value": taken from the environment
docker build --build-arg VERSION=1.4.2 .    # explicit
```
- With no value, the builder propagates the value from the local environment.
- You must add `--build-arg` for each build argument, and the Dockerfile must declare it with `ARG`
  to use it.
- Proxy args (`HTTP_PROXY`, `HTTPS_PROXY`, `FTP_PROXY`, `NO_PROXY`, `ALL_PROXY`, and lowercase
  forms) are predefined and are excluded from `docker history` and the build cache by default; if
  you declare one with `ARG` in the Dockerfile it is recorded in history and changing it
  invalidates the cache.

## Compose
```yaml
services:
  app:
    build:
      context: .
      args:
        - VERSION
        - GIT_SHA=${GIT_SHA:-unknown}
        - BASE_IMAGE=${BASE_IMAGE:?set BASE_IMAGE}
```
`args` can be a mapping or a list. A value can be omitted (`- VERSION`), in which case the value
must be obtained at build time, otherwise the build argument is not set. `${VAR:-default}` and
`${VAR:?message}` are Compose interpolation.

## Bake
```hcl
variable "VERSION" { default = "dev" }    # an environment variable VERSION overrides the default
target "app" {
  args = { VERSION = VERSION, GIT_SHA = null }   # null: the Dockerfile's ARG value is used
}
```
```bash
VERSION=1.4.2 docker buildx bake app
docker buildx bake --set app.args.VERSION=1.4.2
```

## CI pattern
```bash
docker build \
  --build-arg VERSION="${GITHUB_REF_NAME}" \
  --build-arg GIT_SHA="${GITHUB_SHA}" .
```
An `ARG` takes effect from the line where it is declared, so declare frequently changing ones
late in the Dockerfile, right before the `RUN` that uses them.

## Gotchas
- Build arguments are visible in `docker history` and in `max` mode provenance attestations; do
  not pass tokens this way. Use a build secret instead, for example
  `docker build --secret id=token,env=TOKEN .` with `RUN --mount=type=secret,id=token,...`.
- An `ENV` with the same name always overrides an `ARG` of that name.

## Checked

Checked 2026-10-23 against the Dockerfile reference (ARG, predefined ARGs), docker/docs build variables page, the buildx `docker buildx build --build-arg` reference, the Compose build `args` reference, the Bake reference, Bake variables and overrides pages and the build secrets page.
Confirmed: `--build-arg NAME` without a value propagates from the environment; proxy args are excluded from history and cache unless declared with ARG; Compose `args` list and mapping forms and omitted-value behaviour; Bake `null` args and `--set target.args.KEY=value`; env-overrides-variable defaults; `--secret id=...,env=...`. Removed the unconfirmed unset-versus-empty behaviour, the date-stamp CI argument, the exact "not consumed" warning text and the sudo remark.

Method: documentation only; no commands were run.
