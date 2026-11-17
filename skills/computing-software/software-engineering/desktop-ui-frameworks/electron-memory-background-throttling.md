---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-memory-background-throttling
name: electron-memory-background-throttling
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-memory-background-throttling, electron-performance, electron, performance, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Measure per-process memory with app.getAppMetrics and control background throttling of hidden windows."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/performance
  - https://www.electronjs.org/docs/latest/api/web-contents
  - https://www.electronjs.org/docs/latest/api/browser-window
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron memory and background throttling

**Goal:** lighter always-on apps.

```javascript
// main process
win.on('hide', () => win.webContents.setBackgroundThrottling(true));
setInterval(() => console.log(app.getAppMetrics()), 60000);   // memory and CPU for every app process
```

**Gotcha:** if the `backgroundThrottling` web preference is off, the page's visibility state stays `visible` even when the window is minimized, occluded or hidden, so a hidden window keeps running at full rate. Pause expensive work yourself when visibility is `hidden`.

## Verify
- With throttling on, timers in a hidden window slow down; `app.getAppMetrics()` shows memory per process over time.

## Checked
2026-11-03. Confirmed in the Electron `app`, `webContents` and `BrowserWindow` API pages: `app.getAppMetrics()` returning `ProcessMetric[]` of memory and CPU statistics, `contents.setBackgroundThrottling(allowed)`, the `hide` event, and the page visibility behaviour when `backgroundThrottling` is disabled. Removed: the per-window "tens of MB" figure, the 24-hour idle check, the Chromium task manager advice, the share-one-hidden-window advice, and the `m.memory.workingSetSize` field path (the `ProcessMetric` structure page was not read).
Method: documentation only; no commands were run.
