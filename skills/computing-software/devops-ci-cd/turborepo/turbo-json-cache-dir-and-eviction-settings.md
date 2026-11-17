---
id: computing-software.devops-ci-cd.turborepo.turbo-json-cache-dir-and-eviction-settings
name: turbo-json-cache-dir-and-eviction-settings
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, cachedir, cachemaxage, cachemaxsize, cache-eviction, local-cache-size, turbo-cache-max-age, package-manager-check-opt-out]
level: advanced
status: docs-checked
description: "Set the local cache directory and opt in to age and size eviction with cacheMaxAge and cacheMaxSize; also the package manager check opt-out."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`cacheDir`** (default `.turbo/cache`): the filesystem cache directory. With no `cacheDir` in a Git worktree, Turborepo shares the cache with the main worktree. An explicit relative `cacheDir` such as `.turbo/cache` resolves from the current worktree root and disables sharing, which matters because outputs containing absolute worktree paths can otherwise point at another checkout.

**`cacheMaxAge`** (default `"0"`, disabled): maximum age of local cache entries. Eviction runs in a background thread at the start of each `turbo run`, so it does not block tasks. Units: `s`, `m`, `h`, `d`, `w` (for example `30s`, `5m`, `24h`, `7d`, `2w`). Example: `"cacheMaxAge": "7d"`. Also settable with `TURBO_CACHE_MAX_AGE`.

**`cacheMaxSize`** (default `"0"`, disabled): maximum total size; the oldest entries are evicted until under the limit. Units (case-insensitive): `MB`, `GB`, `TB`, with fractions allowed, like `1.5GB`. Example: `"cacheMaxSize": "10GB"`. Also settable with `TURBO_CACHE_MAX_SIZE`. Size eviction runs after age eviction when both are set.

Local cache eviction is opt-in today; the docs expect to enable it by default in Turborepo 3.0.

**`dangerouslyDisablePackageManagerCheck`** (default `false`): Turborepo uses the lockfile for caching and Package Graphs, so it relies on the package manager declaration in your root `package.json` (`devEngines.packageManager` recommended, legacy `packageManager` supported). Opt out during migration, accepting unpredictable behaviour from unstable lockfiles; Turborepo then discovers the package manager best-effort. Alternatives: a CLI flag or `TURBO_DANGEROUSLY_DISABLE_PACKAGE_MANAGER_CHECK`.

## Checked

2026-11-04. Read the `cacheDir`, `cacheMaxAge`, `cacheMaxSize` and `dangerouslyDisablePackageManagerCheck` entries of the configuration reference in full; defaults, units, env vars, ordering and the 3.0 note match. Removed the invented Verify step.

Method: documentation only; no commands were run.
