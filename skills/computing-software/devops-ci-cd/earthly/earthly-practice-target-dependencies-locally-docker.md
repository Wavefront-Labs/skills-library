---
id: computing-software.devops-ci-cd.earthly.earthly-practice-target-dependencies-locally-docker
name: earthly-practice-target-dependencies-locally-docker
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, best-practices, artifact-reference, locally, with-docker, load, git-clone, dind]
level: advanced
status: docs-checked
description: "Pass files and images between Earthly targets with artifact references and WITH DOCKER --load, including LOCALLY, GIT CLONE vs RUN git clone, earthly/dind and pass-through."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Practices: target dependencies, LOCALLY and WITH DOCKER

## Declare dependencies with references
Outputs (`SAVE ARTIFACT ... AS LOCAL`, image pushes) happen only at the end of a successful build, so another target cannot read them mid-build. Targets with no reference between them also run in parallel.
```Dockerfile
all:
    BUILD +build
dep:
    SAVE ARTIFACT my-artifact.jar
build:
    COPY +dep/my-artifact.jar ./
```
Images: use `WITH DOCKER --load=+dep-img` with `SAVE IMAGE my-co/my-image:latest` in `+dep-img`, not a registry push.

## LOCALLY targets
Never pass files between `LOCALLY` targets by local paths; order is not guaranteed. Make the producer `SAVE ARTIFACT ./my-artifact.txt` and the consumer `COPY +dep/my-artifact.txt ./build/my-artifact.txt`. For images use `WITH DOCKER --load=+build-img` inside a `LOCALLY` target. Prefer `SAVE ARTIFACT ... AS LOCAL` over `LOCALLY` for generated code.

Optional `LOCALLY` pattern: `ARG run_locally=false`, then `IF [ "$run_locally" = "true" ]` / `LOCALLY` / `ELSE` / `FROM earthly/dind:...` / `END`; run with `earthly +my-target --run_locally=true`.

## WITH DOCKER
- Declare external images with `WITH DOCKER --pull hello-world`: they are cached and the inner daemon is not logged in to registries. `--compose` pulls compose images itself unless they come from `--load`.
- Use `earthly/dind` (preferably `:alpine`), e.g. `FROM earthly/dind:alpine-3.19-docker-25.0.5-r0`. Otherwise `DO github.com/earthly/lib+INSTALL_DIND` before `COPY`.
- The daemon data is wiped after the block, but `SAVE ARTIFACT` after `END` still works.

## GIT CLONE
Prefer cross-repo references (`COPY repo-1+file/my-file.txt ./` after `IMPORT github.com/my-co/repo-1`). `GIT CLONE` beats `RUN git clone`: cache-aware, commit-hash-aware, passes through auth. It is a shallow clone without branch, origin or tags.

## IF/FOR and pass-through
Use `RUN if` / `RUN for` when only `RUN` is involved; `IF`/`FOR` when other Earthly commands are needed. A wrapper target can re-emit artifacts via `COPY (+build --os=windows) ./` plus `SAVE ARTIFACT ./*`, or images via `FROM +build` plus `SAVE IMAGE`.

## Gotcha
Do not put all Earthfiles in a dedicated directory; Earthly has no `docker build -f` equivalent.

## Checked

2026-11-07. Read docs/guides/best-practices.md in full. The sections on target dependencies, LOCALLY, WITH DOCKER --load/--pull, earthly/dind, GIT CLONE, IF/FOR and saving artifacts from WITH DOCKER match. Nothing removed.
Method: documentation only; no commands were run.
