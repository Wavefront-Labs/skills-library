---
id: computing-software.software-engineering.pnpm.pnx-package-manager-or-runtime
name: pnx-package-manager-or-runtime
category: computing-software
field: software-engineering
product: pnpm
tags: [pnx-yarn, pnx-node, provisioned-tools, run-rust-release, pnx-npm-package, locating-specifier]
level: advanced
status: docs-checked
description: "In pnpm v12, pnx yarn@4, npm@11, bun@1.3.0, node@22 or --package=rust@channel provisions the real tool instead of the same-named npm package."
sources:
  - https://pnpm.io/cli/pnx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
pnpm v12 only (from v12.0.0-rc.6). Naming a package manager (`pnpm`, `npm`, `yarn`, `bun`) or runtime (`node`, `deno`, `bun`) provisions the real thing, because the same-named npm packages are a different line or a wrapper that downloads it. Yarn 4 is published as `@yarnpkg/cli-dist`, so `pnx yarn@4` runs Yarn 4 itself.

```sh
pnx yarn@4 install
pnx npm@11 ci
pnx bun@1.3.0 install
pnx node@22 --version
pnx --package npm@11 npx create-something   # pick which command of the manager
```

A specifier that locates a package rather than a released version installs what it names, unchanged:

```sh
pnx yarn@npm:yarn@1.22.22
pnx yarn@yarnpkg/berry
```

Rust (v12.11.1): `--package=rust@<channel>` installs that toolchain release into the store, then runs a tool from it. Channels are written as in `rust-toolchain.toml`; bare `rust` means `stable`.

```sh
pnx --package=rust@nightly-2026-01-01 cargo build --target wasm32-unknown-unknown
```

The release gets the profile, components and targets of the governing `rust-toolchain.toml`, plus the target of each `--target` argument.

## Checked

2026-11-04. Confirmed the package manager and runtime provisioning, the locating-specifier rule, --package behaviour and the Rust release section (v12.11.1) against pnpm.io/cli/pnx. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
