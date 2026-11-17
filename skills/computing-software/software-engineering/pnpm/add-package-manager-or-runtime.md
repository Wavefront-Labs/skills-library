---
id: computing-software.software-engineering.pnpm.add-package-manager-or-runtime
name: add-package-manager-or-runtime
category: computing-software
field: software-engineering
product: pnpm
tags: [add-package-manager, add-runtime, dev-engines, engines-runtime, rust-toolchain]
level: advanced
status: docs-checked
description: "In pnpm v12, pnpm add yarn, npm, bun, node, deno or rust records a package manager or runtime in the manifest instead of installing the npm package of that name."
sources:
  - https://pnpm.io/cli/add
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm v12 only (from v12.0.0-rc.6). Naming a package manager records which one the project uses:

```sh
pnpm add yarn@4     # writes "packageManager": "yarn@4.18.0"
```

- npm and Bun are recorded as a range in `devEngines.packageManager` instead. Each write removes the other field.
- Runtimes (`node`, `deno`) go under `engines.runtime`; the explicit `node@tool:22` spelling does the same (v12.13.0).
- `bun` is both; it is declared as package manager unless you ask for the runtime: `pnpm add bun@tool:1.3.0`.
- Globally: `pnpm add -g yarn` installs the current Yarn line, and `pnpm add -g node@22` installs that Node release.
- To install the real npm package, use a locating specifier such as `pnpm add yarn@npm:yarn@1.22.22`; it becomes an ordinary dependency.

Rust (v12.11.0): `rust` means the toolchain. `pnpm add rust@1.95` pins `channel` in the nearest `rust-toolchain.toml` (creating one if none), nothing goes into `package.json`. Channels: a version, `stable`, `beta`, `nightly`, or dated `nightly-YYYY-MM-DD`. `pnpm add -g rust@stable` installs globally.

## Checked

2026-11-04. Confirmed against pnpm.io/cli/add: v12.0.0-rc.6 package-manager and runtime behaviour, node@tool:22 (v12.13.0), bun@tool:1.3.0, global installs, locating specifiers, Rust toolchain section (v12.11.0). Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
