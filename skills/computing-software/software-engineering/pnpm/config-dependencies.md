---
id: computing-software.software-engineering.pnpm.config-dependencies
name: config-dependencies
category: computing-software
field: software-engineering
product: pnpm
tags: [config-dependencies, pnpm-plugin, shared-config, add-config, config-dependency-update, boot-document-config, shared-patches]
level: advanced
status: docs-checked
description: "Share hooks, catalogs and patches across repos with configDependencies: adding, updating, plugin naming, optional platform binaries, exact versions and release-age handling."
sources:
  - https://pnpm.io/config-dependencies
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config dependencies install before regular dependencies, into `node_modules/.pnpm-config/<name>`, with integrity in the lockfile's boot document.

```sh
pnpm add --config my-configs
```

```yaml
configDependencies:
  my-configs: "^1.0.0"
patchedDependencies:
  react: "node_modules/.pnpm-config/my-patches/react.patch"
```

- Names matching `pnpm-plugin-*`, `@*/pnpm-plugin-*` or `@pnpm/plugin-*` auto-load `pnpmfile.mjs` (else `.cjs`) from the package root. Others can be imported from `.pnpmfile.mjs` by path.
- Pair with the `updateConfig` hook to inject settings or catalog entries, e.g. `config.catalogs.default['is-odd'] = '1.0.0'`, then `pnpm add is-odd@catalog:`.
- Must come from an npm registry and are verified against it, so an offline install of a new one needs cached metadata. `version+integrity` pins it; `minimumReleaseAge` applies to unpinned ones, and a hook-added exclude does not cover them. `bootConfig` (v12.15.0) sets a separate policy.
- No regular `dependencies`, no lifecycle scripts. `optionalDependencies` allowed one level deep, each with an exact version or `ERR_PNPM_CONFIG_DEP_OPTIONAL_NOT_EXACT`; only the host-matching variant installs.
- Since v12.12.0 `pnpm update` updates them (also `--latest` or by name); `--interactive`, `--patches`, `--no-save`, `--filter` and group flags skip them. Dist-tags keep tracking.
- Removing one drops its link and lockfile entries on the next non-frozen install.

## Checked

2026-11-04. Confirmed against pnpm.io/config-dependencies: install location and boot document, plugin naming auto-load, updateConfig catalog example, registry verification and minimumReleaseAge rules, bootConfig (v12.15.0), restrictions on dependencies and scripts, optionalDependencies exact-version error, update behaviour (v12.12.0), removal. Removed: the generic closing Check line (an ls command not on the page).
Method: documentation only; no commands were run.
