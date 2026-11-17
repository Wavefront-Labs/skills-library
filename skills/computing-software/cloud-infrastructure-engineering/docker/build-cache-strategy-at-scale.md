---
id: computing-software.cloud-infrastructure-engineering.docker.build-cache-strategy-at-scale
name: build-cache-strategy-at-scale
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, cache-from, cache-to, type=registry, type=gha, type=s3, type=local, type=inline, mode=max, mode=min, github-actions-cache, cache-eviction, ephemeral-ci-runner, cache-poisoning, cache-scoping, imagetools]
level: advanced
status: docs-checked
description: "Shipping BuildKit's cache between ephemeral CI runners: cache-from/cache-to backend types, mode=max vs min, per-branch scoping, and why a cache mount alone doesn't survive a fresh runner."
sources: ["https://docs.docker.com/build/cache/backends/", "https://docs.docker.com/build/cache/backends/gha/", "https://docs.docker.com/build/cache/backends/registry/", "https://docs.docker.com/build/cache/garbage-collection/", "https://docs.docker.com/build/builders/drivers/", "https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Build cache strategy at scale (CI fleets)

**Goal:** a fresh, stateless CI runner gets the same warm-cache build speed as a laptop
that's built the image fifty times. This is the fleet-wide problem one layer up from
single-build cache mechanics, which `dockerfile-optimisation-and-multistage-builds` and
`buildkit-advanced-features` already cover (layer order, `RUN --mount=type=cache`, finding
cache busts). Those mounts are local to one BuildKit instance's state dir — a new EC2
runner, a new GitHub-hosted runner, or a scaled-to-zero builder starts with none of it.

## Cache export/import backends
`docker buildx build --cache-to type=<backend>,<opts> --cache-from type=<backend>,<opts>`:
| Backend | Where it lives | Notes |
|---|---|---|
| `inline` | Embedded in the image manifest itself | Simple, no extra infra, but Docker's docs say it does not scale with multi-stage builds as well as the other backends and it does not separate the cache from the image |
| `registry` | A separate (or same) registry ref, e.g. `app:buildcache` | Most portable; works from any runner with registry creds; supports `mode=max` |
| `gha` | GitHub Actions cache service | Parameters `url`, `token` and `scope` default from the Actions runner environment (`$ACTIONS_RUNTIME_TOKEN`, `$ACTIONS_RESULTS_URL`, scope `buildkit`). GitHub limits total cache per repository (default 10 GB, configurable in Actions settings) and removes entries not accessed for 7 days, so large `mode=max` caches can be evicted and builds slow down |
| `s3` | Any S3-compatible bucket | Parameters `region`, `bucket` and `name`; good for self-hosted runners |
| `local` | A directory (`type=local,dest=/tmp/cache`) | Export with `dest=`, import with `src=`; useful for self-hosted runners with a persistent disk between jobs |

## `mode=min` vs `mode=max`
Default `mode=min` only caches layers that are exported into the resulting image. `mode=max`
exports every intermediate stage too — essential for multi-stage builds where a builder
stage (e.g. `go build`, `npm run build`) is expensive but doesn't appear in the final
image. Without `mode=max`, a cache hit on the final `COPY --from=build` stage still forces
a full rebuild of `build` on a fresh runner because its layers were never exported. The
cost: `mode=max` caches are larger — budget registry storage and CI minutes accordingly.

## Scoping the cache key
A single shared `app:buildcache` ref across all branches means a feature branch's build can
both poison the cache other branches read (a broken/huge layer pushed as "latest cache") and
get invalidated by unrelated branch churn. Common pattern:
```
--cache-from type=registry,ref=app:buildcache-main
--cache-from type=registry,ref=app:buildcache-$BRANCH
--cache-to   type=registry,ref=app:buildcache-$BRANCH,mode=max
```
Read from both `main`'s cache (broad base) and the branch's own cache (narrow, recent);
write only to the branch's — keeps `main`'s cache from being overwritten by in-progress
branch work while still giving every branch a warm starting point.

## Pruning
Registry-backed caches grow if nothing expires them — use your registry's retention or
lifecycle feature (if it has one) for the `*-buildcache*` tags. The local BuildKit cache
separately needs pruning on self-hosted runners that aren't ephemeral, for example
`docker buildx prune --filter until=168h`; the daemon's BuildKit garbage collector
also has configurable policies (see the Docker docs page on build garbage collection).

## Gotchas
- The registry backend uses OCI media types by default (`oci-mediatypes=true`); a registry that
  rejects them needs `oci-mediatypes=false`. Test the real round trip (push from runner A,
  pull from a clean runner B) rather than trusting that the flag was accepted.
- Cache export errors fail the build unless you set `ignore-error=true` on `--cache-to`
  (default `false` on the registry, local, s3 and gha backends).
- The default `docker` driver supports cache export only for `inline`, `local`, `registry` and
  `gha`, and only with the containerd image store; use a `docker-container` builder otherwise.

## Verify
On a throwaway/clean runner (no local BuildKit state), run the full CI build twice with
`--progress=plain`: the first run should show real work; after a trivial unrelated file
change, the second run's dependency-install and build stages should show `CACHED` for
everything upstream of the change, pulled entirely from the remote cache backend, not
local state.

## Checked

2026-10-26 against Docker docs (docker/docs main, commit of 2026-10-23). Confirmed: backend parameter tables (gha url/token/scope defaults, registry oci-mediatypes and ignore-error defaults, s3 region/bucket/name, local dest/src), mode=min default and meaning, inline backend multi-stage caveat, driver cache-export support, buildx prune until filter, GitHub's 10 GB default per-repository cache limit and 7-day eviction (GitHub Docs, dependency caching reference). Removed unconfirmed claims about cache poisoning detail, registry lifecycle support per vendor, and cross-platform cache behaviour.

Method: documentation only; no commands were run.
