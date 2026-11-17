---
id: computing-software.web-development.bun.isolated-installs
name: isolated-installs
category: computing-software
field: web-development
product: bun
tags: [isolated-linker, hoisted-linker, phantom-dependencies, config-version]
level: advanced
status: docs-checked
description: "Choose between the isolated and hoisted linkers: defaults by configVersion, node_modules layout, hoist settings, switching and migration steps, and compatibility problems."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/isolated-installs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```toml
[install]
linker = "isolated"   # or "hoisted"
hoist = false         # no .bun/node_modules fallback
```
CLI: `bun install --linker isolated|hoisted`; `--force` rebuilds every store entry; `bun prune` removes unreferenced store entries.

Defaults: configVersion 1 with workspaces gives isolated; configVersion 1 without workspaces gives hoisted; configVersion 0 is hoisted. New projects get 1; lockfiles without a version get 0 (pre-v1.3.2 projects). Migrating from pnpm yields 1, from npm or Yarn 0.

Layout: store entries live in `node_modules/.bun/<name>@<ver>/node_modules/` with one symlink per dependency; top-level entries are symlinks into the store.

Gotchas:
- Phantom dependencies still leak by default via the fallback; set `hoist = false` (root `node_modules` stays visible).
- Switching linkers reinstalls from scratch (old tree moves to `node_modules/.old_modules-<random>`).
- Tools that hardcode flat `node_modules` paths break; use `--linker hoisted`.
- Windows: long store paths can break lifecycle scripts (260 character limit).
- From npm or Yarn: remove `node_modules` and old lockfiles, run `bun install --linker isolated`.

## Checked

2026-11-04. Confirmed against bun docs pm/isolated-installs.mdx: linker flag and bunfig key, configVersion defaults and migration values, store layout, hoist = false caveat, linker switching and .old_modules, bun install --force and bun prune, 260-character Windows path note, migration steps.

Method: documentation only; no commands were run.
