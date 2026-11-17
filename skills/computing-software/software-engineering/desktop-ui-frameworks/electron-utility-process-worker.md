---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-utility-process-worker
name: electron-utility-process-worker
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-utility-process-worker, electron-process-model, electron, nodejs, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Offload CPU or crash-prone work to utilityProcess instead of the main process."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/process-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron utilityProcess for heavy work

**Goal:** keep the main process responsive.

```javascript
const { utilityProcess, MessageChannelMain } = require('electron');
const child = utilityProcess.fork(path.join(__dirname, 'worker.js'));
const { port1, port2 } = new MessageChannelMain();
child.postMessage({ type: 'init' }, [port1]);
win.webContents.postMessage('worker-port', null, [port2]);   // renderer talks to worker directly
child.on('exit', (code) => { /* restart or report */ });
```

**Gotcha:** `utilityProcess.fork` runs in the main process only and creates a child with Node.js and message ports enabled, a counterpart to `child_process.fork`. Transfer ports with `child.postMessage(message, [port])` and listen for the `exit` event so a crashed worker is noticed.

## Verify
- The `exit` handler fires when the worker is killed and the app keeps running.

## Checked
2026-11-03. Confirmed in the Electron `utilityProcess` and `MessageChannelMain` API pages and the message ports tutorial: `utilityProcess.fork(modulePath)`, `child.postMessage(message, [transfer])` with a `MessageChannelMain` port, `webContents.postMessage` to hand the other port to the renderer, the `exit` event, and the Node.js and message-port capabilities. Removed: the "Electron 22" version gate and the "no UI" statement (not in the page read), and the claim that the renderer notices a closed port.
Method: documentation only; no commands were run.
