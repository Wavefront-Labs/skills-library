---
id: computing-software.web-development.vite.npm-dependency-resolving
name: npm-dependency-resolving
category: computing-software
field: web-development
product: vite
tags: [bare-module-imports, dependency-pre-bundling, strong-caching]
level: practitioner
status: docs-checked
description: "How Vite resolves bare npm imports: detects them, pre-bundles with Rolldown to convert CommonJS/UMD to ESM, rewrites to /node_modules/.vite/deps URLs."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/features.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Native ES imports cannot handle bare specifiers such as `import { someMethod } from 'my-dep'`. Vite detects bare imports in all served source and:

1. Pre-bundles them to speed page loads and to convert CommonJS / UMD modules to ESM. Pre-bundling uses Rolldown, which makes cold start much faster than JavaScript-based bundlers.
2. Rewrites the imports to valid URLs like `/node_modules/.vite/deps/my-dep.js?v=f3sf2ebd`.

Dependencies are strongly cached through HTTP headers. To edit or debug a dependency locally, follow the browser-cache steps in the dependency pre-bundling guide.

See also the dependency pre-bundling skills for cache invalidation and the `optimizeDeps` options.

## Checked

Date: 2026-11-07

Read features.md in full (npm Dependency Resolving and Pre-Bundling section). Confirmed the bare import problem, Rolldown pre-bundling, the /node_modules/.vite/deps/my-dep.js?v=f3sf2ebd rewrite and strong caching. The linked dep-pre-bundling guide was not read; the skill only points to it. Nothing removed.

Method: documentation only; no commands were run.
