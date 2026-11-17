---
id: computing-software.web-development.vite.performance-browser-plugins
name: performance-browser-plugins
category: computing-software
field: web-development
product: vite
tags: [dev-performance, disable-cache-devtools, plugin-audit, plugin-transform-debug]
level: practitioner
status: docs-checked
description: "Speed up the Vite dev server by fixing browser setup (extensions, Disable Cache) and auditing slow plugin hooks with --debug plugin-transform and --profile."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/performance.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Browser: extensions can interfere with requests and slow startup and reload for large apps. Use a dev-only profile without extensions, or incognito. The server hard-caches pre-bundled dependencies and answers source with fast 304s, so make sure "Disable Cache" in devtools is not enabled.

Plugins (community plugin speed is outside Vite's control):
1. Dynamically import large dependencies that are used only sometimes, to cut Node.js startup.
2. Keep `buildStart`, `config` and `configResolved` short; they are awaited during server startup.
3. In `resolveId`, `load` and `transform`, check cheaply first (does `code` contain a keyword, does `id` match an extension) before the full transformation. Slow transforms deepen the request waterfall.

Measure:

```bash
vite --debug plugin-transform
vite --profile
```

With `--profile`, visit the site and press `p` then enter to record a `.cpuprofile`, then inspect it in speedscope. `vite-plugin-inspect` also helps. Async timings are rough estimates.

## Checked

Date: 2026-11-07

Read performance.md in full. Confirmed the browser extension and Disable Cache advice, the three plugin audit points, vite --debug plugin-transform, vite --profile with p then enter and speedscope, vite-plugin-inspect and the rough async timings. Nothing removed.

Method: documentation only; no commands were run.
