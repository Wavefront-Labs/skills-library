---
id: computing-software.web-development.frontend-development.geolocation-api
name: geolocation-api
category: computing-software
field: web-development
product: frontend-development
tags: [device-apis, geolocation-api, permission-prompts, location, javascript]
level: practitioner
status: docs-checked
description: "Using navigator.geolocation responsibly: asking in context, getCurrentPosition vs watchPosition, accuracy and timeout options, error handling and privacy fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
  - https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition
  - https://web.dev/articles/permissions-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Geolocation API

## 1. Ask in context
Do not request on page load: the browser prompts the user as soon as `navigator.geolocation` is used, and a refusal is hard to undo. Trigger from a "Use my location" button next to a manual postcode/city field.

## 2. Code
```js
function locate() {
  return new Promise((resolve, reject) => {
    if (!("geolocation" in navigator)) return reject(new Error("unsupported"));
    navigator.geolocation.getCurrentPosition(resolve, reject, {
      enableHighAccuracy: false,   // true = GPS, slower, more battery
      timeout: 10_000,             // ms until TIMEOUT error
      maximumAge: 300_000,         // accept a cached fix up to 5 min old
    });
  });
}
try { const { coords } = await locate(); search(coords.latitude, coords.longitude, coords.accuracy); }
catch (e) { showManualEntry(e.code === 1 ? "Location blocked - enter a postcode" : "Couldn't get location"); }
```
Error codes: `1 PERMISSION_DENIED`, `2 POSITION_UNAVAILABLE`, `3 TIMEOUT`. Without a `timeout`, the default is Infinity - the promise may never settle.

## 3. Tracking
`const id = navigator.geolocation.watchPosition(onPos, onErr, opts)`; stop with `clearWatch(id)` when the view unmounts or the page is hidden - continuous high-accuracy watching drains battery.

## 4. Permissions
```js
const status = await navigator.permissions.query({ name: "geolocation" });
status.state; // "granted" | "prompt" | "denied"; status.onchange = () => {}
```
Use it to decide whether to show the button or a "you blocked location - here's how to re-enable" hint. Cross-origin iframes need the `geolocation` Permissions-Policy allowed (for example `allow="geolocation"`).

## 5. Reality checks
- The browser uses the best available source on the device (for example GPS or Wi-Fi), so accuracy varies - show the `accuracy` radius.
- Requires a secure context (HTTPS).
- Treat coordinates as personal data (check your jurisdiction's privacy law): state the purpose, do not log precise values, round before storing.

## Verify
DevTools > Sensors panel overrides location and can simulate "Location unavailable"; test denied, timeout and success paths.

## Checked

Checked 2026-10-26 against MDN Geolocation API, Geolocation.getCurrentPosition(), GeolocationPositionError and Permissions.query() (mdn/content main): secure-context requirement, `timeout` default Infinity, `maximumAge` default 0, `enableHighAccuracy` default false, error codes 1/2/3 (PERMISSION_DENIED, POSITION_UNAVAILABLE, TIMEOUT), the `geolocation` Permissions-Policy and the `geolocation` permission name. Removed the unconfirmed Safari prompt-frequency and kilometre-accuracy claims and repaired a damaged character in the Permissions example.

Method: documentation only; no commands were run.
