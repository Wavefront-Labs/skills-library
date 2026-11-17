---
id: computing-software.cloud-infrastructure-engineering.docker.bake-contexts-linking-targets
name: bake-contexts-linking-targets
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, bake, bake-contexts, bake-target-context, named-build-context, buildx-bake, monorepo]
level: advanced
status: docs-checked
description: "Chain Bake targets with contexts = { name = \"target:base\" } so a shared base builds once and feeds other targets without a registry push; also image, URL and OCI contexts."
sources: ["https://docs.docker.com/build/bake/contexts/", "https://docs.docker.com/build/bake/reference/", "https://docs.docker.com/reference/cli/docker/buildx/build/#build-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linking Bake targets with contexts

Named contexts replace an image or stage reference in a Dockerfile with another source.
In Bake, the source can be **another target**, so a base image is built once in the same
run and consumed directly from the build graph.

## Pattern
```dockerfile
# base.Dockerfile
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl \
 && rm -rf /var/lib/apt/lists/*
```
```dockerfile
# api/Dockerfile and worker/Dockerfile
FROM company-base
COPY app /usr/local/bin/app
```
```hcl
# docker-bake.hcl
group "default" { targets = ["api", "worker"] }

target "base" {
  dockerfile = "base.Dockerfile"
}
target "api" {
  context  = "api"
  contexts = { company-base = "target:base" }
  tags     = ["reg.example.com/api:latest"]
}
target "worker" {
  context  = "worker"
  contexts = { company-base = "target:base" }
  tags     = ["reg.example.com/worker:latest"]
}
```
```bash
docker buildx bake            # base is built as part of the same run and consumed by api and worker
docker buildx bake --print    # shows the resolved contexts
```

## Other context sources
| Value | Meaning |
|---|---|
| `target:<name>` | Output of another Bake target |
| `docker-image://alpine:3.20@sha256:...` | Pin or swap an image referenced by `FROM` |
| `./vendor` or `../shared` | Local directory, e.g. `COPY --from=shared` |
| `https://github.com/org/repo.git#v1` | Git repository (HTTP URLs are also supported) |
| `oci-layout:///path/to/layout@sha256:...` | Local OCI layout from a previous export |

Override from the CLI without editing HCL:
`docker buildx bake --set api.contexts.company-base=docker-image://reg.example.com/base:2024-10` (the `--set target.contexts.bar=../bar` form is in the buildx reference).

## Gotchas
- Without Bake, a plain `docker build` would try to pull `company-base` as an image name.
  Document the Bake entry point.
- The Docker docs recommend a single multi-stage Dockerfile with several targets where that
  is possible; use `target:` contexts when the Dockerfiles cannot be merged into one.

## Checked

Checked 2026-10-23 against the Docker docs Bake "Contexts" page and the buildx `build --build-context` reference (docker/docs and docker/buildx, main branch).

- Supported context values (local directory, container image, Git URL, HTTP URL, another target via the `target:` prefix) and the `contexts = { name = "target:base" }` form.
- `docker-image://` and `oci-layout:///path:<tag>` / `@sha256:<digest>` schemes for `--build-context`.
- `--set target.contexts.<name>=value` overrides a named context.
- Removed unconfirmed claims about platform matching and driver/buildx version requirements for `target:` contexts, and the claim that the base is "never pushed".

Method: documentation only; no commands were run.
