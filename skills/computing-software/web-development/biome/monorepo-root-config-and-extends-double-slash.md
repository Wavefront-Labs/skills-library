---
id: computing-software.web-development.biome.monorepo-root-config-and-extends-double-slash
name: monorepo-root-config-and-extends-double-slash
category: computing-software
field: web-development
product: biome
tags: [biome, monorepo, root-config, extends, nested-configuration, workspace, root-false, microsyntax]
level: advanced
status: docs-checked
description: "Set up a v2 monorepo with a root biome.json, nested configs using root false and extends '//', and a team that opts out of inheritance."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/big-projects.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v2 Biome supports monorepos out of the box.

1. **Root configuration** at the repository root, e.g. recommended rules and formatter options (`lineWidth: 120`, `indentStyle: "space"`, `indentWidth: 6`).
2. **Nested configs** in packages that need them must set `"root": false`. To inherit the root, use the v2 microsyntax `"extends": "//"`, which means "extend the root configuration wherever this nested file lives":

```json
// packages/logger/biome.json
{ "root": false, "extends": "//",
  "linter": { "rules": { "suspicious": { "noConsole": "off" } } } }
```

```json
// packages/generate/biome.json  (generated code: no formatting)
{ "extends": "//", "formatter": { "enabled": false } }
```

With `extends: "//"` you may omit `"root": false` because it is implied.

3. **Opt out of inheritance**: a team with different standards (for example `packages/analytics`) omits `extends` and sets its own options with `"root": false`.
4. Run Biome from the repo root or from a single package; all settings are respected.

**Nested vendored projects.** If Biome finds a nested config without `"root": false` (a vendored folder or Git submodule using Biome), ignore that project entirely with `files.includes`.

For plain multi-config layouts without a root, Biome uses the nearest config found by walking upward from the working directory.

Verify: run `biome lint` inside `packages/logger` and confirm `noConsole` no longer reports.

## Checked

2026-11-08. Read the Biome big-projects guide in full. Confirmed v2 monorepo support, root false, the extends '//' microsyntax and its implied root false, the opt-out case, the vendored-project tip and nearest-config lookup. Nothing removed.

Method: documentation only; no commands were run.
