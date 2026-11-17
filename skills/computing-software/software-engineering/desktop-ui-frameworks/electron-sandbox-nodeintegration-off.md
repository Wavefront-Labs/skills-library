---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-sandbox-nodeintegration-off
name: electron-sandbox-nodeintegration-off
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-sandbox-nodeintegration-off, electron-preload-isolation, electron, security, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Keep nodeIntegration false, contextIsolation true and sandbox on for renderers."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/context-isolation
  - https://www.electronjs.org/docs/latest/tutorial/sandbox
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron sandbox and nodeIntegration off

**Goal:** a renderer that cannot reach the OS.

```javascript
new BrowserWindow({ webPreferences: {
  nodeIntegration: false,        // default false
  contextIsolation: true,        // default true since Electron 12
  sandbox: true,                 // default true since Electron 20
  webSecurity: true              // never disable in production
}});
// sandboxed preload: require() loads only the electron module (contextBridge, crashReporter,
// ipcRenderer, nativeImage, webFrame, webUtils); no Node built-ins, Buffer or setImmediate
```

**Gotcha:** `nodeIntegration: true` also disables the sandbox for that renderer. Turning the sandbox off to use Node modules hides the real fix: do that work in the main process behind IPC. Even with `nodeIntegration: false`, strong isolation needs `contextIsolation` on too.

## Verify
- `require` is undefined in the renderer console, and a sandboxed preload cannot `require('fs')`.

## Checked
2026-11-03. Confirmed in the Electron sandbox, context isolation and security tutorials: context isolation default since Electron 12, sandbox default since Electron 20, `nodeIntegration: true` disabling the sandbox, the sandboxed preload `require` limited to the electron module and its listed renderer modules, and the advice not to disable `webSecurity` in production. Removed: the `events`, `timers` and `url` modules (not available to a sandboxed preload; use the Web API equivalents). The process model tutorial confirms Node.js in renderers was historically the default and is now disabled.
Method: documentation only; no commands were run.
