---
id: computing-software.web-development.frontend-development.page-visibility-and-lifecycle
name: page-visibility-and-lifecycle
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, page-visibility, page-lifecycle, bfcache, visibilitychange, pagehide]
level: practitioner
status: docs-checked
description: "Reacting to tab hiding, freezing and bfcache with visibilitychange, pagehide/pageshow and freeze/resume: pausing work, saving state and sending final analytics."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Page_Visibility_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/unload_event
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/pageshow_event
  - https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Page Visibility and page lifecycle

## 1. States
`document.visibilityState` is `visible` or `hidden`; a page becomes hidden when the user switches tabs, minimizes the window, navigates away, or (on mobile) switches apps. Chromium's Page Lifecycle API adds `freeze` and `resume` events. The back/forward cache (bfcache) can restore a page that was navigated away from.

## 2. The events to use
```js
document.addEventListener("visibilitychange", () => {
  if (document.visibilityState === "hidden") { pauseVideo(); stopPolling(); saveDraft(); flushAnalytics(); }
  else { resumePolling(); refreshIfStale(); }
});
addEventListener("pagehide", e => { /* e.persisted = entering bfcache */ });
addEventListener("pageshow", e => { if (e.persisted) refreshIfStale(); });   // restored from bfcache
document.addEventListener("freeze", () => closeConnections());               // Chromium only, experimental
document.addEventListener("resume", () => reopenConnections());
```
- `visibilitychange` to hidden is the **last reliable event** on mobile (app switch, then kill). Save state and send beacons there.
- Send data with `navigator.sendBeacon(url, blob)`, or `fetch(url, { keepalive: true })` when you need another method, headers or the response.

## 3. Never use `unload`
`unload` is not reliably fired on mobile, is incompatible with the bfcache (Firefox, for example, will not cache pages that use it), and Chrome has stopped firing it by default. Use `beforeunload` only for "unsaved changes" prompts, added when the form is dirty and removed after save; it is not reliably fired either, and the dialog needs prior user interaction with the page.

## 4. Keep bfcache eligible
- No `unload` handlers.
- `pageshow` with `event.persisted` is true when a page is restored from the bfcache; refresh stale data there.

## 5. Uses
Pause animations/videos/polling when hidden (battery), defer expensive work, show "new messages" counts in the title only while hidden, refresh stale data on return.

## Verify
Switch tabs and check timers stop; on mobile, background the app and confirm drafts/analytics arrive; navigate away and back and confirm `pageshow` fires with the expected `persisted` value.

## Checked

Checked 2026-10-26 against mdn/content (main) Page Visibility API, `visibilitychange`, `unload`, `beforeunload`, `pageshow` and Navigator.sendBeacon pages and mdn/browser-compat-data.

- Confirmed: transitioning to `hidden` is the last event reliably observed, so save state and send analytics there; `unload` and `beforeunload` are not reliably fired on mobile; `unload` is incompatible with the bfcache and Chrome stopped firing it by default; listen for `beforeunload` only while there are unsaved changes; `pageshow` carries `persisted`; `freeze` is Chromium-only and experimental; most browsers stop `requestAnimationFrame` in background tabs.
- Removed: the lifecycle state chain, the `Cache-Control: no-store`, IndexedDB/WebSocket and DevTools bfcache tester advice, and "normal fetches are cancelled", which the pages checked do not state (the Chrome and web.dev articles were not readable and were dropped from sources).

Method: documentation only; no commands were run.
