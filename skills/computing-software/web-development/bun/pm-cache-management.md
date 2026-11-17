---
id: computing-software.web-development.bun.pm-cache-management
name: pm-cache-management
category: computing-software
field: web-development
product: bun
tags: [bun-pm-cache, cache-prune, cache-pack, bun-pm-fetch]
level: advanced
status: docs-checked
description: "Manage Bun's package cache: print the path, prune old entries, pack and unpack the cache for CI, pre-fetch dependencies, and avoid deleting the global store by accident."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/pm.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun pm cache                       # print cache path
bun pm cache rm --dry-run          # list what would be deleted
bun pm cache prune --max-age 14    # default: older than 30 days
bun pm cache pack cache.bin        # save entries the lockfile needs (for CI caching)
bun pm cache unpack cache.bin      # add missing entries, no overwrite
bun pm fetch --os linux --cpu x64  # download all deps to cache, no node_modules
```

Gotchas:
- `bun pm cache rm` deletes the whole cache including the global store at `<cache>/links/`; projects using `globalStore = true` must run `bun install` again. Removing a single package is an error.
- Prune age is time since download, or since last install where the filesystem records access times; pruned packages re-download, which matters for `--offline`.
- Packs are uncompressed, platform-specific, and should be regenerated after a Bun upgrade. Bun trusts its cache: packs detect damage, not tampering, so unpack only files you made.
- Cache location comes from `$BUN_INSTALL_CACHE_DIR`, `--cache-dir` or `$BUN_INSTALL`; for deletion, bunfig/.npmrc/.env settings are ignored, so use `--cache-dir`.
- `bun pm fetch` in monorepos needs only root `package.json` and lockfile; copy `bunfig.toml`/`.npmrc` if they set a registry or cache keys will not match.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/pm.mdx: bun pm cache, rm and rm --dry-run, prune with --max-age and 30-day default, pack and unpack semantics and warning, cache-dir resolution rules, bun pm fetch flags and monorepo notes, global store deletion caveat.

Method: documentation only; no commands were run.
