---
id: computing-software.devops-ci-cd.deployment-strategies.static-asset-versioning-across-deploys
name: static-asset-versioning-across-deploys
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, asset-versioning, zero-downtime, cdn]
level: practitioner
status: draft
description: "Avoid broken pages during deploys by content-hashing static assets, keeping previous builds available on the CDN, and caching HTML differently from hashed files."
sources: ["https://web.dev/articles/http-cache", "https://vite.dev/guide/build"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Static asset versioning across deploys

During a rolling or blue-green deploy, a browser can load HTML from the new version and request
`app.js` from an old server (or vice versa), producing 404s or mismatched code ("ChunkLoadError").

## Rules
1. **Content-hash filenames**: `app.3f9a1c.js` (Vite/webpack/esbuild do this by default in production).
2. **Upload assets before switching HTML**, and **keep old assets** for several releases (at least
   max session length). Use a shared bucket/CDN, not per-server disks.
   ```bash
   aws s3 sync dist/assets s3://web-assets/assets --cache-control "public,max-age=31536000,immutable"
   aws s3 cp dist/index.html s3://web-assets/index.html --cache-control "no-cache"
   ```
   No `--delete` on the asset sync; prune old hashes with a lifecycle rule (e.g. 30 days).
3. **Cache headers**: hashed assets `immutable, max-age=1y`; HTML `no-cache` (revalidate) so new
   deploys are seen; service workers need an update strategy.
4. Lazy-loaded chunks: handle load failure by reloading the page once
   (`window.addEventListener('vite:preloadError', () => location.reload())`).

## Server-rendered apps
Asset manifest mapping logical names to hashed files must be from the same build as the HTML
renderer; deploy assets first, then servers.

## Verify
- [ ] During a deploy, an open old tab still loads its lazy chunks; new tabs get new assets; CDN 404 rate stays flat.
