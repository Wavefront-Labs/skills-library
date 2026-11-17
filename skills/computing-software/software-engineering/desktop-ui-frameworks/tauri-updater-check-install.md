---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-updater-check-install
name: tauri-updater-check-install
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-updater-check-install, tauri-updater, tauri, tauri2, updater, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Call check, downloadAndInstall and relaunch with the Tauri updater plugin and grant its permissions."
sources:
  - https://v2.tauri.app/plugin/updater/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri updater check and install

**Goal:** in-app update flow.

```javascript
import { check } from '@tauri-apps/plugin-updater';
import { relaunch } from '@tauri-apps/plugin-process';
const update = await check();
if (update) {
  await update.downloadAndInstall((event) => console.log(event.event)); // Started, Progress, Finished
  await relaunch();
}
// capabilities: "updater:default" (and the process plugin's restart permission for relaunch)
```

**Gotcha:** on Windows the application exits automatically when the install step runs (an installer limitation), so save state first or use the Rust `on_before_exit` hook. Restarting immediately is not required. The signature check cannot be disabled.

## Verify
- Version N upgrades to N+1 and reports the new version.

## Checked
2026-11-03. Confirmed in the Tauri updater plugin page: `check` from `@tauri-apps/plugin-updater`, `relaunch` from `@tauri-apps/plugin-process`, `downloadAndInstall` with the Started / Progress / Finished events, `updater:default` including check, download, install and download-and-install, the Windows automatic exit and `on_before_exit`, optional restart, and mandatory signatures. Removed: the exact `process:allow-restart` identifier (the page does not name the process plugin's permission) and the claim that `check()` returns null when there is no update (the page only shows an `if (update)` test).
Method: documentation only; no commands were run.
