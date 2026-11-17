---
id: computing-software.software-engineering.pnpm.node-modules-settings
name: node-modules-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [node-linker, hoisted-linker, pnp-linker, package-import-method, virtual-store-dir, modules-dir, virtual-store-only, modules-cache-max-age, dlx-cache-max-age, node-package-map]
level: practitioner
status: docs-checked
description: "Choose pnpm node_modules layout settings: nodeLinker isolated, hoisted or pnp, packageImportMethod and its auto order, virtualStoreDir, path-length limits and cache ages."
sources:
  - https://pnpm.io/settings/node-modules
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In `pnpm-workspace.yaml`:

- `nodeLinker`: `isolated` (default, symlinks from `node_modules/.pnpm`), `hoisted` (flat, no symlinks, for symlink-averse tooling, serverless hosts, `bundledDependencies`, `--preserve-symlinks`), `pnp` (no `node_modules`; also set `symlink: false`), or experimental `loaded`.
- `packageImportMethod`: `auto` (default), `hardlink`, `copy`, `clone`, `clone-or-copy`. `auto` order is hardlink, clone, copy on Linux; clone, hardlink, copy on macOS and Windows. It steps down only when a link fails, not when it is slow (overlayfs image layers, NFS/SMB, virtiofs): measure `copy` there. Use `clone` if you edit files in `node_modules`, since a hardlink edits the store file. Packages that scripts or patches will write are imported with `clone-or-copy`.
- `virtualStoreDir` (default `node_modules/.pnpm`) and `virtualStoreDirMaxLength` (120 Linux/macOS, 60 Windows): shorten for Windows long-path problems.
- `virtualStoreOnly`: populate the virtual store only; `pnpm fetch` uses it.
- `modulesDir`, `enableModulesDir` (false for FUSE), `symlink`.
- `modulesCacheMaxAge` (default 10080 minutes): keeps orphan packages for branch switching. `dlxCacheMaxAge` (default 1440 minutes): pnx cache expiry.
- `nodePackageMap.mode` (`off`, `write-only`, `load`; v12.13.0) writes `node_modules/.package-map.json`; `type` is `standard` or `loose`.
- macOS writes files with 4 threads; `PNPM_MACOS_LINK_THREADS=0` uses the normal thread count (helps with endpoint-security software).

## Checked

2026-11-04. Confirmed nodeLinker values, packageImportMethod and its auto order, virtualStoreDir and virtualStoreDirMaxLength, virtualStoreOnly, cache ages, nodePackageMap and the macOS thread note against pnpm.io/settings/node-modules. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
