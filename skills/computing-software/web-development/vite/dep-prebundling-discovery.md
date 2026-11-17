---
id: computing-software.web-development.vite.dep-prebundling-discovery
name: dep-prebundling-discovery
category: computing-software
field: web-development
product: vite
tags: [auto-dependency-discovery, optimize-deps-include, linked-dependencies, optimize-deps-rolldown]
level: advanced
status: docs-checked
description: "Control Vite dependency discovery: crawl on cold cache, re-bundle for late imports, linked monorepo packages, optimizeDeps include and exclude, and rolldownOptions."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/dep-pre-bundling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With no cache, Vite crawls source for bare imports and uses them as pre-bundle entries. A new dependency met after startup triggers a re-bundle and a page reload if needed.

Linked packages in a monorepo: dependencies not resolved from `node_modules` are treated as source and not bundled; Vite analyzes their dependency list. That needs the linked dep to export ESM; otherwise add it:

```js
export default defineConfig({
  optimizeDeps: {
    include: ['linked-dep'],
  },
})
```

After changing a linked dep, restart the dev server with `--force`.

Use `include` or `exclude` when an import is not discoverable in source (for example created by a plugin transform); otherwise the server re-bundles right after start. Include large or CommonJS deps; exclude small deps that are already valid ESM.

Customize Rolldown for pre-bundling with `optimizeDeps.rolldownOptions`, such as adding a plugin for special files or changing the target.

## Checked

Date: 2026-11-07. Read dep-pre-bundling.md in full. Automatic Dependency Discovery, Monorepos and Linked Dependencies (including `optimizeDeps.include` and `--force`) and Customizing the Behavior (include/exclude advice, `optimizeDeps.rolldownOptions`) matched; nothing trimmed.

Method: documentation only; no commands were run.
