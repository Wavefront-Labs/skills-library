---
id: computing-software.software-engineering.desktop-ui-frameworks.tauri-bundle-targets
name: tauri-bundle-targets
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [tauri-bundle-targets, tauri-distribution, tauri, packaging, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Choose bundle targets (msi, nsis, app, dmg, deb, rpm, appimage) and the WebView2 install mode in tauri.conf.json."
sources:
  - https://v2.tauri.app/distribute/
  - https://v2.tauri.app/start/prerequisites/
  - https://v2.tauri.app/reference/config/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Tauri bundle targets

**Goal:** platform installers.

```bash
npm run tauri build -- --bundles nsis      # build, bundling only the listed formats
npm run tauri build -- --no-bundle         # build without bundling; bundle later with `tauri bundle`
```

```json
// src-tauri/tauri.conf.json
"bundle": {
  "active": true,
  "targets": ["nsis", "msi", "dmg", "deb", "appimage"],
  "icon": ["icons/icon.ico"],
  "windows": { "webviewInstallMode": { "type": "downloadBootstrapper" } }
}
```

**Gotcha:** valid `targets` values are `all`, `deb`, `rpm`, `appimage`, `msi`, `nsis`, `app` and `dmg` (case insensitive). In the reference config `bundle.active` defaults to `false`, so set it to `true` to produce bundles. MSI packaging needs extra Windows tooling (see the prerequisites page). `downloadBootstrapper` is the default WebView2 install mode and needs an internet connection at install time. Most platforms require code signing.

## Verify
- The bundle installs and the app opens with its icon.

## Checked
2026-11-03. Confirmed in the Tauri distribute page, prerequisites page and configuration reference: `tauri build` with `--bundles` and `--no-bundle`, the `BundleType` values, `bundle.targets`, `bundle.icon`, `bundle.active` default, `webviewInstallMode` with `downloadBootstrapper` as the default, and the MSI prerequisite note. Removed: the `tauri icon` helper and the "bundles build only for the host OS" claim (the page only notes `signtool.exe` is Windows-only for signing), plus the earlier unlisted formats.
Method: documentation only; no commands were run.
