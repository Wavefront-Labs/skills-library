---
id: computing-software.software-engineering.pnpm.configuration-files-and-env
name: configuration-files-and-env
category: computing-software
field: software-engineering
product: pnpm
tags: [pnpm-config, config-yaml, global-config, pnpm-config-env, project-only-settings, npm-config-ignored, settings-location]
level: intro
status: docs-checked
description: "Know where pnpm reads settings: pnpm-workspace.yaml, global config.yaml per OS, project-only settings, pnpm_config_ environment variables and why npm_config_ ones are ignored."
sources:
  - https://pnpm.io/configuring
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two categories:

- Authentication and certificate settings live in INI files (not committed).
- Everything else is YAML: project `pnpm-workspace.yaml` and global `config.yaml`.

The `pnpm` field of `package.json` is ignored with a warning.

Global `config.yaml` location, first match:
1. `$XDG_CONFIG_HOME/pnpm/config.yaml` when set
2. Windows: `%LOCALAPPDATA%\pnpm\config\config.yaml`
3. macOS: `~/Library/Preferences/pnpm/config.yaml`
4. Linux: `~/.config/pnpm/config.yaml`

Machine-wide settings (`storeDir`, `cacheDir`, `packageImportMethod`, `minimumReleaseAge`, network) may go global. Structure settings (`nodeLinker`, `hoistPattern`, `publicHoistPattern`, `shamefullyHoist`, `linkWorkspacePackages`) are project-only so every machine installs alike. `pnpm config set --global` refuses them with `ERR_PNPM_CONFIG_SET_UNSUPPORTED_YAML_CONFIG_KEY`; hand-written ones are warned about and ignored. Share project-only settings through a config dependency.

`pnpm login` saves tokens in `config.yaml`; other global auth settings go in `auth.ini` beside it.

Environment: `pnpm_config_<name>` (or `PNPM_CONFIG_`) overrides `pnpm-workspace.yaml` but not CLI arguments, e.g. `pnpm_config_save_exact=true pnpm add foo`. `npm_config_*` is not read, except `NPM_CONFIG_WORKSPACE_DIR`, `npm_config_userconfig` and URL-scoped credentials such as `npm_config_//registry.example.com/:_authToken`.

## Checked

2026-11-04. Confirmed against pnpm.io/configuring: INI versus YAML split, package.json pnpm field ignored, config.yaml locations in order, global versus project-only settings, ERR_PNPM_CONFIG_SET_UNSUPPORTED_YAML_CONFIG_KEY, pnpm login and auth.ini, pnpm_config_ environment rules and the npm_config_ exceptions. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
