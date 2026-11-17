---
id: computing-software.web-development.vite.build-target-modulepreload
name: build-target-modulepreload
category: computing-software
field: web-development
product: vite
tags: [build-target-option, build-module-preload, resolve-dependencies, modulepreload-polyfill]
level: advanced
status: docs-checked
description: "build.target special values (baseline-widely-available, esnext) via Oxc, and build.modulePreload polyfill and resolveDependencies for custom preload lists."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/build-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`build.target` (default `'baseline-widely-available'`): resolves to `['chrome111', 'edge111', 'firefox114', 'safari16.4', 'ios16.4']` for this major. `'esnext'` assumes native dynamic import and does minimal transpiling. Custom values: ES version (`es2015`), browser plus version (`chrome58`) or an array; transformed by Oxc Transformer, which warns on features it cannot lower safely.

`build.modulePreload` (default `{ polyfill: true }`): the polyfill is injected into each `index.html` entry proxy module. With a non-HTML entry via `build.rolldownOptions.input`, import it yourself:

```js
import 'vite/modulepreload-polyfill'
```

It does not apply to library mode. `{ polyfill: false }` disables it. With a relative `base`, preload paths use `import.meta.url`. `build.polyfillModulePreload` is deprecated.

Experimental `resolveDependencies(url, deps, { hostId, hostType })` runs per dynamic import and per chunk imported in entry HTML; return a filtered or extended list of paths relative to `build.outDir`:

```js
modulePreload: { resolveDependencies: (filename, deps, { hostId, hostType }) => deps.filter(condition) }
```

Paths can be changed further with `experimental.renderBuiltUrl`.

## Checked

2026-11-04. Confirmed against the Vite build options page (docs/config/build-options.md): target default list and esnext, Oxc transformer, modulePreload polyfill and resolveDependencies signature, deprecation of polyfillModulePreload. Nothing removed.

Method: documentation only; no commands were run.
