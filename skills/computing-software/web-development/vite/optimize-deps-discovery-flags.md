---
id: computing-software.web-development.vite.optimize-deps-discovery-flags
name: optimize-deps-discovery-flags
category: computing-software
field: web-development
product: vite
tags: [optimize-deps-force, no-discovery, hold-until-crawl-end, needs-interop, optimize-deps-disabled]
level: advanced
status: docs-checked
description: "Optimizer flags: rolldownOptions (esbuildOptions deprecated), force, noDiscovery, holdUntilCrawlEnd, needsInterop, and the deprecated disabled option."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/config/dep-optimization-options.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- `optimizeDeps.rolldownOptions`: Rolldown options for scanning and optimizing; `input`, `logLevel` and some `output` fields (`format`, `sourcemap`, `dir`, `banner`) are omitted. `plugins` merge with Vite's dep plugin. `optimizeDeps.esbuildOptions` is deprecated and converted to it.
- `optimizeDeps.force`: `true` ignores previously cached optimized deps.
- `optimizeDeps.noDiscovery` (default `false`): `true` disables automatic discovery; only `include` entries are optimized, so CJS-only deps must be listed in dev.
- `optimizeDeps.holdUntilCrawlEnd` (experimental, default `true`): holds the first result until static imports are crawled on cold start, avoiding full reloads from new common chunks. If the scanner plus `include` find everything, disable it so the browser processes more requests in parallel.
- `optimizeDeps.needsInterop` (experimental, `string[]`): force ESM interop for listed deps. Vite normally detects this; Vite warns when adding a package here would avoid a full-page reload on cold start.
- `optimizeDeps.disabled` (deprecated): build-time pre-bundling was removed as of Vite 5.1. To turn the optimizer off completely use `noDiscovery: true` with `include` empty or undefined.

## Checked

Date: 2026-11-07

Read dep-optimization-options.md in full. Confirmed rolldownOptions omissions and plugin merge, esbuildOptions deprecated, force, noDiscovery default false, holdUntilCrawlEnd experimental default true, needsInterop experimental string[] and its warning, disabled deprecated since 5.1 with the noDiscovery workaround. Nothing removed.

Method: documentation only; no commands were run.
