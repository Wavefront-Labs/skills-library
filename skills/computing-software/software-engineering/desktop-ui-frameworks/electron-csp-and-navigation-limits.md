---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-csp-and-navigation-limits
name: electron-csp-and-navigation-limits
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-csp-and-navigation-limits, electron-security, electron, security, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Set a Content-Security-Policy and block unexpected navigation and window creation."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron CSP and navigation limits

**Goal:** limit what injected content can do.

```javascript
session.defaultSession.webRequest.onHeadersReceived((d, cb) => cb({ responseHeaders: {
  ...d.responseHeaders, 'Content-Security-Policy': ["default-src 'self'; script-src 'self'"] } }));
app.on('web-contents-created', (_e, wc) => {
  wc.on('will-navigate', (e, url) => { if (new URL(url).origin !== 'app://local') e.preventDefault(); });
  wc.setWindowOpenHandler(({ url }) => { if (url.startsWith('https://')) shell.openExternal(url); return { action: 'deny' }; });
});
```

**Gotcha:** shell.openExternal with unvalidated URLs can launch arbitrary protocols; allow-list https: only.

## Verify
- Navigating to a remote origin or window.open is blocked.

## Checked
2026-11-03. Confirmed in the Electron security tutorial (checklist items on CSP, navigation, window creation and `shell.openExternal`): `session.defaultSession.webRequest.onHeadersReceived` for setting the header, the `web-contents-created` event, `will-navigate` with `preventDefault()`, `setWindowOpenHandler` returning `{ action: 'deny' }`, and the warning against `openExternal` with untrusted content. `app://local` is a placeholder for your app's own origin, not an Electron default.
Method: documentation only; no commands were run.
