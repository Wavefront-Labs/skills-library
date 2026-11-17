---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-ipc-messageport-streams
name: electron-ipc-messageport-streams
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-ipc-messageport-streams, electron-ipc, electron, ipc, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Push events from main with webContents.send and use MessagePorts for streams."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/ipc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron MessagePort and main-to-renderer messages

**Goal:** event streams and direct channels.

```javascript
win.webContents.send('progress', 42);
// two-way direct channel between main and renderer
const { port1, port2 } = new MessageChannelMain();
port2.on('message', (e) => console.log(e.data));
port2.start();
win.webContents.postMessage('port', null, [port1]);
// preload: ipcRenderer.on('port', (e) => { e.ports[0].onmessage = (m) => ... });
```

**Gotcha:** with context isolation on, `webContents.postMessage` delivers to the preload's isolated world, not the page. To reach the page's main world, the preload must forward the port with `window.postMessage('main-world-port', '*', event.ports)`.

## Verify
- A message posted on one end arrives on the other, including one posted before the listener was registered (messages queue until a listener exists).

## Checked
2026-11-03. Confirmed in the Electron message ports tutorial and `MessageChannelMain` API page: `new MessageChannelMain()`, `webContents.postMessage(channel, message, [ports])`, `event.ports` in the receiver, `port2.on('message')` plus `port2.start()` in main, the queueing of early messages, and the context-isolation forwarding via `window.postMessage`. Removed: the claim that the channel connects to a utility process (the snippet did not do so), and the listener-leak gotcha with its 10-reload check (not in the docs).
Method: documentation only; no commands were run.
