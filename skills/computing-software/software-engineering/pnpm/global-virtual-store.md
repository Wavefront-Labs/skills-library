---
id: computing-software.software-engineering.pnpm.global-virtual-store
name: global-virtual-store
category: computing-software
field: software-engineering
product: pnpm
tags: [global-virtual-store, virtual-store-type, enable-global-virtual-store, global-virtual-store-dir, worktree-node-modules, dependency-graph-hash]
level: advanced
status: docs-checked
description: "Share one pnpm virtual store across all projects with virtualStoreType global: layout, graph-hash identity, when it helps, CI and trust limits, NODE_PATH and ESM hoisting."
sources:
  - https://pnpm.io/global-virtual-store
  - https://pnpm.io/settings/node-modules
  - https://pnpm.io/settings/peer-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
virtualStoreType: global     # same as enableGlobalVirtualStore: true; type project | global
```

- Default layout: every project has `node_modules/.pnpm` with hardlinks to the content-addressable store. With the global virtual store, each project's `node_modules` holds only symlinks into `<store-path>/links/` (or `globalVirtualStoreDir`, else an explicit `virtualStoreDir`). The project's `.pnpm` keeps only its current lockfile and hidden hoisted dependencies.
- Each package directory is named by a hash of its dependency graph, so projects with the same tree share one directory; different peers give separate entries (like Nix).
- Best for many checkouts of one project (git worktrees) and for speed across unrelated projects with a warm store. In CI it is generally not useful because caches are absent and it may be slower.
- It is shared writable state: use only among mutually trusting users and jobs; protect the path.
- Hoisting relies on `NODE_PATH`; Node ignores it for ESM, so pnpm adds a `NODE_OPTIONS --import` resolve hook to processes it spawns. A `node` started outside pnpm, or `extendNodePath: false`, loses it; declare missing dependencies with `packageExtensions`.
- Disabled and experimental for project installs; on by default for `pnpm add -g`; `pnx` entries keep their own virtual store. It works with `nodeLinker` isolated or pnp, and `hoisted` ignores it.
- `addMissingPeerTypes` helps TypeScript find types here.

## Checked

2026-11-04. Confirmed against pnpm.io/global-virtual-store, pnpm.io/settings/node-modules and pnpm.io/settings/peer-dependencies: default versus global layout, hash-named directories, best-use and CI guidance, shared-trust warning, NODE_PATH/ESM hoisting caveat, experimental status, global installs and pnx, linker independence, globalVirtualStoreDir/virtualStoreDir location, addMissingPeerTypes. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
