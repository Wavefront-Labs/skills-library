---
id: computing-software.web-development.frontend-development.fullscreen-wake-lock-and-orientation
name: fullscreen-wake-lock-and-orientation
category: computing-software
field: web-development
product: frontend-development
tags: [fullscreen-api, screen-wake-lock, screen-orientation-lock, fullscreen-element, device-apis]
level: practitioner
status: docs-checked
description: "Fullscreen API with user gestures and ::backdrop, keeping the screen awake with Screen Wake Lock (re-acquire on visibility), and orientation lock limits per platform."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API
  - https://developer.mozilla.org/en-US/docs/Web/API/ScreenOrientation/lock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fullscreen, Wake Lock and orientation

## 1. Fullscreen
```js
async function toggleFullscreen(el) {
  if (document.fullscreenElement) return document.exitFullscreen();
  await el.requestFullscreen({ navigationUI: "hide" });   // must be inside a user gesture
}
document.addEventListener("fullscreenchange", () => btn.setAttribute("aria-pressed", !!document.fullscreenElement));
```
```css
.player:fullscreen { background: #000; }
.player::backdrop { background: rgb(0 0 0 / .9); }
```
- An element in an iframe needs the iframe's `allowfullscreen` attribute (or `allow="fullscreen"`), and any Permissions-Policy must allow the `fullscreen` feature.
- Safari on iOS is listed as partial support for `requestFullscreen()` from 16.4 (MDN browser-compat-data); check the current notes, and feature-detect with `document.fullscreenEnabled`, which is false when fullscreen is unavailable for any reason.
- Users can exit with Esc or F11; provide your own visible exit control and do not trap users.

## 2. Screen Wake Lock (recipes, presentations, scanning)
```js
let lock = null;
async function keepAwake() {
  try { lock = await navigator.wakeLock.request("screen"); lock.addEventListener("release", () => (lock = null)); }
  catch (e) { /* NotAllowedError: document not fully active or hidden, or the system refused (for example low battery) */ }
}
document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible" && wantAwake && !lock) keepAwake(); });
```
Only visible documents can acquire the lock, and the system can release it (for example on low battery or when the document is hidden or inactive), so re-acquire on visibility. Per MDN browser-compat-data: Chrome 84, Firefox 126, Safari 16.4. Release when done (`lock.release()`) and offer a visible toggle.

## 3. Orientation lock
```js
await el.requestFullscreen();
await screen.orientation.lock("landscape").catch(() => {});   // mostly mobile browsers; may reject
```
MDN: orientation locking is typically enabled only on mobile devices and when the browser context is full screen. Support (browser-compat-data): Chrome 38 (partial), Firefox 144, not Safari; some engines always reject with `NotSupportedError`. Prefer responsive layouts; WCAG 2.1 SC 1.3.4 (Orientation) says content should not restrict its view and operation to a single display orientation unless essential. The web app manifest `orientation` member sets the default orientation for the installed web app.

## Verify
- [ ] Fullscreen button works on desktop, Android and degrades on iPhone (hidden or uses video fullscreen).
- [ ] Screen stays on for 5+ minutes in a recipe view, including after switching apps and back.

## Checked

Checked 2026-10-26 against MDN Fullscreen API, Element.requestFullscreen(), Screen Wake Lock API, WakeLock.request(), ScreenOrientation.lock() and the manifest `orientation` member (mdn/content main), MDN browser-compat-data (api/WakeLock.json, api/Element.json, api/ScreenOrientation.json) and the W3C WCAG 2.1 Understanding SC 1.3.4 page: iframe and Permissions-Policy requirements, `navigationUI` option, wake-lock visibility rules and `NotAllowedError`, orientation-lock context and support. Removed the unconfirmed `webkitEnterFullscreen` iPhone statement and the Android-only orientation remark.

Method: documentation only; no commands were run.
