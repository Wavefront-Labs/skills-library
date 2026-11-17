---
id: computing-software.software-engineering.javascript.js-sw-lifecycle-updates
name: js-sw-lifecycle-updates
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, service-worker-update, js-service-workers]
level: advanced
status: docs-checked
description: "Service worker lifecycle: install, waiting, activate, skipWaiting and clients.claim, and what happens when a new version is fetched."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API/Using_Service_Workers", "https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorker/state", "https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service worker lifecycle and updates

- First install: `install` is always the first event, used to populate caches. After a successful install the first worker gets `activate` without waiting for pages to close. Existing documents are not controlled until reloaded, because a document starts with or without a service worker and keeps that for its lifetime; `clients.claim()` overrides this.
- Update: whenever a new version of the worker is fetched the cycle repeats. The old version stays active and controls its clients while the new one runs `install` (it can populate a new cache). When installation succeeds the new version waits.
- Once all pages controlled by the old version are closed and it has finished handling pending events, the new version receives `activate`; use it to clean up resources from previous versions, such as old caches.
- The new worker can call `skipWaiting()` to be activated without waiting for open pages to close; it then takes over the pages the old version controlled. After activation, newly opened pages in scope are controlled by the new version.
- `ServiceWorker.state` and the registration's `installing`, `waiting` and `active` workers let a page see where a worker is in this cycle.

Self-check: deploy a changed worker and confirm a waiting worker appears before activation.

## Checked

2026-11-03. Confirmed on MDN: Using Service Workers (initial installation, replacing a worker, waiting, activate cleanup, skipWaiting, clients.claim, scope after activation), ServiceWorker.state, ServiceWorkerRegistration. Removed: the 24-hour byte-compare update check, the `SKIP_WAITING` message and `controllerchange` update-prompt pattern, the `Cache-Control: no-cache` header advice and DevTools panel options, none of which is stated on a page read.
Method: documentation only; no commands were run.
