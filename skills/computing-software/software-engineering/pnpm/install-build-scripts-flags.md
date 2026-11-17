---
id: computing-software.software-engineering.pnpm.install-build-scripts-flags
name: install-build-scripts-flags
category: computing-software
field: software-engineering
product: pnpm
tags: [allow-build, ignore-scripts, ignore-pnpmfile, shamefully-hoist, node-linker-flag, reporter]
level: practitioner
status: docs-checked
description: "Use pnpm install flags that change execution: --allow-build and !deny, --ignore-scripts, --ignore-pnpmfile, --node-linker, --shamefully-hoist, --frozen-store and --reporter."
sources:
  - https://pnpm.io/cli/install
  - https://pnpm.io/cli/add
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
pnpm install --allow-build=esbuild --allow-build='!core-js'
pnpm add --allow-build=esbuild my-bundler
```

`--allow-build` lets the named package run lifecycle scripts and records it in `allowBuilds` in `pnpm-workspace.yaml` (`esbuild: true`; a `!` prefix writes `false`, i.e. denied). Install option since v12.7.0; the `add` form with `!` since v12.4.0. Quote `!` in POSIX shells; leave quotes out in Windows `cmd.exe`.

Other flags:
- `--ignore-scripts`: run no scripts from the project or dependencies; `--no-ignore-scripts` overrides the setting.
- `--ignore-pnpmfile`: skip `.pnpmfile.cjs` hooks, including config-dependency pnpmfiles.
- `--node-linker isolated|hoisted|pnp`: override `nodeLinker` for one install.
- `--shamefully-hoist`: flat `node_modules` like npm; docs say highly discouraged.
- `--frozen-store`: read-only store for read-only filesystems; combine with `--offline --frozen-lockfile`.
- `--reporter default|append-only|ndjson|silent`: default is `default` on a TTY, `append-only` otherwise; `silent` hides even fatal errors.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/install and pnpm.io/cli/add: --allow-build (v12.7.0; add form with ! since v12.4.0), quoting note, --ignore-scripts, --no-ignore-scripts, --ignore-pnpmfile, --node-linker, --shamefully-hoist, --frozen-store, --reporter values and defaults. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
