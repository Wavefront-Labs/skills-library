---
id: computing-software.web-development.frontend-development.static-assets-hashing-and-base-path
name: static-assets-hashing-and-base-path
category: computing-software
field: web-development
product: frontend-development
tags: [asset-hashing, vite-base-path, public-directory, cache-busting, build-tooling]
level: practitioner
status: docs-checked
description: "Handling static assets in Vite and bundlers: imported vs public assets, content hashes for immutable caching, base path for subdirectory deploys, CDN URLs and the manifest."
sources:
  - https://vite.dev/guide/assets
  - https://vite.dev/guide/build#public-base-path
  - https://vite.dev/config/shared-options#base
  - https://vite.dev/guide/backend-integration
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static assets, hashing and the base path

## 1. Imported assets vs the public folder
| | `import logo from "./logo.svg"` | `public/robots.txt` |
|---|---|---|
| Output name | `assets/logo-3fA9c2.svg` (content hash) | copied as-is |
| Use for | everything referenced by code/CSS | files needing a fixed URL: `robots.txt`, `favicon.ico`, `.well-known/*`, verification files |

Reference public files with absolute paths (`/robots.txt`), never `import` them. Small imports are inlined as base64 data URLs below `build.assetsInlineLimit`.

## 2. Dynamic asset URLs
```js
const url = new URL(`./flags/${code}.svg`, import.meta.url).href; // Vite resolves and hashes at build
```
Keep the URL pattern statically analysable; for links built on the fly use `import.meta.env.BASE_URL`, written exactly like that (it is replaced at build time).

## 3. Caching headers that go with hashes
- `/assets/*` -> `Cache-Control: public, max-age=31536000, immutable`.
- `index.html` -> `Cache-Control: no-cache` so new deploys pick up new hashes.
- Keep previous deploy's assets for a while (or deploy atomically to object storage without deleting) so open tabs lazy-loading old chunks don't 404; Vite fires a `vite:preloadError` event when a dynamic import fails, which you can handle by reloading.

## 4. Base path for subdirectory or CDN deploys
```js
// vite.config.js
export default { base: process.env.BASE_PATH ?? "/" };   // "/app/" for example.com/app/, or "https://cdn.example.com/"
```
- In code use `import.meta.env.BASE_URL` for runtime-built links; router basename must match (`createBrowserRouter(routes, { basename: import.meta.env.BASE_URL })`).

## 5. Backend integration
`build.manifest: true` writes `.vite/manifest.json` mapping source entries to hashed files + CSS + imports, so Django/Rails/Laravel templates can emit the right `<script>`/`<link>` tags.

## Checked

2026-11-01. Confirmed in Vite docs source: imports return resolved public URLs, `assetsInlineLimit` inlines small assets as base64, `public` directory copied as-is and served at `/`, `base` option and `--base`, `import.meta.env.BASE_URL`, `vite:preloadError`, `build.manifest` writing `.vite/manifest.json`; MDN caching guide for `max-age=31536000, immutable`. Removed: size figure, hashed-name and build-error claims, GitHub Pages and relative-base claims.

Method: documentation only; no commands were run.

## Verify
- [ ] After a build, every hashed file gets the immutable header and `index.html` does not; app works under the configured base path including deep-link reload; no 404s for `/public` files in the network panel.
