---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-forge-makers
name: electron-forge-makers
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-forge-makers, electron-packaging, electron, packaging, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Create installers with Electron Forge makers configured in forge.config.js."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/application-distribution
  - https://www.electronforge.io/
  - https://www.electronforge.io/config/makers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron Forge makers

**Goal:** repeatable packaging.

```bash
npx create-electron-app@latest myapp --template=vite
cd myapp && npm run make
```

```javascript
// forge.config.js
module.exports = {
  packagerConfig: { asar: true },
  makers: [
    { name: '@electron-forge/maker-squirrel' },                          // Windows
    { name: '@electron-forge/maker-zip', platforms: ['darwin', 'linux'] },
    { name: '@electron-forge/maker-dmg' },                                // macOS
  ],
};
```

**Gotcha:** Squirrel.Windows launches the app with `--squirrel-firstrun` right after installation and holds a file lock for a few seconds. Do not check for updates when `process.argv` contains that flag, or the check fails.

## Verify
- `make` produces the installers for the current platform and they install on a clean machine.

## Checked
2026-11-03. Confirmed in the Electron Forge docs (getting started, configuration, makers, Windows signing) and the Electron autoUpdater API page: `create-electron-app` with `--template=vite`, `packagerConfig` with `asar: true`, maker names `@electron-forge/maker-squirrel`, `-zip`, `-dmg`, the `platforms` property, and the `--squirrel-firstrun` behaviour. The `make` script is named by the getting-started page. Removed: `electron-forge package` as a separate step, deb/rpm makers and the `out/make` path (not confirmed), and the earlier wrong claim that ignoring the flag runs the app during install.
Method: documentation only; no commands were run.
