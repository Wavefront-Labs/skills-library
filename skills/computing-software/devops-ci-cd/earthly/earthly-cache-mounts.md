---
id: computing-software.devops-ci-cd.earthly.earthly-cache-mounts
name: earthly-cache-mounts
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, cache-mounts, run-mount-type-cache, cache-command, sharing, locked, shared, private]
level: advanced
status: docs-checked
description: "Choose between RUN --mount type=cache and the CACHE command in Earthly, share mounts across targets with id, set sharing to locked, shared or private, and know the drawbacks."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/caching/caching-in-earthfiles.md
  - https://github.com/earthly/earthly/blob/main/docs/earthfile/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cache mounts in Earthfiles

Goal: persist a directory (package downloads, incremental compiler output) across builds when layer caching is not enough.

Two forms: `RUN --mount type=cache,target=/my-cache ...` and the `CACHE` command.

| | `RUN --mount type=cache` | `CACHE` |
|---|---|---|
| Scope | that single `RUN` | every following `RUN` in the same target |
| Final image | contents NOT persisted | contents copied into the image and visible to targets that inherit it (caching-in-earthfiles.md); features.md says the `--cache-persist-option` flag, on by default from VERSION 0.8, changes this so `CACHE` does not persist unless `--persist` is given |
| Performance | very performant, no transfer at the end | can be slow for large contents |
| Consistency | isolated to one command | shared by all commands, so easier to hit races with parallel builds |

## Sharing between targets
By default a cache mount is only available within the same target, so `target1` and `target2` using `target=/my-cache` do not share contents. Give it an `id` to make it global:

```Dockerfile
RUN --mount type=cache,id=my-cache-id,target=/my-cache ...
```

## Concurrency
Default sharing is `locked`: parallel executions wait for each other (safest, slowest; overusing global mounts limits build parallelism). Alternatives: `shared` (concurrent access) or `private` (a new empty mount is created if parallel execution occurs).

## Drawbacks stated by the docs
- Reusing prior state can hide inconsistency: a test may pass only because the cache already has the right contents.
- Do not use cache mounts to pass files between build steps; parallel builds (including different branches) can interfere. Extract results within the same operation so the cache stays locked.
- Mounts can grow indefinitely. Earthly garbage-collects least-recently-used layers and mounts, but a hot mount can still grow; clean unused files at the end of the same `RUN`.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: caching/caching-in-earthfiles.md, earthfile/features.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: added that from VERSION 0.8 `CACHE` does not persist its contents unless `--persist` is given (features.md), which contradicts the older table row; added features.md to sources.

Method: documentation only; no commands were run.
