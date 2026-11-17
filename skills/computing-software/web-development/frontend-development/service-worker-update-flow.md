---
id: computing-software.web-development.frontend-development.service-worker-update-flow
name: service-worker-update-flow
category: computing-software
field: web-development
product: frontend-development
tags: [progressive-web-app, pwa, service-worker-update, skipwaiting, update-prompt, controllerchange, workbox-window, registration-update]
level: practitioner
status: docs-checked
description: "Shipping service worker updates users actually get: detecting a waiting worker, prompting to reload, skipWaiting via message and controllerchange reload."
sources:
  - https://developer.chrome.com/docs/workbox/handling-service-worker-updates
  - https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers
  - https://vite-pwa-org.netlify.app/guide/prompt-for-update.html
  - https://github.com/GoogleChrome/workbox/blob/v7/packages/workbox-window/src/Workbox.ts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service worker update flow

**Goal:** new deployments reach users promptly without breaking a page that is mid-use.

## 1. Why updates stall
A new SW installs then **waits** while pages are still controlled by the old one (MDN). Users who keep a tab open, or an installed PWA that is never fully closed, can stay on the old version for a long time.

## 2. Options
- **Automatic `self.skipWaiting()` in install**: simplest; safe only if old pages can keep working with new SW + new caches (old page may request asset files the new SW deleted, causing chunk-load errors).
- **Prompted update (recommended for SPAs)**: show "New version available - Reload"; on click, tell the waiting SW to skip waiting, then reload when it takes control.

## 3. Prompted update, no library
```js
// page
const reg = await navigator.serviceWorker.register('/sw.js');
function offer(worker) { showToast('Update available', () => worker.postMessage({ type: 'SKIP_WAITING' })); }
if (reg.waiting) offer(reg.waiting);
reg.addEventListener('updatefound', () => {
  const w = reg.installing;
  w.addEventListener('statechange', () => {
    if (w.state === 'installed' && navigator.serviceWorker.controller) offer(w);
  });
});
let reloaded = false;
navigator.serviceWorker.addEventListener('controllerchange', () => { if (!reloaded) { reloaded = true; location.reload(); } });
setInterval(() => reg.update(), 60 * 60 * 1000);   // long-lived tabs check hourly

// sw.js
self.addEventListener('message', (e) => { if (e.data?.type === 'SKIP_WAITING') self.skipWaiting(); });
```
`navigator.serviceWorker.controller` check excludes the very first install (nothing to update). The `reloaded` guard avoids repeated reloads from multiple `controllerchange` events, for example when DevTools "Update on reload" is on.

With Workbox: `workbox-window` offers a `waiting` event and `wb.messageSkipWaiting()`, which posts a `{type: 'SKIP_WAITING'}` message to the waiting worker (your worker must handle it). vite-plugin-pwa's `registerType` option defaults to `'prompt'`.

## 4. Chunk-load errors
Keep the previous deploy's hashed assets on the server/CDN for a while (don't delete on deploy) so old pages can still lazy-load chunks; catch dynamic `import()` failures and offer a reload.

## Verify
- [ ] Deploy a change with a tab open: toast appears within the check interval; reload shows new version.
- [ ] No infinite reload with DevTools "Update on reload".
- [ ] Old tab can still navigate lazy routes after deploy.

## Checked
Checked 2026-10-26 against the Workbox guide handling-service-worker-updates (offer a reload when precached HTML is served; messageSkipWaiting tells the waiting worker to call skipWaiting), the workbox-window source (SKIP_WAITING message type), MDN Using Service Workers (waiting behaviour) and the vite-plugin-pwa prompt-for-update docs (registerType default prompt). Removed the unconfirmed `useRegisterSW` hook mention. The page and worker snippets were not run.

Method: documentation only; no commands were run.
