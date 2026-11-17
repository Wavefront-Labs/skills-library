---
id: computing-software.cloud-infrastructure-engineering.docker.per-dockerfile-ignore-files
name: per-dockerfile-ignore-files
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, dockerignore, dockerfile-dockerignore, per-dockerfile-ignore, build-context, monorepo, multiple-dockerfiles, buildkit]
level: practitioner
description: "Use <Dockerfile>.dockerignore so each Dockerfile in a repo has its own context exclusions, with the precedence rules and the Compose/Bake behaviour that goes with it."
sources: ["https://docs.docker.com/build/concepts/context/#filename-and-location", "https://docs.docker.com/reference/compose-file/build/#dockerfile", "https://docs.docker.com/build/bake/reference/#targetdockerfile"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Per-Dockerfile .dockerignore files

**Goal:** in a repo with several Dockerfiles, let each build exclude different things without one
giant shared ignore list.

## The rule
If you use multiple Dockerfiles, place an ignore file in the same directory as the Dockerfile and
name it after the Dockerfile with `.dockerignore` appended. A Dockerfile-specific ignore file
takes precedence over the `.dockerignore` at the root of the build context if both exist; without
one, the root `.dockerignore` applies.

```
.
  .dockerignore
  docker/build.Dockerfile
  docker/build.Dockerfile.dockerignore
  docker/lint.Dockerfile
  docker/lint.Dockerfile.dockerignore
  docker/test.Dockerfile
  docker/test.Dockerfile.dockerignore
```
```sh
docker build -f docker/build.Dockerfile .     # uses docker/build.Dockerfile.dockerignore
```
The name is exactly `<DockerfileName>.dockerignore`: for `Dockerfile.prod` it is
`Dockerfile.prod.dockerignore`, and for a file simply named `Dockerfile` it is
`Dockerfile.dockerignore`.

## Patterns remain context-relative
Patterns in any `.dockerignore` are relative to the **context root**, not to the directory that
holds the ignore file. To exclude another service's source from a build with context `.`, write
`services/worker`, not `../worker`.

A per-service ignore file can use an allowlist:
```
*
!services/api
!libs/shared
!go.mod
!go.sum
```
(`*` first, then `!` exceptions: the last matching line wins.)

## Compose and Bake
The Compose `build.dockerfile` attribute sets an alternate Dockerfile; a relative path is resolved
from the build context:
```yaml
services:
  api:
    build: {context: ., dockerfile: docker/build.Dockerfile}
```
Bake takes `dockerfile = "docker/build.Dockerfile"` in a target.

## Gotchas
- Renaming the Dockerfile orphans its ignore file; a jump in the "transferring context" size is
  the symptom.
- A root-level `Dockerfile.dockerignore` takes precedence over `.dockerignore` for a default
  `docker build .`, so the plain `.dockerignore` is unused for that build.

## Verify
`docker build -f docker/build.Dockerfile --progress=plain .` and compare the "transferring context"
size with and without the per-Dockerfile file.

## Checked

Checked 2026-10-23 against docker/docs "Build context" (Filename and location of `.dockerignore`, Dockerfile-specific ignore files) and the Compose `build.dockerfile` and Bake reference pages.
Confirmed: the `<Dockerfile>.dockerignore` naming convention, precedence over the root file, context-root-relative patterns, Compose `dockerfile` relative to context, Bake `dockerfile`. Removed unconfirmed claims about legacy-builder history (19.03), stdin Dockerfiles, `dockerfile-inline` targets, IDE and hadolint behaviour, and the deliberate-syntax-error verification.

Method: documentation only; no commands were run.
