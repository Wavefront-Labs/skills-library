---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-main-renderer-processes
name: electron-main-renderer-processes
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-main-renderer-processes, electron-process-model, electron, nodejs, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Structure an app around one main process and sandboxed renderer windows."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/process-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron main and renderer processes

**Goal:** correct separation of privileged and UI code.

```javascript
// main.js
const { app, BrowserWindow } = require('electron');
const path = require('node:path');
function create() {
  const win = new BrowserWindow({
    width: 1000, height: 700,
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, sandbox: true }
  });
  win.loadFile('index.html');
}
app.whenReady().then(create);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
```

**Gotcha:** the main process houses the UI thread and handles windows and OS interaction, so a long-running operation there freezes the whole app. Prefer asynchronous `fs` and `child_process` calls, avoid synchronous IPC and `@electron/remote`, and move CPU-heavy work to worker threads, a window or a dedicated process.

## Verify
- The window stays responsive while a long task runs elsewhere.

## Checked
2026-11-03. Confirmed in the Electron process model tutorial, the performance tutorial (item 3, blocking the main process) and the `BrowserWindow` API page: the multi-process model, the `window-all-closed` / `process.platform !== 'darwin'` pattern, `win.loadFile`, and the advice on blocking work. The sandbox default is covered by the sandbox tutorial (Electron 20 onward) and context isolation by its tutorial (default since Electron 12). Removed: the Task Manager check and the "owns the event loop for menus and IPC" wording.
Method: documentation only; no commands were run.
