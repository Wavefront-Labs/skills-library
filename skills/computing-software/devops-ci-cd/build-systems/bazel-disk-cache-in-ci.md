---
id: computing-software.devops-ci-cd.build-systems.bazel-disk-cache-in-ci
name: bazel-disk-cache-in-ci
category: computing-software
field: devops-ci-cd
product: build-systems
tags: [build-systems, disk-cache, bazel, bazel-disk-cache, repository-cache, ci-cache, actions-cache]
level: practitioner
status: docs-checked
description: "Use Bazel's --disk_cache and --repository_cache in CI: what each stores, persisting them with CI caches, size management, combining with a remote cache, and key strategies."
sources: ["https://bazel.build/remote/caching#disk-cache", "https://bazel.build/reference/command-line-reference#flag--disk_cache", "https://bazel.build/remote/output-directories", "https://github.com/bazel-contrib/setup-bazel"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bazel disk cache in CI

Ephemeral CI runners start with an empty output base, so every job rebuilds everything unless something persists. Without a remote cache, the disk cache plus repository cache saved by the CI system is the next best thing.

## What each cache holds
| Flag | Contents |
|---|---|
| `--disk_cache=<dir>` | action cache and outputs, a directory Bazel reads and writes; works across workspaces and checkouts. With no value it uses `<outputUserRoot>/cache/disk` |
| `--repository_cache=<dir>` | downloaded external archives, avoiding refetching dependencies |
| output base (under `outputRoot/_bazel_$USER`, `~/.cache/bazel` by default on Linux) | everything including analysis state; huge, path-dependent; don't cache it |

## Configure
```
# .bazelrc
build:ci --disk_cache=~/.cache/bazel-disk
build:ci --repository_cache=~/.cache/bazel-repo
build:ci --disk_cache_gc_max_size=10G      # garbage-collect the disk cache while the server is idle
build:ci --disk_cache_gc_max_age=14d
```
Automatic disk-cache garbage collection arrived in Bazel 7.4 under the names `--experimental_disk_cache_gc_max_size` and `--experimental_disk_cache_gc_max_age` (the current source accepts the shorter names and keeps the old ones as aliases); collection runs after the server has been idle for `--disk_cache_gc_idle_delay` (default 5 minutes). On older Bazel versions, or if you prefer on-demand cleanup, the Bazel repository ships a disk cache garbage collection tool (`src/tools/diskcache`).

## GitHub Actions
```yaml
- uses: bazel-contrib/setup-bazel@0.19.1
  with:
    bazelisk-cache: true
    disk-cache: ${{ github.workflow }}          # key to separate caches per workflow
    repository-cache: true
    cache-save: ${{ github.event_name != 'pull_request' }}   # PRs restore but do not save
- run: bazel test //...
```
`bazelisk-cache` caches Bazelisk downloads keyed on `.bazelversion`. The action also has an `external-cache` input (caches `external/` repositories, keyed on `MODULE.bazel` and `WORKSPACE`).
Manual alternative with `actions/cache`: a rolling key (`${{ runner.os }}-bazel-${{ github.sha }}` with `restore-keys: ${{ runner.os }}-bazel-`) so each run restores the latest and saves an updated copy.

## Trade-offs
- Restore/save time grows with cache size; large caches favour a remote cache (bazel-remote, BuildBuddy, EngFlow, Buildbarn), which transfers only the blobs needed.
- GitHub's default cache limit is 10 GB per repository (configurable), unaccessed entries are removed after 7 days; keep separate caches per OS/architecture.
- Disk cache plus remote cache is a supported combination.
- Save only from main-branch jobs so PR jobs do not pollute or evict the useful cache (`cache-save` above, or `actions/cache/save` with an `if:`).

## Diagnose hit rates
Bazel's build summary reports counts such as `N processes: M disk cache hit, ...`; compare them across runs.
Low hit rates across runs usually mean non-deterministic actions or environment differences (`--action_env`, `--stamp` on every build - stamp release builds only; `--incompatible_strict_action_env` is on by default in current Bazel).

## Verify
- [ ] The second CI run on an unchanged commit shows mostly disk cache hits and much shorter wall time.
- [ ] Cache size stays bounded over weeks.

## Checked
Date: 2026-10-25. Documentation: Bazel `docs/remote/caching.mdx` and `output-directories.mdx` and option definitions in `RemoteOptions.java` (bazelbuild/bazel, default branch); bazel-contrib/setup-bazel README (release 0.19.1); GitHub's dependency-caching reference.
Confirmed: `--disk_cache` semantics and default location; disk-cache GC flags (documented as `--experimental_disk_cache_gc_*` since Bazel 7.4, renamed in source with the old names kept), idle delay default 5m, diskcache tool; setup-bazel inputs `bazelisk-cache`, `disk-cache`, `repository-cache`, `external-cache`, `cache-save`; output root layout; GitHub cache limits.
Fixed: GC flag names; the setup-bazel version (0.9.0 replaced by 0.19.1).
Removed: the `find ... -atime ... -delete` prune command, the `MODULE.bazel.lock`-keyed manual cache recipe, the `grep` log-parsing command and example output line, and "Bazel checks disk first, then remote" ordering detail (not stated in the pages read). `--repository_cache` is described only by its documented purpose.
Method: documentation only; no commands were run.
