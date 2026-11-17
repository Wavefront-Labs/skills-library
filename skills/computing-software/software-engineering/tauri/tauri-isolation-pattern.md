---
id: computing-software.software-engineering.tauri.tauri-isolation-pattern
name: tauri-isolation-pattern
category: computing-software
field: software-engineering
product: tauri
tags: [isolation-pattern, tauri, security, ipc]
level: advanced
status: docs-checked
description: "Add a sandboxed Isolation application to a Tauri app to intercept, validate and encrypt all frontend IPC messages before they reach the Core."
sources:
  - "https://v2.tauri.app/concept/inter-process-communication/isolation/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Isolation pattern

Goal: intercept and modify every IPC message from the frontend, in JavaScript, before it reaches Tauri Core, to guard against untrusted frontend content (the main threat is Development Threats: deeply nested build-time and bundled dependencies). Tauri highly recommends it whenever possible; since it intercepts all messages it can always be used, including always-on APIs such as Events.

Use the hook to validate inputs, e.g. that a file read or write stays within expected paths, or that an HTTP fetch sets only the expected Origin header.

## How it works

A secure app runs in a sandboxed `<iframe>` alongside the frontend. Tauri forces all IPC calls through it first. The message is then encrypted with AES-GCM via the browser's SubtleCrypto, passed back, forwarded to Core, and decrypted there. New keys are generated every time the app runs.

Steps: IPC handler receives message; goes to the Isolation app; the hook runs and may modify it; it is encrypted with a runtime-generated key; returns to the IPC handler; goes to Core.

## Create the Isolation application

Assume `frontendDist` is `../dist` and the isolation app is in `../dist-isolation`.

`../dist-isolation/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Isolation Secure Script</title>
  </head>
  <body>
    <script src="index.js"></script>
  </body>
</html>
```

`../dist-isolation/index.js`:

```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  console.log('hook', payload);
  return payload;
};
```

## Configure `tauri.conf.json`

```json
{
  "build": { "frontendDist": "../dist" },
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": { "dir": "../dist-isolation" }
      }
    }
  }
}
```

## Limits and costs

- Encryption adds overhead versus the Brownfield pattern, which most apps will not notice.
- A key is generated at each start; in headless integration testing with WebDriver, install an entropy service such as `haveged` if the OS has none.
- External files do not load in sandboxed iframes on Windows, so Tauri inlines scripts relative to the Isolation app at build time. Plain `<script src>` works; ES Modules do not load.
- Keep the Isolation app and its dependencies and build steps minimal, to avoid supply chain attacks.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/concept/inter-process-communication/isolation/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
