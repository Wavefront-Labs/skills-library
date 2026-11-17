---
id: computing-software.web-development.vite.js-api-config-utilities
name: js-api-config-utilities
category: computing-software
field: web-development
product: vite
tags: [merge-config, search-for-workspace-root, load-env-api, load-config-from-file, normalize-path-api]
level: advanced
status: docs-checked
description: "Config helper exports: mergeConfig (isRoot, null skipped, callback configs), searchForWorkspaceRoot, loadEnv prefixes, normalizePath and loadConfigFromFile."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-javascript.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`mergeConfig(defaults, overrides, isRoot = true)`: deep merge. Pass `isRoot = false` when merging nested options such as two `build` objects. `null` and `undefined` in `overrides` are skipped; to clear a value edit the result. It accepts object-form configs only; for a callback config call it first, or wrap:

```ts
export default defineConfig((configEnv) =>
  mergeConfig(configAsCallback(configEnv), configAsObject),
)
```

`searchForWorkspaceRoot(current, root = searchForPackageRoot(current))`: finds a workspace root (`workspaces` in `package.json`, `lerna.json` or `pnpm-workspace.yaml`), else falls back to `root`. Use with `server.fs.allow`.

`loadEnv(mode, envDir, prefixes = 'VITE_')`: loads `.env` files from `envDir`, merged with matching variables already in `process.env`; only `VITE_`-prefixed unless `prefixes` changes.

`normalizePath(id)`: normalizes a path for plugin interop.

`loadConfigFromFile(configEnv, configFile?, configRoot = process.cwd(), logLevel?, customLogger?)`: loads a config with Rolldown; returns `{ path, config, dependencies }` or `null`.

`version` is Vite's version string; `rolldownVersion` re-exports Rolldown's `VERSION`; `esbuildVersion` and `rollupVersion` remain only for compatibility.

## Checked

2026-11-07. Confirmed against guide/api-javascript.md, read in full: `mergeConfig` signature, `isRoot`, null and undefined skipped, object-form only with the `defineConfig` callback example, `searchForWorkspaceRoot` conditions and `server.fs.allow` pointer, `loadEnv` default `VITE_` prefix, `normalizePath`, `loadConfigFromFile` signature and return shape, and `version`, `rolldownVersion`, `esbuildVersion`, `rollupVersion`. Nothing removed.

Method: documentation only; no commands were run.
