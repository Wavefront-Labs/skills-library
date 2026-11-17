---
id: computing-software.web-development.vite.ssr-production-build
name: ssr-production-build
category: computing-software
field: web-development
product: vite
tags: [ssr-build, ssr-manifest, prerender-ssg, early-hints]
level: advanced
status: docs-checked
description: "Ship Vite SSR to production: separate client and --ssr server builds, production branches in server.js, --ssrManifest preload directives, and pre-rendering."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/ssr.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Produce a client build and an SSR build that can be loaded directly with `import()`:

```json
{
  "scripts": {
    "dev": "node server",
    "build:client": "vite build --outDir dist/client",
    "build:server": "vite build --outDir dist/server --ssr src/entry-server.js"
  }
}
```

`--ssr` marks the SSR build and needs the SSR entry. In `server.js`, branch on `process.env.NODE_ENV`:
- use `dist/client/index.html` as the template (correct asset links) instead of the root file;
- use `import('./dist/server/entry-server.js')` instead of `vite.ssrLoadModule`;
- create and use the Vite dev server only in dev branches, and add static serving of `dist/client`.

Preload directives: add `--ssrManifest` to the client build. It writes `dist/client/.vite/ssr-manifest.json` (from the client build, to map module IDs to client files). The frameworks must collect the module IDs used in a render; `@vitejs/plugin-vue` registers them on the Vue SSR context (`ctx.modules`). Pass the manifest to `render` to emit preload directives for async routes; also usable for 103 Early Hints.

Pre-rendering / SSG: if routes and data are known ahead, pre-render them using the same logic as production SSR.

## Checked

2026-11-04. Confirmed against the Vite SSR guide (docs/guide/ssr.md, Building for Production, Generating Preload Directives, Pre-Rendering): build scripts, --ssr, production branches in server.js, --ssrManifest output path, plugin-vue ctx.modules, 103 Early Hints, pre-rendering. Nothing removed.

Method: documentation only; no commands were run.
