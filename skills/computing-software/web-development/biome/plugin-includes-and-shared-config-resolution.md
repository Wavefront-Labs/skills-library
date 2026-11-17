---
id: computing-software.web-development.biome.plugin-includes-and-shared-config-resolution
name: plugin-includes-and-shared-config-resolution
category: computing-software
field: web-development
product: biome
tags: [biome, plugin-includes, plugin-path, resolutionkind, shared-configs, extends, plugins-config, glob-patterns]
level: advanced
status: docs-checked
description: "Restrict a plugin to files with includes globs and load plugins shipped inside a shared config using resolutionKind config."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default a plugin runs on every file Biome processes. Use the object form with `includes` to narrow it:

```json
{ "plugins": [
  { "path": "./react-plugin.grit", "includes": ["src/components/**"] },
  { "path": "./ts-only-plugin.grit", "includes": ["src/**/*.ts", "!src/**/*.test.ts"] }
] }
```

The first runs only inside `src/components/`. The second runs on `.ts` files under `src/` except `.test.ts` files. When `includes` is set a file must match at least one positive pattern and no negated one. Patterns follow the glob syntax reference.

**Plugins in shared configs.** By default Biome resolves a plugin path found in a shared configuration from the directory of the configuration that extends it. To load a plugin that ships alongside the shared file set `resolutionKind` to `"config"`:

```json
{ "plugins": [ { "path": "./plugins/no-object-assign.grit", "resolutionKind": "config" } ] }
```

in `biome.shared.jsonc`, and extend it with `{ "extends": ["./biome.shared.jsonc"] }`. Biome then resolves the plugin from the directory of `biome.shared.jsonc`, while `includes` globs still resolve from the directory of the extending configuration.

The page points to the configuration reference entry `plugins.<ITEM>.resolutionKind` for the full option description.

## Checked

Method: 2026-11-08 compared against the Biome website source mdx for linter plugins (Restricting Plugins to Specific Files, Resolve plugins from shared configurations). The includes example, matching rule and resolutionKind behaviour match the page. Dropped an inferred "publish a shared preset" sentence and an invented "Verify" step.
