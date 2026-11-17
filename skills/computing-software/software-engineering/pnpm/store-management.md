---
id: computing-software.software-engineering.pnpm.store-management
name: store-management
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-store, store-prune, store-status, store-path, store-add, unreferenced-packages, store-projects-registry]
level: practitioner
status: docs-checked
description: "Maintain the pnpm store: store status, add, path and prune, what prune removes (unreferenced packages, metadata and pnx caches), global virtual store sweeping, projects registry."
sources:
  - https://pnpm.io/cli/store
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm store path                # active store directory
pnpm store status              # verify lockfile packages unmodified in store
pnpm store add express@4       # add to store only, no project files change
pnpm store prune
```

- `status`: exit 0 if package contents match what was unpacked; otherwise `ERR_PNPM_MODIFIED_DEPENDENCY` listing modified packages.
- `prune` removes unreferenced packages (not used by any project on the system). It is harmless: removed packages are re-downloaded if needed. Run occasionally, not too often, since switching to a branch with older dependencies re-downloads them.
- Before pruning, pnpm deletes expired `pnx` cache entries (`dlxCacheMaxAge`), because they hold hard links into the store. It also removes the `metadata*` directories in the cache directory, such as `v12/metadata`; other caches stay.
- Undecodable index entries are kept and counted in the summary.
- Since v12.7.0 prune also removes private copies of pnpm or a runtime left by a killed process.
- With `enableGlobalVirtualStore`, prune also does mark-and-sweep on the `links/` directory using the registered projects; if no project links into it, it is unchanged.
- `pnpm install` registers the project as a symlink in `"$(pnpm store path)/projects"`; not written with `--frozen-store`, `enableModulesDir: false`, `--lockfile-only` or `--dry-run`.

## Checked

2026-11-04. Confirmed status, add, prune and path behaviour, the pnx cache and metadata cleanup, undecodable entries, v12.7.0 private-copy removal, global virtual store sweep and the projects registry against pnpm.io/cli/store. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
