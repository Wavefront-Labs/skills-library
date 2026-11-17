---
id: computing-software.software-engineering.pnpm.migrate-from-v10
name: migrate-from-v10
category: computing-software
field: software-engineering
product: pnpm
tags: [migration, pnpm-v10-to-v11, codemod, settings-migration, ignore-ghsas, npm-config-rename, script-name-shadowing]
level: practitioner
status: docs-checked
description: "Migrate a project from pnpm v10 to v11 or v12: the pnpm-v10-to-v11 codemod, what it rewrites, and manual follow-ups for GHSA ids, env variables, Docker, link, removed commands."
sources:
  - https://pnpm.io/migration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```sh
cd /path/to/your/project
pnx codemod run pnpm-v10-to-v11     # pnpx on pnpm v10
```

v12 keeps the v11 changes; moving to pnpm 12 also needs the separate v11-to-12 guide.

Automated by the codemod:
- Moves `package.json#pnpm` settings into `pnpm-workspace.yaml`.
- Splits `.npmrc`: only auth and registry settings stay; others become camelCase keys in `pnpm-workspace.yaml` (per-subproject `.npmrc` goes under `packageConfigs["<project-name>"]`).
- Merges `onlyBuiltDependencies`, `neverBuiltDependencies`, `ignoredBuiltDependencies`, `onlyBuiltDependenciesFile` into `allowBuilds`.
- Collapses `managePackageManagerVersions`, `packageManagerStrict`, `packageManagerStrictVersion` into `pmOnFail`.
- Renames `allowNonAppliedPatches` to `allowUnusedPatches` and `auditConfig.ignoreCves` to `ignoreGhsas`.
- Turns `useNodeVersion` into `devEngines.runtime`; bumps `packageManager`.

Manual:
- Replace each `CVE-...` ignore with its `GHSA-...` id (shown in `pnpm audit`).
- `ignorePatchFailures` is gone; failed patches always throw.
- `executionEnv.nodeVersion` is gone; use the subpackage's `devEngines.runtime`.
- Rename `npm_config_*` environment variables to `pnpm_config_*` (CI, shells, Docker).
- Docker images must copy `pnpm-workspace.yaml` before `pnpm install`.
- `pnpm link <pkg-name>` no longer uses the global store; use a path (`pnpm link ./foo`).
- `pnpm install -g` without arguments is unsupported; `pnpm server` is removed.
- A script named like a built-in (`clean`, `deploy`) now shadows the command.

## Checked

2026-11-04. Confirmed against pnpm.io/migration: codemod command, automated changes (package.json#pnpm, .npmrc split, allowBuilds, pmOnFail, renames, useNodeVersion, packageManager), manual follow-ups, v11-to-12 note. Removed: the generic closing Check line (an unknown-setting-warnings claim not on the page).
Method: documentation only; no commands were run.
