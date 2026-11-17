---
id: computing-software.web-development.vite.plugin-rolldown-hooks-dev
name: plugin-rolldown-hooks-dev
category: computing-software
field: web-development
product: vite
tags: [rolldown-hooks-in-dev, plugin-container, module-parsed-not-called, per-environment-hooks]
level: advanced
status: docs-checked
description: "Which Rolldown hooks the dev server plugin container calls: once at start, per module request, at close; moduleParsed and output generation hooks are skipped."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In dev, the server's plugin container invokes Rolldown build hooks like Rolldown does. All Rolldown hooks are per-environment hooks.

- Once on server start: `options`, `buildStart`.
- Per incoming module request: `resolveId`, `load`, `transform`. Their `options` argument has extra Vite properties (see the SSR docs on SSR-specific plugin logic).
- On server close: `buildEnd`, `closeBundle`.
- Not called in dev: `moduleParsed` (Vite avoids full AST parses) and output generation hooks other than `closeBundle`.

Some `resolveId` calls may pass an absolute path to a generic root `index.html` as `importer`, since the unbundled dev server cannot always derive the real importer. Imports handled in Vite's own resolve pipeline get the correct importer from import analysis.

`this.meta.viteVersion` is a version string; `this.meta.rolldownVersion` exists only on Rolldown-powered Vite (8+):

```ts
buildStart() {
  if (this.meta.rolldownVersion) { /* Rolldown powered Vite */ }
}
```

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Rolldown Hooks, Plugin Context Meta). Confirmed hooks called at start, per request and on close, moduleParsed and output generation hooks not called, the importer note, this.meta.viteVersion and this.meta.rolldownVersion. Nothing removed.

Method: documentation only; no commands were run.
