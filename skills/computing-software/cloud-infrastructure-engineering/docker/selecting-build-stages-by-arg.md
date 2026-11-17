---
id: computing-software.cloud-infrastructure-engineering.docker.selecting-build-stages-by-arg
name: selecting-build-stages-by-arg
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, multi-stage, conditional-stage, stage-selection-arg, build-arg, arg-before-from, buildkit]
level: advanced
status: docs-checked
description: "Pick which stage feeds the final image with an ARG in FROM (FROM build-${VARIANT}) so BuildKit builds only the chosen branch; covers defaults, checks and legacy builder."
sources: ["https://docs.docker.com/reference/dockerfile/#understand-how-arg-and-from-interact", "https://docs.docker.com/build/building/multi-stage/#differences-between-legacy-builder-and-buildkit", "https://docs.docker.com/reference/build-checks/invalid-default-arg-in-from/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Selecting stages with an ARG

Dockerfiles have no `if`. The idiom is a stage per branch plus a `FROM` whose image name is
an `ARG`. With BuildKit only the stages the target depends on are processed, so unused branches
are skipped.

## Pattern
```dockerfile
# syntax=docker/dockerfile:1
ARG VARIANT=release          # declared before the first FROM so FROM can use it

FROM ubuntu AS base
RUN apt-get update && apt-get install -y ca-certificates

FROM base AS variant-release
COPY dist/app /usr/local/bin/app

FROM base AS variant-debug
RUN apt-get install -y gdb
COPY dist/app-debug /usr/local/bin/app

FROM variant-${VARIANT} AS final
ENTRYPOINT ["/usr/local/bin/app"]
```
```bash
docker build -t app .                              # release
docker build --build-arg VARIANT=debug -t app:debug .
```

Same trick to pick a base image:
```dockerfile
ARG BASE=scratch
FROM ${BASE}
```

## Rules
- `FROM` instructions can use variables declared by `ARG` before the first `FROM`; such an ARG is
  outside any stage, so redeclare it (`ARG VARIANT`, no value) inside a stage to read it there.
- Give the ARG a default that makes a valid reference: an image reference should be valid with no
  `--build-arg` (`InvalidDefaultArgInFrom` check); undeclared ARGs in `FROM` trigger
  `UndefinedArgInFrom`.
- A name that is not a stage is treated as an image reference to pull.
- Compose: `build.args` (`VARIANT: debug`); Bake: `args = { VARIANT = "debug" }`.

## When to prefer --target
If the branches are endpoints (dev image vs prod image), `--target` is clearer. Use the ARG
pattern when the branch sits in the middle and later stages are shared (both variants get the
same final `ENTRYPOINT`, labels and user).

## Gotchas
- The legacy builder processes all stages leading up to the target, including ones the target
  does not depend on; BuildKit builds only the stages the target depends on.

## Verify
`docker build --build-arg VARIANT=debug --progress=plain .` shows no steps from `variant-release`;
`docker build --check .` reports no `InvalidDefaultArgInFrom` warning.

## Checked

Checked 2026-10-23 against the Dockerfile reference ("Understand how ARG and FROM interact"), docker/docs "Multi-stage builds" (BuildKit builds only dependent stages) and the BuildKit rule pages InvalidDefaultArgInFrom and UndefinedArgInFrom.
Confirmed: global ARG use in FROM and redeclaration inside stages, the rule that default values must give a valid image reference, legacy builder versus BuildKit stage processing, Compose `args` and Bake `args`. Removed the exact error message text, the cache-ref remark, the grep verification and pinned distro tags.

Method: documentation only; no commands were run.
