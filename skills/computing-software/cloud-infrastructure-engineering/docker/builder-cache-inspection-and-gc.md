---
id: computing-software.cloud-infrastructure-engineering.docker.builder-cache-inspection-and-gc
name: builder-cache-inspection-and-gc
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, buildkit, buildx, layer-caching, build-cache, buildx-du, buildx-prune, cache-gc, builder-prune, keep-storage, gc-policy, buildkitd-toml]
level: practitioner
description: "See what is eating the BuildKit cache with buildx du, prune it selectively, and set a gc policy (keep-storage) so builders do not fill the disk."
sources: ["https://docs.docker.com/reference/cli/docker/buildx/du/", "https://docs.docker.com/reference/cli/docker/buildx/prune/", "https://docs.docker.com/build/cache/garbage-collection/", "https://docs.docker.com/reference/cli/docker/builder/prune/", "https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Inspecting and garbage-collecting the builder cache

**Goal:** know what the build cache holds, free space without losing the layers that make
builds fast, and configure automatic GC so it never becomes an emergency.

## Inspect
```sh
docker buildx du                 # build cache records of the current builder
docker buildx du --verbose       # shorthand for --format=pretty
docker buildx du --builder mybuilder
```
Record types (the valid `type` filter values) are `internal`, `frontend`, `source.local`,
`source.git.checkout`, `exec.cachemount` and `regular`. Other filter keys include `until`, `id`,
`parents`, `description`, `inuse`, `mutable`, `immutable`, `shared` and `private`; records that
are in use are not reclaimable.

## Prune
```sh
docker buildx prune                                   # clear the build cache of the builder
docker buildx prune --all                             # also clear internal helper and frontend images
docker buildx prune --filter until=72h                # keep records used in the last 72h
docker buildx prune --filter type=exec.cachemount     # only cache mounts
docker buildx prune --reserved-space 10GB             # disk space always allowed to keep for cache
docker buildx prune --max-used-space 50GB             # maximum space allowed for cache
docker buildx prune --min-free-space 20GB             # target free disk space after pruning
docker builder prune --keep-storage 10GB              # docker CLI command: amount of disk space to keep
```
`docker buildx prune` has `--reserved-space`, `--max-used-space` and `--min-free-space`;
`docker builder prune` has `--keep-storage`, `--all` and `--filter`.

## Automatic GC policy
For builders other than the `docker` driver, GC is configured in a `buildkitd.toml`. The
high-level options are `reservedSpace` (usage below it is not reclaimed), `maxUsedSpace` (usage
above it is reclaimed) and `minFreeSpace` (free space to keep); each accepts bytes, a unit
string such as `512MB`, or a percentage of the disk. Per-policy rules use `[[worker.oci.gcpolicy]]`
with `keepDuration` and `filters` (BuildKit syntax uses `==`):
```toml
[worker.oci]
  gc = true
  reservedSpace = "20GB"
  maxUsedSpace = "50GB"
  [[worker.oci.gcpolicy]]
    reservedSpace = "512MB"
    keepDuration = "48h"
    filters = ["type==source.local", "type==exec.cachemount", "type==source.git.checkout"]
  [[worker.oci.gcpolicy]]
    all = true
    reservedSpace = "20GB"
```
Apply with `docker buildx create --buildkitd-config buildkitd.toml --name ci --driver docker-container`.
The default `docker` driver builder is configured in `daemon.json` (or Docker Desktop **Settings
> Docker Engine**); `defaultKeepStorage` sets the cache size limit that the default policies
derive from:
```json
{"builder": {"gc": {"enabled": true, "defaultKeepStorage": "20GB"}}}
```
Custom policies use `"policy": [{ "reservedSpace": "50GB", "keepDuration": ["1440h"] }, ...]`, and
filters there use a single `=` (`type=source.local`). The default policies remove cache that can
be regenerated (local contexts, Git checkouts, cache mounts) unused for 48 hours, cache unused for
60 days, then unshared and finally any cache above the limit.

## What to keep
Prefer pruning with `--filter until=<duration>` or a space limit over `--all`, so recently
used layers survive; for most users the default GC behaviour is enough.

## Gotchas
- Changing the Docker Engine GC settings means editing `daemon.json`; the Docker docs describe
  GC for the `docker` driver there and for other drivers in `buildkitd.toml`.
- Pruning the cache on a shared runner slows the next builds that relied on it.

## Verify
Run `docker buildx du` before and after pruning and confirm that a subsequent build still shows
`CACHED` for the layers you intended to keep.

## Checked

Checked 2026-10-23 against the docker/buildx `buildx prune` and `buildx du` references, the Docker docs "Build garbage collection" page, the BuildKit `docs/buildkitd.toml.md`, the docker/cli `builder prune` reference and the dockerd daemon.json reference (main branches).

- `buildx prune` flags (`--all`, `--filter`, `--reserved-space`, `--max-used-space`, `--min-free-space`) and the filter keys and `type` values; `docker builder prune --keep-storage`. The draft's `buildx prune --keep-storage` flag is not in the buildx reference.
- GC configuration: `daemon.json` `builder.gc` with `defaultKeepStorage` for the `docker` driver, `buildkitd.toml` `reservedSpace` / `maxUsedSpace` / `minFreeSpace` and `[[worker.oci.gcpolicy]]` for other drivers; `=` versus `==` in filters; default policy summary.
- The draft's `gckeepstorage` / `keepBytes` keys are not in the current `buildkitd.toml` reference and were replaced.
- Removed the `docker system df`, `docker image prune`/`system prune` and builder-volume claims, which were not checked.

Method: documentation only; no commands were run.
