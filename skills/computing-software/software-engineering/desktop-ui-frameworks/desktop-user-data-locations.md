---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-user-data-locations
name: desktop-user-data-locations
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-user-data-locations, desktop-settings-storage, settings, storage, appdata, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Store config in per-user app data folders, not the install directory."
sources:
  - https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder
  - https://doc.qt.io/qt-6/qstandardpaths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# User data and config locations

**Goal:** correct, writable paths.

```text
Qt 6 QStandardPaths (first entry is the writable location), per the Qt docs table:
  Windows  AppDataLocation   <USER>/AppData/Roaming/<APPNAME>
           AppLocalDataLocation <USER>/AppData/Local/<APPNAME>
           CacheLocation     <USER>/AppData/Local/<APPNAME>/cache
  macOS    AppDataLocation   ~/Library/Application Support/<APPNAME>
           CacheLocation     ~/Library/Caches/<APPNAME>
           AppConfigLocation ~/Library/Preferences/<APPNAME>
  Linux    AppDataLocation   ~/.local/share/<APPNAME>
           AppConfigLocation ~/.config/<APPNAME>
           CacheLocation     ~/.cache/<APPNAME>
.NET: Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData | LocalApplicationData | CommonApplicationData)
```

- Qt: `QStandardPaths::writableLocation(type)` returns the directory where files should be written, typically user-scoped and, for application-specific types, scoped to the calling application. On Windows `AppDataLocation` is the roaming path; `AppLocalDataLocation` is the local one. Cached (non-essential) data goes under `CacheLocation`; configuration under `AppConfigLocation`.
- .NET: `ApplicationData` is the repository for application-specific data of the current roaming user; `LocalApplicationData` is for the current non-roaming user; `CommonApplicationData` is shared by all users. Applications should not create files at the `UserProfile` level and should put data under `ApplicationData` locations instead.
- Never write into the install directory; keep config in the per-user locations above.
- On sandboxed macOS apps the home directory is transparently redirected to a per-application container, so `~` resolves inside it.

## Verify
- The app runs as a standard user and survives an upgrade with settings intact.

## Checked

Checked 2026-11-09 against the Qt 6 QStandardPaths page (enum and per-platform table sections) and the .NET Environment.SpecialFolder page on Microsoft Learn.
Confirmed: every path and rule above.
Removed as unconfirmed: the `XDG_CONFIG_HOME` variable names, Electron `app.getPath('userData')`, Tauri `app_config_dir()`, the Program Files read-only and MSIX write-redirect gotcha.

Method: documentation only; no commands were run.
