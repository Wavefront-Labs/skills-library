---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-contextbridge-preload
name: electron-contextbridge-preload
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-contextbridge-preload, electron-preload-isolation, electron, security, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Expose a minimal safe API from preload with contextBridge."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/context-isolation
  - https://www.electronjs.org/docs/latest/tutorial/sandbox
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron contextBridge preload

**Goal:** renderer gets capabilities, not Node.

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require('electron');
contextBridge.exposeInMainWorld('api', {
  openFile: () => ipcRenderer.invoke('dialog:open'),
  onProgress: (cb) => { const h = (_e, v) => cb(v); ipcRenderer.on('progress', h); return () => ipcRenderer.off('progress', h); }
});
// renderer: const text = await window.api.openFile();
```

**Gotcha:** Never expose ipcRenderer or send directly; wrap each channel in a function, because an exposed raw ipcRenderer lets any script call any channel.

## Verify
- In the renderer console, `window.api` lists only the wrapped functions and `window.ipcRenderer` is undefined.

## Checked
2026-11-03. Confirmed in the Electron IPC tutorial, context isolation tutorial, security checklist item 20 and the `ipcRenderer` API page: `contextBridge.exposeInMainWorld`, `ipcRenderer.invoke`, `ipcRenderer.on`/`off` (`off` is the documented name, `removeListener` its alias), and the rule to expose one method per IPC message rather than the raw API. The callback wrapper drops `event` as the docs advise. Removed: the `typeof require` check (not stated for this setup).
Method: documentation only; no commands were run.
