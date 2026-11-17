---
id: computing-software.cloud-infrastructure-engineering.docker.named-build-contexts
name: named-build-contexts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, dockerfile, buildkit, build-context, named-build-context, build-context-flag, additional-context, copy-from-context, local-dependency-build, stage-override]
level: advanced
description: "Use --build-context name=path|url|docker-image|oci-layout to give a build extra directories, images or repos accessible via COPY --from and FROM, and to swap stages or base images at build time."
sources: ["https://docs.docker.com/reference/cli/docker/buildx/build/#build-context", "https://docs.docker.com/build/concepts/context/#named-contexts", "https://docs.docker.com/reference/compose-file/build/#additional_contexts"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Named build contexts (--build-context)

**Goal:** build a service that needs a sibling library directory, a locally built base
image, or a pinned upstream repo, without copying files into one giant context or editing
the Dockerfile per environment.

## Syntax
```sh
docker build --build-context <name>=<source> .
```
Sources:
| Form | Example |
|---|---|
| local directory | `--build-context shared=../libs/shared` |
| Git URL | `--build-context proto=https://github.com/org/proto.git#v3` |
| HTTP tarball | `--build-context assets=https://cdn.example.com/assets.tar.gz` |
| image | `--build-context base=docker-image://myregistry/base:dev` |
| OCI layout dir | `--build-context base=oci-layout:///path/to/layout:<tag>` or `...layout@sha256:<digest>` |

In the Dockerfile the name is used like a stage (`FROM name`, `COPY --from=name`,
`RUN --mount=from=name`):
```dockerfile
FROM base                       # resolves to the docker-image:// context
COPY --from=shared . /app/libs/shared
RUN --mount=from=proto,source=.,target=/proto protoc -I/proto ...
```

## Overriding a stage or base image
A named context with the **same name as a stage or image reference** replaces it:
```dockerfile
FROM python:3.12-slim AS base
```
```sh
docker build --build-context python:3.12-slim=docker-image://python:3.12-slim@sha256:... .
docker build --build-context base=docker-image://localhost:5000/base:pr-123 .
```
The context overrides a stage called `name` when used as `FROM ... AS name`, and the first
command pins an image reference without editing the file.

## Compose and Bake
```yaml
services:
  api:
    build:
      context: ./services/api
      additional_contexts:
        shared: ../libs/shared
        base: docker-image://org/base:dev
```
Bake:
```hcl
target "api" {
  contexts = {
    shared = "../libs/shared"
    base   = "target:base"     # another bake target's output, no registry round-trip
  }
}
```
`target:` sources let one bake run build a base and consume it in the same invocation.

Compose also accepts `additional_contexts` as a list (`name=value`) or mapping. Values other
than paths and Git URLs must carry a scheme prefix (such as `docker-image://`), and a context
can refer to an image built by another service.

## Gotchas
- Named contexts need BuildKit (buildx); Compose warns if the image builder does not support
  additional contexts.
- Contexts can be used as `FROM name`, `--from=name`, and as a `#syntax=name` override.
- The `.dockerignore` rules for named contexts were not confirmed in the docs; check the
  `.dockerignore` behaviour of your builder before relying on it for large sibling directories.

## Verify
Run `docker build --progress=plain --build-context shared=../libs/shared .` and confirm the
steps that read from `shared` build as expected.

## Checked

Checked 2026-10-23 against the docker/buildx `build --build-context` reference, the Docker docs "Build context" page (named contexts) and the compose-spec `build.md` (`additional_contexts`).

- Supported context value kinds (local directory, OCI layout, image, Git URL, HTTP URL) and the `docker-image://` and `oci-layout:///` schemes (the draft's `oci-layout://./out@sha256:` form was wrong).
- Overriding a stage `AS name`, `FROM name`, `--from=name`, `RUN --mount=from=name`; `#syntax=name` override.
- Compose `additional_contexts` list/mapping forms and service-built images.
- Removed the buildx 0.8 / syntax 1.4 version gate, the per-context `.dockerignore` and cache-hashing claims, and the driver-transfer claims, none of which the docs state.

Method: documentation only; no commands were run.
