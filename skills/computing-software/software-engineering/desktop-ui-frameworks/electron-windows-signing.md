---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-windows-signing
name: electron-windows-signing
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-windows-signing, electron-packaging, electron, packaging, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Sign Windows Electron builds with the windowsSign option and a cloud or hardware-backed certificate."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/code-signing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron Windows code signing

**Goal:** a signed app and installer that Windows does not treat as unsigned.

```javascript
// @electron/packager; electron-winstaller, electron-wix-msi and Forge take the same windowsSign options
const packager = require('@electron/packager');
packager({
  dir: '/path/to/my/app',
  windowsSign: {
    signWithParams: '--my=custom --parameters',   // arguments for your signing tool
    signToolPath: 'C:\\Path\\To\\my-custom-tool.exe', // omit to use signtool.exe
  },
});
```

**Gotcha:** since June 2023 Microsoft requires an extended validation (EV) code signing certificate. Older OV or software-based certificates make Windows treat the app as unsigned. EV keys must live on a hardware module (FIPS 140 Level 2, Common Criteria EAL 4+ or equivalent), so a key file cannot simply be downloaded onto CI. Use a provider's cloud-based signing with a command-line signing tool, or Azure Artifact Signing, and point `signToolPath` and `signWithParams` at it.

## Verify
- The installer and the app executable show your publisher in file properties, and Windows shows no unsigned-app warning.

## Checked
2026-11-03. Confirmed in the Electron code signing tutorial: the `windowsSign` property from `@electron/windows-sign` shared by Forge, `@electron/packager`, `electron-winstaller` and `electron-wix-msi`, its `signWithParams` and `signToolPath` options, the June 2023 EV requirement, the hardware-module rule, and cloud signing for CI. Removed: raw `signtool` command lines and the DigiCert timestamp URL, the "always timestamp" rule and `win.signtoolOptions` (not in the pages read).
Method: documentation only; no commands were run.
