---
id: computing-software.devops-ci-cd.earthly.earthly-manage-cache
name: earthly-manage-cache
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, earthly-cache, cache-size-mb, cache-size-pct, earthly-prune, prune-reset, sat-update-drop-cache, buildkitd]
level: practitioner
status: docs-checked
description: "Set the Earthly local cache size with cache_size_mb and cache_size_pct, reset it with earthly prune, and reset or resize cache on a satellite or self-hosted runner."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/caching/managing-cache.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manage the Earthly cache

## Local cache
The cache lives in a docker (or podman) volume named `earthly-cache`, created when Earthly first starts its BuildKit daemon container (`earthly-buildkitd`). BuildKit garbage-collects old cache regularly.

Default size is `min(55%, max(10%, 20GB))`. Change it in the Earthly config:

```yaml
global:
  cache_size_mb: 30000
  cache_size_pct: 70
```

Check the current size:
```bash
sudo du -h /var/lib/docker/volumes/earthly-cache | tail -n 1
```

## Reset local cache
```bash
earthly prune
```
Manual alternative, only with the daemon not running:
```bash
docker stop earthly-buildkitd
docker rm earthly-buildkitd
docker volume rm earthly-cache
```
`earthly prune --reset` automates that.

## Remote runner or satellite
- Size: launch a bigger satellite with `earthly sat launch --size ...`. For a self-hosted runner, pass a BuildKit configuration (buildkitd.toml) to the BuildKit container to set the cache policy.
- Reset: `earthly prune` works on remote runners but without `--reset`, which is unsupported remotely. To restart a satellite with a fresh cache use `earthly sat update --drop-cache`.

## Auto-skip cache
It is global, stored in a cloud database; clear it with `earthly prune-auto-skip` (see the auto-skip skill for the `--path`, `--deep` and `--target` forms).

## Checked

2026-11-07. Read docs/caching/managing-cache.md in full. Default size formula, cache_size_mb/pct, prune and --reset, remote runner behaviour and auto-skip clearing match. Removed: the Gotcha about garbage collection and cache misses on Mac and Windows VMs (not on the page).
Method: documentation only; no commands were run.
