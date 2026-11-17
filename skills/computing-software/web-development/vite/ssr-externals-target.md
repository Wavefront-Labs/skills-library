---
id: computing-software.web-development.vite.ssr-externals-target
name: ssr-externals-target
category: computing-software
field: web-development
product: vite
tags: [ssr-external, ssr-no-external, ssr-target-webworker, ssr-resolve-conditions]
level: advanced
status: docs-checked
description: "Configure SSR dependency handling: externalized by default, ssr.noExternal and ssr.external, aliases, webworker target, single-file bundles, resolve conditions."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/ssr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Externals: dependencies are externalized from Vite's SSR module system by default, which speeds dev and build. Add one to `ssr.noExternal` if it must go through Vite's pipeline (for example it uses Vite features untranspiled). Linked dependencies are not externalized by default so HMR works; add them to `ssr.external` to test them as unlinked.

Aliases: if an alias redirects one package to another, alias the actual `node_modules` packages instead so externalized dependencies work; Yarn and pnpm support aliasing with the `npm:` prefix.

Target: the SSR build targets Node by default. Set `ssr.target` to `'webworker'` to run in a Web Worker; package entry resolution differs per platform.

Bundle: for runtimes like `webworker`, set `ssr.noExternal: true` to bundle everything into one JS file. All dependencies are treated as noExternal, and importing any Node.js built-in throws.

Conditions: SSR uses `resolve.conditions`; customize with `ssr.resolve.conditions` and `ssr.resolve.externalConditions`.

```js
export default { ssr: { target: 'webworker', noExternal: true } }
```

## Checked

2026-11-07. Re-read the Server-Side Rendering guide (docs/guide/ssr.md) in full. Confirmed SSR Externals (default externalization, ssr.noExternal, linked dependencies and ssr.external), the aliases warning, SSR Target (node default, ssr.target 'webworker'), SSR Bundle (ssr.noExternal true treats all as noExternal and throws on Node.js built-ins) and SSR Resolve Conditions. Nothing removed.

Method: documentation only; no commands were run.
