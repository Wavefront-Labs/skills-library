---
id: computing-software.software-engineering.pnpm.project-aware-global-bins
name: project-aware-global-bins
category: computing-software
field: software-engineering
product: pnpm
tags: [project-aware-shims, global-shims, nvmrc, node-version-file, shim-bypass, shim-trust, pnpm-shim-add]
level: advanced
status: docs-checked
description: "Use pnpm v12 project-aware global commands: node follows devEngines.runtime, .node-version or .nvmrc, trust prompts, globalShims, package manager pins, PNPM_SHIM_BYPASS."
sources:
  - https://pnpm.io/global-packages
  - https://pnpm.io/settings/other
  - https://pnpm.io/settings/other
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Added in v12.0.0-rc.2 (not in v11). A global command run inside a project uses the version that project asks for; no shell hooks.

Version choice walks up from the working directory to the nearest project providing the command:
- Runtimes (`node`, `deno`, `bun`): only `devEngines.runtime`, then `engines.runtime` count. For `node`, v12.7.0 also reads `.node-version` or `.nvmrc` (accepts `v` prefix, `node`, `stable`, `lts/*`, codenames; `system`, `default` and custom aliases are ignored). In one directory `package.json` beats `.node-version` beats `.nvmrc`. The pinned version downloads on demand; `node_modules/.bin` is never consulted for a runtime.
- Package managers (`npm`, `yarn`, `bun`; rc.6): the `packageManager` or `devEngines.packageManager` pin, which outranks a global copy.
- Anything else: the project's `node_modules/.bin/<name>`, and only if it comes from the same package as the global one.
- Directories inside the pnpm home are skipped; if nothing matches the global version runs.

Trust under `auto`: stable Node.js (signature-verified) and registry-signed package manager pins switch silently; Deno, Bun, Node prereleases and other packages ask once per project and binary fingerprint. Non-interactive sessions run the global version and record nothing.

`globalShims` policies per providing package: `auto`/`true`, `prompt`, `always` (works in CI), `false`; scalars `false` (all off) and `true` (reset). Read only from global `config.yaml`, the pnpm home's `pnpm-workspace.yaml`, or `PNPM_CONFIG_GLOBAL_SHIMS` JSON, never a project file. Enabling needs a reinstall (`pnpm add -g typescript`); disabling does not. `pnpm shim add <pkg>` gives a non-installed package a dispatching command. Skip once with `PNPM_SHIM_BYPASS=1`.

## Checked

2026-11-04. Confirmed against pnpm.io/global-packages and pnpm.io/settings/other (globalShims): v12.0.0-rc.2 behaviour, version-selection rules per kind, .node-version/.nvmrc (v12.7.0) rules, trust policy under auto, globalShims policies and scalar shorthands, allowed read locations, reinstall requirement, pnpm shim add, PNPM_SHIM_BYPASS. Removed: the generic closing Check line (not stated on the page).
Method: documentation only; no commands were run.
