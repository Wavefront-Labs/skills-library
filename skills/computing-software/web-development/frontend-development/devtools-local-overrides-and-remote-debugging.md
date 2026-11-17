---
id: computing-software.web-development.frontend-development.devtools-local-overrides-and-remote-debugging
name: devtools-local-overrides-and-remote-debugging
category: computing-software
field: web-development
product: frontend-development
tags: [devtools, local-overrides, remote-debugging, chrome-devtools, safari-web-inspector, mobile-debugging, remote-debugging-ios, android-remote-debugging]
level: practitioner
status: docs-checked
description: "Using DevTools local overrides to patch production files and headers, and remote-debugging Android Chrome and iOS Safari from desktop over USB or Wi-Fi."
sources:
  - https://developer.chrome.com/docs/devtools/overrides
  - https://developer.chrome.com/docs/devtools/remote-debugging
  - https://developer.apple.com/documentation/safari-developer-tools/inspecting-ios
  - https://developer.mozilla.org/en-US/docs/Tools/about:debugging
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Local overrides and remote debugging

## 1. Local overrides (Chrome/Edge)
Test a fix against production without deploying:
1. Sources > Overrides > Select folder for overrides, allow access.
2. Network panel: right-click a request > **Override content** (or Override headers). Edit the file; DevTools serves your copy on reload (purple dot marks overridden files).
3. **Override headers**: add/modify response headers, e.g. try a stricter CSP, `Cache-Control`, or CORS headers before changing the server. Stored in `.headers` files.
4. Also mock a failing API: override a JSON response with an error body.
Overrides persist across reloads until disabled - remember to switch them off.

## 2. Android remote debugging
1. Phone: enable USB debugging in Developer options.
2. Desktop Chrome: open `chrome://inspect#devices` and follow the Chrome remote-debugging page.
3. Each remote Chrome tab, and each app using WebView, gets its own section there to inspect.

## 3. iOS Safari
Enable Web Inspector on the iPhone and the developer features in Mac Safari, then pick the device in the Develop menu. Menu paths change by OS version: follow Apple's "Inspecting iOS" documentation (not verified in this review).

## 4. Quick dev-server access on devices
Bind the dev server to the LAN (see your dev server's host option) and open `http://<laptop-ip>:<port>`. APIs needing secure contexts (camera, service workers, clipboard) require HTTPS or localhost.

## Verify
Override a production CSS file and see the change; inspect a real phone tab and capture a Performance trace from it.

## Checked
2026-10-28. Confirmed: Chrome DevTools overrides page (Network panel Override content/headers, `.headers` files, purple dot) and Chrome remote-debugging page (`chrome://inspect#devices`, per-tab and WebView sections). Removed: Safari/Firefox override claims, RSA prompt, port-forwarding detail, WebView and WKWebView flags, iOS menu paths and version, dev-server flags (not on fetched pages).
Method: documentation only; no commands were run.
