---
id: computing-software.web-development.biome.config-schema-extends-root-and-plugins
name: config-schema-extends-root-and-plugins
category: computing-software
field: web-development
product: biome
tags: [biome, config-reference, schema, extends, root, plugins, resolutionkind, biome-init, biome-jsonc]
level: practitioner
status: docs-checked
description: "Reference for top-level $schema, extends, root and plugins options including resolutionKind, plus biome init --jsonc."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Scaffold a minimal config with `biome init --jsonc`.

**`$schema`** (string): enables validation, completion and inline docs. If `@biomejs/biome` is installed, point at the local copy, which always matches the installed version: `"$schema": "./node_modules/@biomejs/biome/configuration_schema.json"`. If the editor cannot resolve it, use `https://biomejs.dev/schemas/<version>/schema.json` and set the version to the one you use. Biome warns when the `$schema` URL version differs from the package version.

**`extends`** (`"//"` or `string[]`): `"//"` extends the project-root config from any nested depth. An array takes relative paths or package specifiers, for example `["./common.json", "@org/shared-configs/biome"]`. Merging is left to right: single-value options are overridden by later configs, list options are combined, and the current file is applied last.

**`root`** (boolean, default `true`): marks the root configuration. `"root": false` tells Biome a config found inside the project is nested rather than a second project root. Biome implicitly treats `root` as false when a nested config uses `"extends": "//"`; every other nested config must set `"root": false` explicitly or Biome errors.

**`plugins`** (array of path strings or objects): loads GritQL plugins and JavaScript/TypeScript plugins.

```json
{ "plugins": [
  "./general-plugin.grit",
  { "path": "./react-plugin.js", "includes": ["**/src/components/**", "!**/src/components/generated/**"] }
] }
```

- `path`: a `.grit` file, or a directory containing `biome-manifest.jsonc`.
- `includes`: globs selecting the files the plugin runs on. Omitted means every file eligible for linting; `[]` selects none.
- `resolutionKind`: `"project"` (default) resolves a relative path from the config file's directory, or in a shared config from the directory of the config that extends it; `"config"` resolves from the directory of the config that declares the plugin. Use `"config"` when a shared config loaded via `extends` ships its own plugins. It does not change how `includes` globs resolve.

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the invented Verify step. The `$schema` URL form is confirmed by configuration.mdx (biomejs.dev/schemas/ itself returns 404).

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
