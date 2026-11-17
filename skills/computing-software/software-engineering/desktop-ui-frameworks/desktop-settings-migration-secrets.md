---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-settings-migration-secrets
name: desktop-settings-migration-secrets
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-settings-migration-secrets, desktop-settings-storage, settings, storage, appdata, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Version the settings schema, migrate on load and keep credentials in the OS store."
sources:
  - https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder
  - https://doc.qt.io/qt-6/qstandardpaths.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Settings versioning and secrets

**Goal:** safe upgrades and secret handling.

```text
settings.json: { "schema": 3, ... }  ->  load, run migrations 1->2->3, write atomically (temp file + rename)
Secrets: Windows Credential Manager / DPAPI, macOS Keychain, libsecret on Linux
APIs: Electron safeStorage.encryptString; Tauri stronghold or keyring crate; Qt: QtKeychain library; .NET ProtectedData
Never store tokens in plain JSON or localStorage
```

**Gotcha:** Writing settings in place can corrupt the file on a crash; write to a temp file and rename.

## Verify
- Opening a v1 settings file in the new build migrates without losing keys.
