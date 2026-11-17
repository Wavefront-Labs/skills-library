---
id: computing-software.systems-network-administration.restic.local-cache
name: local-cache
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, cache, cache-dir, no-cache, performance]
level: practitioner
status: docs-checked
description: "Understand the restic local cache layout per repository ID, relocate it with RESTIC_CACHE_DIR, and clear stale cache directories."
sources:
  - https://raw.githubusercontent.com/restic/restic/master/doc/cache.rst
  - https://raw.githubusercontent.com/restic/restic/master/doc/075_scripting.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local cache

Restic keeps a local cache to speed up operations, especially on remote backends.

## Layout

- Each repository gets its own cache subdirectory named by the repository ID (assigned at `init`).
- Inside, snapshot, data and index files are cached as read from the repository, in the sub-directories `snapshots`, `data` and `index`.
- Caches for different repositories are independent.

The default location depends on the operating system and environment. `RESTIC_CACHE_DIR` sets the cache directory.

## Expiry

Using a cache updates its directory's modification time. Looking at those timestamps shows which cache directories have not been used for a long time; those are probably stale and can be removed.

## Checked

2026-11-08. Claims were read against: https://raw.githubusercontent.com/restic/restic/master/doc/cache.rst, https://raw.githubusercontent.com/restic/restic/master/doc/075_scripting.rst.

Method: documentation only; no commands were run.
