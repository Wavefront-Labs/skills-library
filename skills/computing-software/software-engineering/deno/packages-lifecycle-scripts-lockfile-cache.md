---
id: computing-software.software-engineering.deno.packages-lifecycle-scripts-lockfile-cache
name: packages-lifecycle-scripts-lockfile-cache
category: computing-software
field: software-engineering
product: deno
tags: [packages, lifecycle-scripts, allow-scripts, deno-ci, lockfile, reload, cached-only]
level: practitioner
status: docs-checked
description: "Opt in to npm install scripts, reproducible installs with deno.lock and deno ci, and cache control with --reload and --cached-only."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Lifecycle scripts: unlike npm, Deno does not run `preinstall`/`postinstall` scripts by default. Allow one explicitly, or approve interactively; scripts only execute when a `node_modules` directory is in use.

```sh
deno install --allow-scripts=npm:better-sqlite3
deno approve-scripts
```

Lockfile: Deno maintains `deno.lock` with each dependency's exact version and integrity hash, verified on later runs. Commit it. In CI and production use `deno ci`, which errors if `deno.lock` is missing or stale rather than resolving new versions:

```sh
deno ci          # like npm ci
deno ci --prod   # additionally skip devDependencies
```

Enforce a frozen lockfile on any command with `--frozen`.

Cache: downloads go to a global cache (`DENO_DIR`) shared across projects. A local `node_modules` is created only if the project has a `package.json` (see `nodeModulesDir`).

```bash
deno run --reload my_module.ts            # refetch everything
deno run --reload=jsr:@std/fs my_module.ts  # refetch one module
deno run --cached-only mod.ts             # forbid network; fail if not cached
```

`--cached-only` suits offline work and reproducible CI.

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: lifecycle scripts opt-in and `--allow-scripts`, `deno approve-scripts`, `deno.lock`, `deno ci` and `--prod`, `--frozen`, global cache, `--reload` and `--cached-only`. Nothing removed.

Method: documentation only; no commands were run.
