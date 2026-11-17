---
id: computing-software.web-development.frontend-development.workbox-precaching-and-routing
name: workbox-precaching-and-routing
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, workbox, workbox-precaching, workbox-routing, vite-plugin-pwa, injectmanifest, generatesw, expiration-plugin]
level: practitioner
status: docs-checked
description: "Using Workbox (generateSW/injectManifest, vite-plugin-pwa) for revisioned precaching, routes with strategies, expiration and navigation fallback."
sources:
  - https://developer.chrome.com/docs/workbox/precaching-with-workbox
  - https://developer.chrome.com/docs/workbox/precaching-dos-and-donts
  - https://developer.chrome.com/docs/workbox/managing-fallback-responses
  - https://github.com/GoogleChrome/workbox/blob/v7/packages/workbox-build/src/types.ts
  - https://github.com/GoogleChrome/workbox/blob/v7/packages/workbox-routing/src/NavigationRoute.ts
  - https://vite-pwa-org.netlify.app/guide/inject-manifest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workbox precaching and routing

**Goal:** let Workbox generate the precache manifest from the build and declare runtime routes declaratively.

## 1. Pick a mode
- **generateSW**: Workbox writes the whole SW from config. Good when you only need precache + runtime caching.
- **injectManifest**: you write `sw.js`, Workbox injects `self.__WB_MANIFEST`. Needed for push, background sync, custom logic.

With Vite: `vite-plugin-pwa` wraps both; set `strategies: 'injectManifest'` for your own worker (its docs show this).

## 2. injectManifest SW
```js
import { precacheAndRoute, cleanupOutdatedCaches, createHandlerBoundToURL } from 'workbox-precaching';
import { registerRoute, NavigationRoute } from 'workbox-routing';
import { StaleWhileRevalidate, CacheFirst, NetworkFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

precacheAndRoute(self.__WB_MANIFEST);      // [{url, revision}] from the build
cleanupOutdatedCaches();
registerRoute(new NavigationRoute(createHandlerBoundToURL('/index.html'), { denylist: [/^\/api\//] })); // SPA fallback
registerRoute(({ request }) => request.destination === 'image',
  new CacheFirst({ cacheName: 'images', plugins: [new ExpirationPlugin({ maxEntries: 200, maxAgeSeconds: 30 * 86400 })] }));
registerRoute(({ url }) => url.pathname.startsWith('/api/feed'),
  new StaleWhileRevalidate({ cacheName: 'feed' }));
```

## 3. Precache list hygiene
- Precache only the shell (HTML entry, main JS/CSS, critical fonts/icons). Configure `globPatterns` / `globIgnores`; hundreds of MB of images in precache means every install downloads them.
- Workbox precache entries are `{url, revision}`; see the precaching-dos-and-donts guide for how to handle revisioned and versioned URLs.
- `maximumFileSizeToCacheInBytes` defaults to 2097152 (2 MiB) in workbox-build and is meant to stop accidentally precaching very large files; larger matching files are skipped, so check the build output.

## 4. Debugging
Workbox logs to the console in development builds. In DevTools > Application > Cache Storage the precache cache is named with the `workbox` prefix and `precache-v2` (workbox-core defaults). A navigation fallback that catches API or admin URLs is a common bug - `NavigationRoute` takes `allowlist` and `denylist` options.

## Verify
- [ ] Build output lists the precached files and total size you expect.
- [ ] Offline reload of a deep SPA route serves `index.html`.
- [ ] Image cache entry count stays at or below `maxEntries`.

## Checked
Checked 2026-10-26 against the Workbox guides precaching-with-workbox (injectManifest placeholder self.__WB_MANIFEST) and managing-fallback-responses, the workbox-build types (maximumFileSizeToCacheInBytes default 2097152), workbox-routing NavigationRoute (allowlist, denylist), workbox-core cacheNames defaults (prefix workbox, precache-v2), workbox-expiration options (maxEntries, maxAgeSeconds), and the vite-plugin-pwa inject-manifest docs. Removed the unconfirmed claim about how Workbox treats hashed versus un-hashed filenames. Code was not run.

Method: documentation only; no commands were run.
