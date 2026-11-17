---
id: computing-software.web-development.frontend-development.sendbeacon-and-fetch-keepalive
name: sendbeacon-and-fetch-keepalive
category: computing-software
field: web-development
product: frontend-development
tags: [fetch-api, browser-networking, sendbeacon, fetch-keepalive, page-unload-analytics, pagehide, visibilitychange, analytics]
level: practitioner
status: docs-checked
description: "Reliably sending analytics and final state when a page is hidden or closed using sendBeacon or fetch keepalive on visibilitychange/pagehide instead of unload."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon
  - https://developer.mozilla.org/en-US/docs/Web/API/RequestInit
  - https://developer.mozilla.org/en-US/docs/Web/API/Request/keepalive
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sendBeacon and fetch keepalive

**Goal:** the last analytics batch or draft save reaches the server when the user leaves, without delaying navigation or breaking bfcache.

## 1. Use the right event
- Send on `visibilitychange` when `document.visibilityState === 'hidden'`; MDN calls it the most reliable event for this.
- MDN says `unload`, `beforeunload` and `pagehide` are unreliable for sending analytics, especially on mobile (for example when the user switches apps and later kills the browser), and that developers should use `visibilitychange` instead.
- **Don't use `unload`**: it is incompatible with the back/forward cache (Firefox excludes pages that have unload handlers from the bfcache; Safari and Chrome on Android may not fire it).

## 2. sendBeacon
```js
let queue = [];
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState !== 'hidden' || !queue.length) return;
  const ok = navigator.sendBeacon('/collect', new Blob([JSON.stringify(queue)], { type: 'application/json' }));
  if (ok) queue = [];
});
```
- POST only; the server response is not available; returns `true` if the user agent queued the data and `false` otherwise. The total size of queued data is limited to 64 KiB (MDN).
- For other methods, request properties or the response, MDN recommends `fetch()` with `keepalive`. For a cross-origin collector, test the content type you send against the server's CORS handling.

## 3. fetch keepalive
```js
fetch('/api/draft', { method: 'POST', body: JSON.stringify(draft), headers: { 'Content-Type': 'application/json' }, keepalive: true });
```
Supports methods other than POST, custom request properties and reading the response via the promise; the request body is limited to 64 KiB (MDN). Use for PUT/PATCH or authenticated endpoints that need headers.

## 4. Data design
Batch events in memory and flush on hide; make the server accept duplicates (event ids) since the same batch may be sent twice if the page comes back from hidden.

## Verify
- [ ] Network panel ("Preserve log") shows the beacon after closing/switching tabs.
- [ ] DevTools > Application > Back/forward cache test reports the page as eligible.
- [ ] Server dedupes repeated batches.

## Checked

Checked 2026-10-26 against MDN Navigator.sendBeacon(), RequestInit and Request.keepalive (mdn/content main): POST-only, 64 KiB size limit, boolean return, `visibilitychange` as the recommended event, unreliability of unload/beforeunload/pagehide, unload and bfcache incompatibility, and keepalive advantages over sendBeacon. Removed the unconfirmed CORS-preflight/text-plain advice, the 'being deprecated in Chromium' claim and the beforeunload bfcache claim. The developer.chrome.com source link was replaced by MDN pages that were read.

Method: documentation only; no commands were run.
