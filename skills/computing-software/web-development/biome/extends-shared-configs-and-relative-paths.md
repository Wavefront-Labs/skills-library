---
id: computing-software.web-development.biome.extends-shared-configs-and-relative-paths
name: extends-shared-configs-and-relative-paths
category: computing-software
field: web-development
product: biome
tags: [biome, extends, shared-config, common-json, config-inheritance, relative-paths, plugin-paths, publish-config]
level: advanced
status: docs-checked
description: "Share settings with extends arrays: resolution order, nested extends, relative paths resolved from the extending config, and root-config caveat."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/big-projects.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Besides `"//"`, `extends` accepts an array of paths to other configs:

```json
{ "extends": ["./common.json"] }
```

- Entries resolve from the path where the `biome.json` is defined and are processed in order, so later files override earlier ones.
- Extended files can extend other files.
- Relative paths in a shared config (globs, plugin paths by default) are resolved from the directory of the config that extends it, not from the shared file's own directory. Plugins that ship with a shared configuration can opt out; see the plugin documentation section on resolving plugins from shared configurations.

**Example.** `common.json` at the repo root sets `files.includes: ["src/**/*.js", "test/**/*.js"]` and `linter.includes: ["**", "!test"]`. Both `frontend/biome.json` and `backend/biome.json` contain `{ "extends": ["../common.json"] }`. Per the page, running from `frontend/` formats and lints all JavaScript in `frontend/src/` and `frontend/test/` and, in its wording, 'only format[s]' files in `frontend/src/` (`linter.includes` is the setting that excludes `test`); `backend/` behaves the same relative to itself. The paths in `common.json` are interpreted from the folder containing the extending `biome.json`.

**Caveat.** In this layout both `frontend/biome.json` and `backend/biome.json` are root configurations, so you cannot run Biome from the repository root unless you pass `--config-path` pointing at one of them.

To share one config across many projects, publish it as an npm package (see the publishing guide).

## Checked

2026-11-04: every remaining claim, flag, default and example was compared with the cited page(s) read in full and confirmed. Removed: the example result reworded to the page's own wording, and the unsupported comparison with the v2 monorepo setup and the invented Verify step.

Method: fetched the cited pages with tools/review/fetch_pages.py, read them in full, ran tools/review/phrase_check.py and compared the remaining misses by hand.
