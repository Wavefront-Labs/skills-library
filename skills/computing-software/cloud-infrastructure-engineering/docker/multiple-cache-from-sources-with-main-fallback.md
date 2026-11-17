---
id: computing-software.cloud-infrastructure-engineering.docker.multiple-cache-from-sources-with-main-fallback
name: multiple-cache-from-sources-with-main-fallback
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, remote-cache, cache-from-fallback, cache-from, cache-to, registry-cache, gha-cache]
level: advanced
status: docs-checked
description: "Seed feature-branch builds from the main branch cache: several --cache-from refs or GHA scopes, writing only the branch cache, read-only PR caches, and cleaning stale refs."
sources: ["https://docs.docker.com/build/cache/backends/", "https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/cache/backends/gha/", "https://docs.docker.com/reference/cli/docker/buildx/build/#cache-from"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multiple cache-from sources with main fallback

A new branch has no cache of its own; its first build would be cold. Import the main branch
cache as well, and export only to the branch's own ref.

## Registry backend
```bash
BR=$(git rev-parse --abbrev-ref HEAD | tr '/' '-' | tr '[:upper:]' '[:lower:]')
docker buildx build \
  --cache-from type=registry,ref=reg.example.com/app:cache-$BR \
  --cache-from type=registry,ref=reg.example.com/app:cache-main \
  --cache-to   type=registry,ref=reg.example.com/app:cache-$BR,mode=max,image-manifest=true,oci-mediatypes=true \
  -t reg.example.com/app:$BR --push .
```
- Docker documents this as a common pattern: import the cache of both the current branch and
  `main`, and export to the branch's own location. Each cache location is overwritten on write,
  so keep one ref per scope.
- If a `--cache-from` ref does not exist (first build of a branch) the import step fails but the
  build continues.
- `mode=max` exports intermediate stages too, which is what makes the cache useful for
  multi-stage builds; `min` (the default) caches only layers of the exported image.

## GitHub Actions cache backend
```yaml
- uses: docker/build-push-action@v7
  with:
    cache-from: |
      type=gha,scope=${{ github.ref_name }}
      type=gha,scope=main
    cache-to: type=gha,scope=${{ github.ref_name }},mode=max
```
The `gha` backend (`scope` defaults to `buildkit`) identifies cache objects by scope; use
distinct scopes to keep several images in one repository apart (`scope=api-${{ github.ref_name }}`).
GitHub Actions cache access rules still apply: a workflow can access only the cache for the
current branch, the base branch and the default branch. Cache access is subject to GitHub's
usage limits and eviction policy.

## Pull requests from forks
Untrusted builds should not write shared caches: import only and omit `cache-to`.
```yaml
    cache-from: type=registry,ref=reg.example.com/app:cache-main
```

## Housekeeping
- Delete `cache-<branch>` refs when branches are deleted (registry API or a retention rule).
- The GHA cache is subject to GitHub's size limits and eviction policy, so large caches for many
  branches can displace others. `min` is smaller than `max`; experiment with both.

## Verify
Build with `--progress=plain` and look for imported cache and `CACHED` steps on the second run.

## Checked

Checked 2026-10-23 against the Docker docs cache backends pages (index, registry, gha) and docker/buildx `build --cache-from` reference (main branch).

- Multiple `--cache-from` plus one branch-specific `--cache-to` is the documented pattern; `mode` default `min`; missing cache-from ref fails the import step but the build continues.
- `gha` backend `scope` default (`buildkit`), branch access rule (current, base and default branch), GitHub usage limits and eviction.
- Current `docker/build-push-action` major is v7.4.0 (releases API).
- Removed unconfirmed claims about import ordering/priority, `cache-to: ""` for forks and the grep-based verification.

Method: documentation only; no commands were run.
