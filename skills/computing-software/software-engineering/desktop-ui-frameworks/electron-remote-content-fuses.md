---
id: computing-software.software-engineering.desktop-ui-frameworks.electron-remote-content-fuses
name: electron-remote-content-fuses
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [electron-remote-content-fuses, electron-security, electron, security, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Flip Electron fuses at package time to disable features such as ELECTRON_RUN_AS_NODE and load app code only from an asar."
sources:
  - https://www.electronjs.org/docs/latest/tutorial/fuses
  - https://www.electronjs.org/docs/latest/tutorial/security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Electron fuses

**Goal:** harden the shipped binary.

```bash
npm i -D @electron/fuses
```

```javascript
const { flipFuses, FuseVersion, FuseV1Options } = require('@electron/fuses');
flipFuses(require('electron'), {   // path to the electron binary to flip
  version: FuseVersion.V1,
  [FuseV1Options.RunAsNode]: false,
  [FuseV1Options.EnableNodeCliInspectArguments]: false,
  [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
  [FuseV1Options.OnlyLoadAppFromAsar]: true,
});
```

**Gotcha:** fuses are flipped at package time, before code signing. The OS signature check is what stops anyone flipping them back, so flip first and sign afterwards. `EnableEmbeddedAsarIntegrityValidation` works on macOS and Windows only, and `OnlyLoadAppFromAsar` is meant to be paired with it.

## Verify
- With `RunAsNode` disabled, `ELECTRON_RUN_AS_NODE` is ignored by the packaged app.

## Checked
2026-11-03. Confirmed in the Electron fuses tutorial: `flipFuses`, `FuseVersion.V1`, `FuseV1Options.RunAsNode`, `EnableNodeCliInspectArguments`, `EnableEmbeddedAsarIntegrityValidation` (macOS and Windows), `OnlyLoadAppFromAsar`, flipping before code signing, and the `ELECTRON_RUN_AS_NODE` behaviour. Removed: the claim that flipping afterwards "breaks signatures" (the docs say to flip before signing so the OS can validate it) and the bare `npm`/JS mix in one bash block.
Method: documentation only; no commands were run.
