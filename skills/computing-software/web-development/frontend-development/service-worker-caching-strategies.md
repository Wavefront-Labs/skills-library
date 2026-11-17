---
id: computing-software.web-development.frontend-development.service-worker-caching-strategies
name: service-worker-caching-strategies
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, service-worker-caching, caching-strategies, cache-first, network-first, stale-while-revalidate, cache-api, runtime-caching]
level: practitioner
status: docs-checked
description: "Picking per-route service worker caching strategies (cache-first, network-first, stale-while-revalidate, network-only) and expiring the Cache API safely."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
  - https://developer.mozilla.org/en-US/docs/Web/API/Cache
  - https://developer.chrome.com/docs/workbox/understanding-storage-quota
  - https://developer.chrome.com/docs/workbox/serving-cached-audio-and-video
  - https://developer.chrome.com/docs/workbox/caching-strategies-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service worker caching strategies

**Goal:** each kind of request uses the strategy that matches how fresh it must be.

## 1. Strategy per request type
| Request | Strategy | Reason |
|---|---|---|
| Hashed static assets (`app.3f9a.js`, fonts) | **Cache first** | Content never changes for a URL |
| HTML navigations | **Network first** with timeout, fallback to cache/offline page | Freshness matters, still works offline |
| Avatars, non-critical images, API reads tolerant of staleness | **Stale-while-revalidate** | Instant, refreshed in background |
| POST/PUT, auth, payments, analytics | **Network only** | Never cache |
| Precached app shell | **Cache only** | Installed with the SW |

## 2. Hand-written fetch handler
```js
self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;                 // let the network handle it
  const url = new URL(request.url);
  if (request.mode === 'navigate') return event.respondWith(networkFirst(request, 3000));
  if (url.pathname.startsWith('/assets/')) return event.respondWith(cacheFirst(request));
});
async function cacheFirst(req) {
  const hit = await caches.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) (await caches.open('assets')).put(req, res.clone());
  return res;
}
async function networkFirst(req, ms) {
  const cache = await caches.open('pages');
  try {
    const res = await Promise.race([fetch(req), new Promise((_, r) => setTimeout(r, ms))]);
    cache.put(req, res.clone());
    return res;
  } catch { return (await cache.match(req)) || caches.match('/offline.html'); }
}
```

## 3. Gotchas
- **Clone before caching**: a Response body can be read once.
- **Opaque responses** (cross-origin `no-cors`, status 0) can't be checked for errors, and Workbox's storage-quota guide says Chrome counts even a few-kilobyte opaque response as around 7 MB against quota. Prefer CORS-enabled CDNs, or limit them with Workbox `ExpirationPlugin` (`maxEntries`, `purgeOnQuotaError`).
- **Range requests** (video/audio) need explicit handling: Workbox documents its `workbox-range-requests` module (`RangeRequestsPlugin`) for serving cached media.
- Items in a `Cache` are not updated or expired automatically (MDN: you are responsible for handling updates); evict by cache-name versioning in `activate`, or with an entry-count/age limit such as Workbox `ExpirationPlugin` (`maxEntries`, `maxAgeSeconds`).
- Don't cache user-specific responses under shared URLs.

## Verify
- [ ] DevTools > Network with "Offline": shell and visited pages load; others show the offline page.
- [ ] Application > Cache Storage size stays bounded after browsing many pages.
- [ ] After deploy, HTML updates on next online navigation.

## Checked
Checked 2026-10-26 against MDN Using Service Workers and the Cache interface (no automatic update or expiry), and the Workbox guides on storage quota (opaque responses about 7 MB in Chrome, ExpirationPlugin options) and serving cached audio and video (RangeRequestsPlugin). The strategy table and the fetch-handler code are general patterns and were not run; removed the unconfirmed claim that range requests do not work from a cached 200 response and the Set-Cookie remark.

Method: documentation only; no commands were run.
