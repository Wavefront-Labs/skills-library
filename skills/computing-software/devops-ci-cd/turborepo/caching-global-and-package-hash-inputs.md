---
id: computing-software.devops-ci-cd.turborepo.caching-global-and-package-hash-inputs
name: caching-global-and-package-hash-inputs
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, global-hash, task-hash, globaldependencies, globalenv, passthrough-args, lockfile-changes, root-internal-dependencies, package-hash]
level: advanced
status: docs-checked
description: "The inputs that make up Turborepo's global hash and per-package task hash, such as lockfile changes, globalDependencies, globalEnv and passthrough arguments."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/caching.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo creates two hashes: a **global hash** and a **task hash**. If either changes, the task misses cache.

**Global hash inputs**
- Resolved task definition from root `turbo.json` and package `turbo.json` (for example changing `outputs`).
- Lockfile changes that affect the workspace root: updating dependencies in the root `package.json` makes **all** tasks miss.
- Source files in internal packages used by the workspace root: if the root depends on `@repo/tooling`, changing `packages/tooling/src/index.ts` makes **all** tasks miss.
- Contents of files in `globalDependencies` (for example `./.env`).
- Values of variables in `globalEnv` (for example `GITHUB_TOKEN`).
- Flag values that affect task runtime, such as `--cache-dir`, `--framework-inference`, `--env-mode`.
- Arbitrary passthrough arguments: `turbo build -- --arg=value` makes **all** tasks miss versus `turbo build` or `turbo build -- --arg=diff`, including dependencies of `build` that did not receive the argument.

**Root workspace dependencies.** Source files of every internal package that the root `package.json` depends on, directly or transitively, join the global hash. A change in an internal package outside that closure only changes relevant package and task hashes. With Git revisions, `turbo query affected --packages` reports this wide result using the `RootInternalDepChanged` reason.

**Package hash inputs**
- Package Configuration changes (the package's `turbo.json`).
- Lockfile changes that affect the package.
- Changes to the package's `package.json`, such as its `name`.
- File changes: defaults to all source-controlled files in the package directory, configurable with `inputs`.

Verify: compare two `--summarize` runs to see which hash input differed.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/caching); commands, flags, key names, defaults and example values were matched against it. Removed: nothing; every claim matched.

Method: documentation only; no commands were run.
