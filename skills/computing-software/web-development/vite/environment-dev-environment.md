---
id: computing-software.web-development.vite.environment-dev-environment
name: environment-dev-environment
category: computing-software
field: web-development
product: vite
tags: [dev-environment-class, server-environments, environment-module-graph, fetch-module-result]
level: advanced
status: docs-checked
description: "Use server.environments and the DevEnvironment class: transformRequest, warmupRequest, isolated EnvironmentModuleGraph, and FetchResult variants for the module runner."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-instances.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Access environments with `server.environments` (for example `server.environments.client.transformRequest(url)`, `server.environments.ssr.moduleGraph`).

`DevEnvironment` has `name`, `hot` (channel to the module runner), `moduleGraph`, `plugins`, `pluginContainer`, `config`. Methods:
- `transformRequest(url)`: resolve to an id, load, run the plugin pipeline, update the module graph.
- `warmupRequest(url)`: low-priority processing to avoid waterfalls.
- `fetchModule(id, importer?, options?)`: called by the module runner, not manually.

`TransformResult` is `{ code, map, etag?, deps?, dynamicDeps? }`.

Each environment has an isolated `EnvironmentModuleGraph` with one signature, so generic algorithms and `hotUpdate` work per environment. Nodes (`EnvironmentModuleNode`) carry `url`, `id`, `file`, `type`, `importers`, `importedModules`, `transformResult` (`null` if registered but unprocessed) and HMR fields. Graph methods include `getModuleByUrl`, `getModuleById`, `getModulesByFile`, `invalidateModule`, `invalidateAll` and `ensureEntryFromUrl`.

`fetchModule` returns a `FetchResult`:
- `CachedFetchResult { cache: true }`, like HTTP 304.
- `ExternalFetchResult { externalize, type }`: runner uses native `import` (`type`: `module`, `commonjs`, `builtin`, `network`).
- `ViteFetchResult { code, file, id, url, invalidate }`; `invalidate` is usually `true` after an HMR update.

## Checked

2026-11-07. Confirmed against guide/api-environment-instances.md, read in full: `server.environments` access, the `DevEnvironment` members and methods, `TransformResult`, separate module graphs, the `EnvironmentModuleNode` fields, the `EnvironmentModuleGraph` methods named in the skill, and the three `FetchResult` variants with `externalize` types and `invalidate`. Nothing removed.

Method: documentation only; no commands were run.
