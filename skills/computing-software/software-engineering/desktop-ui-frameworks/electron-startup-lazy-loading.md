---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-startup-lazy-loading
name: electron-startup-lazy-loading
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-startup-lazy-loading, electron-performance, electron, performance, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Cut Electron startup time by deferring heavy requires, showing the window on ready-to-show and bundling code."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/performance
  - https://www.electronjs.org/docs/latest/api/browser-window
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron startup performance

**Goal:** fast first window.

```javascript
// defer heavy modules until first use (require has a module cache, so only the first call is expensive)
ipcMain.handle('export', async () => (await import('./exporter.js')).run());
// show the window once the renderer has rendered its first frame
const win = new BrowserWindow({ show: false });
win.once('ready-to-show', () => win.show());
```

**Gotcha:** loading modules is expensive, especially on Windows, so besides deferring work, bundle your main and renderer code into a single file so the `require()` overhead is paid once. Electron does not recommend a particular bundler; pick one that handles both Node.js and browser environments.

## Verify
- Measure before and after (the Electron docs say to measure first); time to first paint drops after bundling and deferring.

## Checked
2026-11-03. Confirmed in the Electron performance tutorial (just-in-time loading, module cost on Windows, bundle your code, measure first) and the `BrowserWindow` page (`show: false` with the `ready-to-show` event). Removed: the `console.time`, `node --cpu-prof` and `app.getAppMetrics` measuring line and the asar-read-speed explanation (not in the pages read).
Method: documentation only; no commands were run.
