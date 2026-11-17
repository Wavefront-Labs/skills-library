---
id: computing-software.web-development.biome.v2-globs-includes-and-config-relative-paths
name: v2-globs-includes-and-config-relative-paths
category: computing-software
field: web-development
product: biome
tags: [biome, includes, ignore-removed, glob-engine, relative-paths, monorepo, upgrade-v2, files-includes, negated-globs]
level: advanced
status: docs-checked
description: "Understand v2 glob changes: ignore and include became includes, no auto **/ prefix, * no longer matches /, and paths are relative to the config file."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/installation/upgrade-to-biome-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`ignore` and `include` were replaced by `includes`.** The old glob engine had flaws that could not be fixed without breaking changes. If you already ran the `migrate` command you should not see regressions.

**No more automatic `**/` prefix.** v1 turned `src/**` into `**/src/**`, so it also matched `/projectB/frontend/src/file.js`. In v2 `src/**` matches `src/file.js` but not `/projectA/src/file.js` or `/projectB/frontend/src/file.js`, whereas `**/src/**` matches all three (the table in the page calls it too eager).

**`*` does not match `/` anymore.** v1 converted `**/src/*.js` to `**/src/**/*.js`. In v2 `*` stays within one path segment.

**Paths are relative to the configuration file**, not the working directory. Example: `biome.json` at the repo root with `files.includes: ["src/**"]`, and a package `ui/` whose script runs `biome check`.

- v1: Biome finds the parent `biome.json`, prepends the working directory `ui/`, so the glob became `ui/src/**` and matched `ui/src/main.tsx` and `ui/src/utils.ts` (two files), but not the root `src/deploy.js`.
- v2: the glob `src/**` is evaluated from the config file location, so it matches `src/deploy.js` (one file) and not `ui/src/*`.

To keep the v1 behaviour write `"includes": ["ui/src/**"]`.

## Checked

2026-11-08. Read the upgrade-to-biome-v2 page in full. Unchanged: ignore/include replaced by includes, no automatic **/ prefix, * no longer matching /, paths relative to the config file, the ui/src example and its v1/v2 behaviour. Reworded the migrate note to the page's wording. Removed: the claim about ! exclusion patterns (taken from another page) and the invented Verify step.

Method: documentation only; no commands were run.
