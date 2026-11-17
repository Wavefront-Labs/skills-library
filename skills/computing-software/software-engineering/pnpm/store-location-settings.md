---
id: computing-software.software-engineering.pnpm.store-location-settings
name: store-location-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [store-dir, store-per-disk, frozen-store, store-index-format, verify-store-integrity, cache-dir, state-dir, store-trust]
level: advanced
status: docs-checked
description: "Place and protect the pnpm store: storeDir defaults and per-disk rule, read-only stores with frozenStore, storeIndexFormat files, integrity checks, cacheDir and stateDir."
sources:
  - https://pnpm.io/settings/store
  - https://pnpm.io/settings/other
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`storeDir` default: `$PNPM_HOME/store`, else `$XDG_DATA_HOME/pnpm/store`, else `~/AppData/Local/pnpm/store` (Windows), `~/Library/pnpm/store` (macOS), `~/.local/share/pnpm/store` (Linux).

- Keep the store on the same disk as the project: one store per disk, created in the home directory on that disk or at the disk root (`/mnt/.pnpm-store`). A store on another disk means copying instead of hard links. If no ancestor directory accepts a hard link (sandbox, container), the store goes to `node_modules/.pnpm-store`.
- Process locks live in a per-user directory: `$XDG_RUNTIME_DIR` when usable, else `/tmp` (Windows `~/AppData/Local`). Processes sharing a store should see the same value.
- The store is a trust domain: share it only between mutually trusted users and protect it with permissions. `verifyStoreIntegrity` (true) detects accidental corruption only. `strictStorePkgContentCheck` (true) can be set false for registries that publish identical content under different names.
- `frozenStore` runs installs against a read-only store (Nix, bind mount, image layer): `pnpm install --frozen-store --offline --frozen-lockfile`. The store must hold everything, including approved build outputs, else `ERR_PNPM_FROZEN_STORE_NEEDS_BUILD`. Incompatible with `--force` and a pnpr server; no other process may modify the store.
- `storeIndexFormat` (v12.13.0): `sqlite` (default, local disk) or `files` (one file per package, for network filesystems shared by CI jobs). The store keeps whichever format was first written; switch back by deleting its `index` directory. pnpm v11 reads only `index.db`.
- `cacheDir` (package metadata, dlx cache, some install verification results) and `stateDir` (update checker, task slot files) have per-OS defaults; `stateDir` is global-config or CLI only.

## Checked

2026-11-04. Confirmed storeDir defaults and the per-disk rule, lock directory, trust-domain note, verifyStoreIntegrity, strictStorePkgContentCheck, frozenStore, storeIndexFormat (v12.13.0), cacheDir and stateDir against pnpm.io/settings/store and pnpm.io/settings/other. Aligned the cacheDir wording with the page. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
