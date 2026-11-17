---
id: computing-software.software-engineering.tauri.tauri-csp
name: tauri-csp
category: computing-software
field: software-engineering
product: tauri
tags: [csp, tauri, security, webview]
level: practitioner
status: docs-checked
description: "Enable and tailor the Content Security Policy in the Tauri configuration to restrict what the webview can load."
sources:
  - "https://v2.tauri.app/security/csp/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tauri Content Security Policy

Goal: restrict the webview's CSP to reduce the impact of web vulnerabilities such as cross-site scripting (XSS).

## How it works

- Local scripts are hashed; styles and external scripts use a cryptographic nonce, so unallowed content is not loaded.
- CSP protection is only enabled if it is set in the Tauri configuration file.
- At compile time Tauri appends its nonces and hashes to the relevant CSP attributes of bundled code and assets, so you only configure what is unique to your app.

## Method

Make the policy as restricted as possible, allowing the webview to load assets only from hosts you trust, preferably your own. Avoid remote content such as scripts served from a CDN, since it is an attack vector; any untrusted file can introduce subtle ones.

Example from Tauri's `api` example (tailor it to your app):

```json
  "csp": {
        "default-src": "'self' customprotocol: asset:",
        "connect-src": "ipc: http://ipc.localhost",
        "font-src": ["https://fonts.gstatic.com"],
        "img-src": "'self' asset: http://asset.localhost blob: data:",
        "style-src": "'unsafe-inline' 'self' https://fonts.googleapis.com"
      },
```

If the frontend is written in Rust or otherwise uses WebAssembly, include `'wasm-unsafe-eval'` as a `script-src`.

For details see MDN on `script-src`, `style-src` and CSP sources.

## Checked
2026-11-07. Confirmed claim by claim against https://v2.tauri.app/security/csp/ (page text including code blocks and tabs read in full).
Method: documentation only; no commands were run.
