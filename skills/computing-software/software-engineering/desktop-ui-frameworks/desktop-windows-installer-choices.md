---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-windows-installer-choices
name: desktop-windows-installer-choices
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-windows-installer-choices, desktop-installers, installer, code-signing, windows, macos, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Choose MSIX, WiX MSI, NSIS or Inno Setup for a desktop app."
sources:
  - https://learn.microsoft.com/en-us/windows/msix/
  - https://wixtoolset.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Windows installer choices

**Goal:** right installer for the audience.

```text
MSIX: clean uninstall, auto-update via App Installer, Store; needs signing; some sandbox limits
WiX (MSI): enterprise/GPO deployment, per-machine; wix build Product.wxs -o App.msi
NSIS / Inno Setup: flexible scripted setups; sign both the installer and the exe inside
Per-user installs (no admin) suit auto-updating apps; per-machine suits managed fleets
```

**Gotcha:** An installer signed but containing unsigned binaries still triggers SmartScreen and AV warnings; sign every exe and dll.

## Verify
- Install, upgrade and uninstall leave no files or registry keys behind.
