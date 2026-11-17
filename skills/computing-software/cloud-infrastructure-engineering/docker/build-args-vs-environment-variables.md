---
id: computing-software.cloud-infrastructure-engineering.docker.build-args-vs-environment-variables
name: build-args-vs-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, build-args, build-arg, arg, env, environment-variables, arg-before-from, arg-scope, env-override, env-persistence, build-time-vs-runtime, predefined-args, target-platform, docker-build, secrets-in-args]
level: practitioner
status: docs-checked
description: "Choosing ARG vs ENV in a Dockerfile: scope rules, FROM-line ARGs, predefined TARGETPLATFORM args, why ARG is not for secrets, and how ARG values poison the build cache and image history."
sources: ["https://docs.docker.com/reference/dockerfile/#arg", "https://docs.docker.com/build/building/variables/", "https://docs.docker.com/build/building/secrets/", "https://docs.docker.com/reference/dockerfile/#env"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Build args vs environment variables

**Goal:** parameterise a build without leaking values into the final image, and set
runtime config without accidentally baking it at build time.

## The one-line rule
`ARG` values are available only during the build; they do not persist in the image the way `ENV`
values do. `ENV` values are persisted in the image and in containers started from it. If a value
must be present when the container runs, it is `ENV`; if it only steers the build (a version to
download), it is `ARG`. You cannot override an `ENV` at build time, but you can combine the two:
`ARG` carries the value in, `ENV` persists it.

## Scope rules that bite
```dockerfile
ARG NODE_VERSION=20          # before FROM: usable only in FROM lines
FROM node:${NODE_VERSION}-slim
ARG NODE_VERSION             # redeclare (no value needed) to use it inside the stage
RUN echo "building with $NODE_VERSION"
```
- An `ARG` declared before the first `FROM` is outside any build stage; redeclare it with
  `ARG NAME` (no value) inside a stage to use its default there.
- An `ARG` takes effect from the line where it is declared; earlier uses expand to empty.
- An `ARG` declared in a stage is inherited by stages based on that stage; unrelated stages
  need their own `ARG` line (or a shared base stage that declares it).
- An `ENV` with the same name as an `ARG` always wins:
  `ARG V` then `ENV V=v1.0.0` ignores `--build-arg V=...`.
- To promote an arg into the image, use `ARG APP_PORT=8080` then `ENV APP_PORT=${APP_PORT}`.
- `ENV` values are persisted: `ARG CONT_IMG_VER` + `ENV CONT_IMG_VER=${CONT_IMG_VER:-v1.0.0}`
  keeps `v1.0.0` in the image when no `--build-arg` is given.
- Variable expansion is supported only in a limited set of instructions (see the Dockerfile
  reference, "Environment replacement"); `RUN`, `CMD` and `ENTRYPOINT` get the shell's expansion.

## Predefined args
`TARGETPLATFORM`, `TARGETOS`, `TARGETARCH`, `TARGETVARIANT`, `BUILDPLATFORM`, `BUILDOS`,
`BUILDARCH` and `BUILDVARIANT` are automatic platform args in the global scope: usable in `FROM`,
and redeclared without a value inside a stage to read them:
```dockerfile
FROM --platform=$BUILDPLATFORM golang AS build
ARG TARGETOS TARGETARCH
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o /out/app .
```
`HTTP_PROXY`, `HTTPS_PROXY`, `FTP_PROXY`, `NO_PROXY`, `ALL_PROXY` (and lowercase forms) are
predefined and excluded from `docker history` and the cache by default, unless you declare them
with `ARG`.

## ARG is not a secret mechanism
Build arguments are visible in `docker history` and in `max` mode provenance attestations.
Use a build secret instead:
`RUN --mount=type=secret,id=npm_token ...` with `docker build --secret id=npm_token,src=.npmrc .`
(or `env=VAR` to read from an environment variable). Secret mounts are not stored in the image.

## ENV gotchas
- Use `ENV KEY=value`; the legacy `ENV KEY value` form triggers the `LegacyKeyValueFormat` check.
- `ENV` set in a build stage only lands in the final image if the final stage is based on it.
- `docker run -e KEY` (no value) forwards the variable from the calling environment; runtime `-e`
  and `--env-file` overwrite variables defined in the image.
- `docker inspect` on the base image shows its `ENV` before you rely on a name being free.

## Verify
```bash
docker image inspect --format '{{json .Config.Env}}' app:latest      # ENV persisted
docker history --no-trunc app:latest                                  # ARG values that appear in history
docker build --check .
```

## Checked

Checked 2026-10-23 against the Dockerfile reference (ARG scope, using ARG variables, predefined ARGs, automatic platform ARGs, ENV), docker/docs build variables page, build secrets page and the buildx `--build-arg` reference.
Confirmed: ARG versus ENV persistence and the ENV-overrides-ARG rule; scope and inheritance rules for ARG and FROM; the ENV promotion pattern; visibility of build args in `docker history` and provenance; predefined and automatic platform args; proxy args excluded from history and cache; secret mounts; runtime `-e` overwrites image variables. Removed the cache-invalidation specifics, `ENV FOO=$(date)` and base-image variable examples that no documentation page covers.

Method: documentation only; no commands were run.
