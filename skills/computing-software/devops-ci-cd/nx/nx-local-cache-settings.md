---
id: computing-software.devops-ci-cd.nx.nx-local-cache-settings
name: nx-local-cache-settings
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, cache, maxcachesize, cachedirectory, parallel, defaultbase]
level: practitioner
status: docs-checked
description: "nx.json root options for the local cache and task running: maxCacheSize, cacheDirectory, parallel, defaultBase, skipping the cache, nxCloudEncryptionKey."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/environment-variables.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/kb/change-cache-location.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size, relocate, or bypass the local Nx cache and set run-wide defaults in `nx.json`.

Root properties:
- `parallel`: max targets run in parallel (CLI: `--parallel=5`).
- `cacheDirectory`: where the local cache lives; default `~/.nx/<id>/cache`, shared by every checkout of the workspace. Example: `"cacheDirectory": "tmp/my-nx-cache"`.
- `defaultBase`: base branch for affected calculations, default `main`. (`affected.defaultBase` is deprecated.)
- `nxCloudEncryptionKey`: end-to-end encryption key for the cloud cache (only when connected); env var `NX_CLOUD_ENCRYPTION_KEY` also works, any key length accepted.
- `nxCloudId` / `nxCloudUrl`: connect to Nx Cloud (default URL `https://cloud.nx.app`).

`maxCacheSize`:
- Default (unset): 10% of the disk holding the cache, capped at 10GB.
- Accepts bytes or units: `819200`, `"100MB"`, `"1GB"`; `0` disables the limit.
- Over the limit, Nx deletes least-recently-used entries until under 90% of the limit.
- `NX_MAX_CACHE_SIZE` env var (same units) takes precedence over `nx.json`.
- Regardless of size, entries not accessed in 7 days are removed.

```json
{ "maxCacheSize": "10GB", "cacheDirectory": "tmp/my-nx-cache", "parallel": 4 }
```

Skipping: pass `--skip-nx-cache` (alias `--disableNxCache`) for one run; there is no root `nx.json` property for it. `NX_SKIP_REMOTE_CACHE` disables all remote caching (Nx Cloud and self-hosted). `nx reset` clears the cache directory for the workspace (nx-cache-location).

Note: the page's `maxCacheSize` JSON examples use quoted strings (`"0"`, `"10GB"`); its value table also lists bare byte counts such as `819200`.

## Checked

2026-11-07. Confirmed: parallel, cacheDirectory, defaultBase, nxCloudEncryptionKey, maxCacheSize units, defaults, 90% and 7-day rules and --skip-nx-cache against the nx.json reference; NX_SKIP_REMOTE_CACHE against Environment variables and nx reset against Change cache location (both added to sources). Removed: the unconfirmed --skipRemoteCache flag (replaced by the NX_SKIP_REMOTE_CACHE variable) and an invented Verify step.

Method: documentation only; no commands were run.
