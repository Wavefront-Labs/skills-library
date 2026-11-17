---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-updater-flow
name: electron-updater-flow
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-updater-flow, electron-updates, electron, updates, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Check, download and install updates with electron-updater events and autoDownload set to false."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/updates
  - https://www.electron.build/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# electron-updater update flow

**Goal:** controlled, safe updates.

```javascript
const { autoUpdater } = require('electron-updater');
autoUpdater.autoDownload = false;                       // default is true
autoUpdater.on('update-available', () => autoUpdater.downloadUpdate());
autoUpdater.on('update-downloaded', () => { /* ask user */ autoUpdater.quitAndInstall(); });
autoUpdater.on('error', (e) => console.error(e));
app.whenReady().then(() => autoUpdater.checkForUpdates());
```

**Gotcha:** the macOS app must be code signed for auto-update to work, and the `zip` target is required next to `dmg` (it is part of the default macOS targets) or `latest-mac.yml` is not created and `autoUpdater` errors. On Windows use the NSIS target: Squirrel.Windows is not supported by electron-updater. Test against a real installed copy.

## Verify
- Install version N, publish N+1, and the installed app updates in place.

## Checked
2026-11-03. Confirmed in the electron-builder auto-update guide and the electron-updater `AppUpdater` source: `autoDownload` (default `true`), `downloadUpdate()`, `checkForUpdates()`, `quitAndInstall()`, the `error`, `update-available` and `update-downloaded` events, signing required on macOS, the required `zip` target and `latest-mac.yml`, the auto-updatable targets (macOS DMG, Linux AppImage/DEB/Pacman/RPM, Windows NSIS), and no Squirrel.Windows support. Removed: the `log.error` call (no `log` was defined), and the claim that updates work "only on packaged" builds. The electron.build auto-update URL returned 404, so the source is the site root.
Method: documentation only; no commands were run.
