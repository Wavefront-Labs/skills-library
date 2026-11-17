---
id: computing-software.devops-ci-cd.build-systems.docker-cache-from-and-inline-cache
name: docker-cache-from-and-inline-cache
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, cache-from, inline-cache, docker-layer-caching]
level: practitioner
status: docs-checked
description: "Reuse Docker layer cache across CI runners with --cache-from: inline cache vs registry cache (mode=max), GHA cache backend, and why cache misses happen."
sources: ["https://docs.docker.com/build/cache/backends/", "https://docs.docker.com/build/cache/backends/inline/", "https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/cache/backends/gha/", "https://docs.docker.com/build/cache/optimize/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Docker --cache-from and inline cache

Ephemeral runners start with an empty BuildKit cache. Import cache from a remote source.

## Inline cache (simplest)
```bash
docker buildx build --cache-from type=registry,ref=registry.example.com/app:main \
  --cache-to type=inline -t registry.example.com/app:main --push .
```
Cache metadata is embedded in the image itself. Docker documents that it does not scale with multi-stage builds as well as the other backends and does not separate cache from output artifacts; use the registry cache for complex builds.

## Registry cache (recommended)
```bash
docker buildx build \
  --cache-from type=registry,ref=registry.example.com/app:buildcache \
  --cache-to type=registry,ref=registry.example.com/app:buildcache,mode=max \
  -t registry.example.com/app:$SHA --push .
```
`mode=min` (default) exports only layers of the final image; `mode=max` exports all stages' layers (larger cache, more hits). The registry backend defaults to `oci-mediatypes=true` and, since BuildKit v0.21, `image-manifest=true`; on older BuildKit, set `image-manifest=true` when exporting to registries such as Amazon ECR that do not support image indexes.

## GitHub Actions cache backend
```yaml
- uses: docker/build-push-action@<version-or-sha>
  with:
    cache-from: type=gha,scope=app
    cache-to: type=gha,mode=max,scope=app
```
The backend uses the GitHub Actions cache, so GitHub's limits apply (10 GB per repository by default, configurable; entries not accessed for 7 days are removed). The default `scope` is `buildkit`; use one `scope` per image so builds do not overwrite each other.

## Why it still misses
- `COPY . .` early in the Dockerfile invalidates every later layer on any change: copy lockfiles first, install dependencies, then copy source (Docker's guidance on ordering layers).
- Build arguments or labels with changing values (such as a build date) placed early.

## Verify
- [ ] Second CI build shows `CACHED` for dependency layers in the build log.

## Checked
Date: 2026-10-25. Documentation: docker/docs `content/manuals/build/cache/backends` (inline, registry, gha, index), `build/cache/optimize.md`, and GitHub's dependency-caching reference (github/docs).
Confirmed: inline cache syntax and its multi-stage limitation; registry parameters (`mode` min/max, default min; `oci-mediatypes`; `image-manifest` default true since BuildKit v0.21, ECR note); gha `scope` default `buildkit`; GitHub cache limit (10 GB default, configurable) and 7-day eviction.
Removed: the claims that inline cache is mode=min only in all cases, that the legacy builder ignores these options, and that platforms have separate cache entries (not stated in the pages read).
Method: documentation only; no commands were run.
