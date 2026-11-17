---
id: computing-software.software-engineering.pnpm.config-includes
name: config-includes
category: computing-software
field: software-engineering
product: pnpm
tags: [workspace-include, split-settings, setting-ownership, boot-config, codeowners-config, config-dependency-settings, delegated-settings]
level: sme
status: docs-checked
description: "Split pnpm-workspace.yaml settings across files and config dependencies with include (v12.15.0): delegation lists, ownership errors, write routing, pnpm.config and bootConfig."
sources:
  - https://pnpm.io/config-includes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```yaml
configDependencies:
  '@acme/pnpm-policy': 3.1.0
pnpmfile: []
include:
  ./config/security.yaml: '*'
  ./config/catalog.yaml: [catalog]
  '@acme/pnpm-policy': [minimumReleaseAge, trustPolicy]
```

- Only the root `pnpm-workspace.yaml` may define `include`. Sources are local `./` or `../` `.yaml`/`.yml` files (must exist, no globs, URLs or absolute paths) or a name from `configDependencies` (always needs a list).
- A list permits and reserves those settings for that source. `'*'` lets a local file define anything unowned; use it only for files as protected as the workspace file. Violations: `ERR_PNPM_SETTING_NOT_DELEGATED`, `ERR_PNPM_DUPLICATE_SETTING`, `ERR_PNPM_INVALID_WORKSPACE_INCLUDE`.
- Catalogs: `catalog` is the default one, `catalogs.<name>` one named catalog, `catalogs` all. Each has a single owner.
- Relative paths inside an included file are relative to that file (`patchedDependencies`, `patchesDir`, `file:` and `link:` in catalogs and overrides).
- Writes (`pnpm add` with catalog, `approve-builds`, `patch-commit`, `audit --fix`, `config set --location project`) go to the owning source; unowned settings go to `pnpm-workspace.yaml`. A config-dependency-owned setting fails with `ERR_PNPM_SETTING_OWNED_BY_CONFIG_DEPENDENCY`.
- A config dependency declares `"pnpm": { "config": "./config.yaml" }`. Not delegable to it: `configDependencies`, `pnpmfile`, `globalPnpmfile`, `bootConfig`, `packages`, `scriptShell`, path settings.
- `bootConfig` sets release-age and trust policy used while installing config dependencies and the `packageManager` pnpm.
- Protect the workspace file, `'*'` files and loaded pnpmfiles with CODEOWNERS or permissions.

## Checked

2026-11-04. Confirmed against pnpm.io/config-includes: include source rules, list versus '*' delegation, the three error codes, catalog ownership forms, relative path handling, write routing and ERR_PNPM_SETTING_OWNED_BY_CONFIG_DEPENDENCY, pnpm.config field, non-delegable settings, bootConfig, CODEOWNERS advice. Removed: the generic closing Check line (a pnpm config list claim not on the page).
Method: documentation only; no commands were run.
