---
id: computing-software.web-development.frontend-development.postmessage-origin-validation
name: postmessage-origin-validation
category: computing-software
field: web-development
product: frontend-development
tags: [postmessage-origin, cross-window-messaging, iframe-security, messagechannel, dom-xss, security]
level: practitioner
status: docs-checked
description: "Secure cross-window messaging with postMessage: exact targetOrigin, validating event.origin and event.source, message schemas, MessageChannel handshakes and popup flows."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage
  - https://developer.mozilla.org/en-US/docs/Web/API/MessageChannel
  - https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cross-Origin-Opener-Policy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# postMessage origin validation

## 1. Sending
```js
iframe.contentWindow.postMessage({ type: "init", token }, "https://widget.example.com");   // never "*" with secrets
```
MDN: always specify an exact target origin, not `"*"`; a malicious site can change the location of the target window without your knowledge, and would then receive the data. (`"*"` is required only for `data:` URL contexts, which have opaque origins.)

## 2. Receiving
```js
const WIDGET_ORIGIN = "https://widget.example.com";
addEventListener("message", (e) => {
  if (e.origin !== WIDGET_ORIGIN) return;                  // exact string match
  if (e.source !== iframe.contentWindow) return;           // the specific frame, not any window of that origin
  const msg = e.data;
  if (typeof msg !== "object" || msg === null) return;
  switch (msg.type) {
    case "resize": if (Number.isFinite(msg.height)) iframe.style.height = `${Math.min(msg.height, 5000)}px`; break;
    default: return;
  }
});
```
- Compare `e.origin` for exact equality (MDN: verify the sender with `origin` and possibly `source`); substring checks such as `origin.includes(...)` would accept `https://widget.example.com.evil.net`.
- Treat data as untrusted: no `innerHTML`, `eval` or `location = msg.url` without validation.

## 3. Private channel after a handshake
```js
const { port1, port2 } = new MessageChannel();
iframe.contentWindow.postMessage({ type: "connect" }, WIDGET_ORIGIN, [port2]);
port1.onmessage = (e) => handle(e.data);            // port2 was transferred to the target window; messages arrive from whoever holds it
```

## 4. Popups (OAuth, payments)
- Popup posts the result to `window.opener` with the opener's exact origin; the opener validates `e.origin` and a `state` nonce it generated.
- `Cross-Origin-Opener-Policy: same-origin` puts the page in a separate browsing context group so cross-origin popups lose their opener relationship; MDN names `same-origin-allow-popups` for flows that use a cross-origin OAuth or payments service, or use a redirect-based flow.

## Verify
- [ ] A test page on another origin posting messages to your window is ignored (no state change, no errors thrown).

## Checked
Checked 2026-10-26 against MDN Window.postMessage (targetOrigin never `*` except data: URLs, verify origin and source, transfer parameter), MDN COOP (separate browsing context group; same-origin-allow-popups for OAuth or payments) and MessageChannel. Removed the unconfirmed 'listen for any message' libraries remark and the overstated claim that a port channel is private to its holder; the example code was not run.

Method: documentation only; no commands were run.
