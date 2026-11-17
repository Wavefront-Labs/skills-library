---
id: computing-software.software-engineering.pnpm.add-dependency-types
name: add-dependency-types
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-add, save-dev, save-optional, save-exact, save-peer, tilde, save-types]
level: intro
status: docs-checked
description: "Add packages with pnpm add and choose where they land: dependencies, devDependencies, optional, peer, exact or tilde ranges, @types companions, global installs and workspace root."
sources:
  - https://pnpm.io/cli/add
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
| Command | Result |
|---|---|
| `pnpm add sax` | `dependencies` |
| `pnpm add -D sax` | `devDependencies` |
| `pnpm add -O sax` | `optionalDependencies` |
| `pnpm add sax@next` / `sax@3.0.0` | tag / exact version |
| `pnpm add -g sax` | global |

Version range options:
- `--save-exact`, `-E`: exact version.
- `--save-prefix <p>`: `^`, `~`, `=` (explicit exact) or empty string (bare exact); overrides `savePrefix`.
- `--tilde` (v12.6.0): same as `--save-prefix=~`.
- `--save-peer`: add to `peerDependencies` and install as dev dependency.
- `--save-types` (v12.6.0): also save `@types/*` to `devDependencies`, skipping packages with bundled types; `saveTypes: true` makes it default.

Gotchas:
- Adding to the workspace root fails unless you pass `--ignore-workspace-root-check` or `-w` (e.g. `pnpm add debug -w`).
- `--workspace` only adds a package that a workspace project provides, saved with `workspace:`; it never falls back to the registry.
- `pnpm add -g eslint,prettier` bundles packages into one isolated install; space-separated ones are isolated each.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/add: TL;DR table, --save-exact, --save-prefix, --tilde and --save-types (v12.6.0), --save-peer, workspace-root check, --workspace, comma-separated global bundling. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
