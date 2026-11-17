---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-ipc-invoke-handle
name: electron-ipc-invoke-handle
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-ipc-invoke-handle, electron-ipc, electron, ipc, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Use request-response IPC with invoke/handle and validate inputs."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/ipc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron ipcMain.handle and invoke

**Goal:** typed, safe renderer-to-main calls.

```javascript
// main
ipcMain.handle('file:read', async (event, name) => {
  if (!isTrusted(event.senderFrame)) throw new Error('untrusted sender');
  if (typeof name !== 'string' || name.includes('..')) throw new Error('bad name');
  return fs.promises.readFile(path.join(app.getPath('userData'), name), 'utf8');
});
// renderer via preload: await window.api.readFile('notes.txt')
```

**Gotcha:** Treat every argument as hostile input and verify event.senderFrame URL, since any frame can call exposed channels.

## Verify
- Calling with ../ or from an iframe is rejected.

## Checked
2026-11-03. Confirmed in the Electron security tutorial (checklist item 17, validate the sender of all IPC messages, using `e.senderFrame`), the IPC tutorial (`ipcMain.handle` with `ipcRenderer.invoke`, and not exposing the raw API) and the `app.getPath` entry for `userData`. `isTrusted` stands for your own origin allow-list check (the docs call theirs `validateSender`). The docs suggest keeping app files in a subdirectory of `userData`.
Method: documentation only; no commands were run.
