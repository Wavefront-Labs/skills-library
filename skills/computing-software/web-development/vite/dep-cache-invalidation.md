---
id: computing-software.web-development.vite.dep-cache-invalidation
name: dep-cache-invalidation
category: computing-software
field: web-development
product: vite
tags: [vite-cache-directory, force-rebundle, browser-dependency-cache, lockfile-invalidation]
level: practitioner
status: docs-checked
description: "Vite dependency caches: node_modules/.vite triggers, force re-bundling, immutable browser caching, and the steps to debug a dependency with local edits."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/dep-pre-bundling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
File system cache: pre-bundled dependencies live in `node_modules/.vite`. Pre-bundling re-runs only when one of these changes:
- package manager lockfile content (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lock`, `aube-lock.yaml`, `nub.lock`)
- patches folder modification time
- relevant fields in `vite.config.js`
- the `NODE_ENV` value

Force a re-bundle with `vite --force`, or delete `node_modules/.vite`.

Browser cache: resolved dependency requests carry `max-age=31536000,immutable`, so once cached they never hit the dev server again. They auto-invalidate through the appended version query when a different version is installed.

To debug a dependency with local edits:
1. Temporarily disable the cache in the browser devtools Network tab.
2. Restart the dev server with `--force`.
3. Reload the page.

## Checked

2026-11-04. Confirmed against the Vite Dependency Pre-Bundling guide (docs/guide/dep-pre-bundling.md, Caching): cache directory, the four re-run triggers with lockfile names, --force, max-age=31536000,immutable and the three debugging steps. Nothing removed.

Method: documentation only; no commands were run.
