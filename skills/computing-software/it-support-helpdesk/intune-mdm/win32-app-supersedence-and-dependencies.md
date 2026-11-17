---
id: computing-software.it-support-helpdesk.intune-mdm.win32-app-supersedence-and-dependencies
name: win32-app-supersedence-and-dependencies
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, app-supersedence, app-dependencies, win32-app, app-upgrade, auto-update, intunewin, intune]
level: advanced
status: docs-checked
description: "Upgrade and chain Intune Win32 apps: supersedence with or without uninstall, auto-update of available apps, dependency auto-install, documented limits, detection traps."
sources:
  - "https://learn.microsoft.com/en-us/intune/app-management/deployment/configure-win32-supersedence"
  - "https://learn.microsoft.com/en-us/intune/app-management/deployment/add-win32"
  - "https://learn.microsoft.com/en-us/intune/app-management/deployment/troubleshoot-win32"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# win32-app-supersedence-and-dependencies

## Supersedence (new version replaces old)
On the new app: **Supersedence** tab > Add the old app > **Uninstall previous version**:
| Uninstall previous | Use when |
|---|---|
| Yes | Replacing with an entirely different app, or the new installer doesn't remove the old one |
| No | The new installer updates the old version itself (app update) |

Behaviour:
- With Uninstall previous = Yes and a Required superseding app, the superseded app is
  uninstalled even if it isn't targeted, and the superseding app installs.
- Auto-update: set a supersedence relationship and tick **Auto-update** on an *Available for
  enrolled devices* assignment. It applies only to Available intent, not Required, and
  needs two available check-ins (commonly 8-16 hours in total).
- Docs state a maximum of 10 nodes in a supersedence relationship or chain (another
  section says 11 in one graph); retire old versions instead of chaining forever.
- Enforcement prefers supersedence over dependency if both conflict.

## Dependencies (prerequisites)
On the app: **Dependencies** tab > add apps that must be present (e.g. VC++ runtime,
.NET, a VPN client before its plugin). For each choose **Automatically install** Yes/No:
- Yes (the default): Intune installs the dependency first even if it isn't assigned.
- No: the dependency must already be present.

Dependencies must themselves be Win32 apps (not MSI LOB or Store apps). The docs state a
maximum of 100 dependencies, counting dependencies of dependencies and the app itself. An
app in a dependency relationship can't be deleted until the relationship is removed.

## Detection rules make or break both
- Review detection rules after any supersedence update. If detection still finds the old
  app after replacement, the superseding app won't install.
- New app detection should not match the old version (version-based rules rather than
  "folder exists").

## Troubleshooting
- Agent logs are under `<PROGRAMDATA>\Microsoft\IntuneManagementExtension\Logs`;
  `AppWorkload.log` is the main app log (check-ins, installs, applicability, detection).
  View with CMTrace.
- Device install status per app in Intune > Apps > app > Device install status.

## Gotchas
- Uninstall previous version runs the old app's uninstall command: test it silently first.
- Supersedence applies to Win32 apps.
- Win32 apps with dependencies don't show an uninstall option in Company Portal.

## Verify
A pilot device with the old version receives the new one, old detection no longer
matches, the dependency installs first in the IME log, and the device install status
shows Installed for the new app only.

## Checked
2026-11-01. Confirmed against the Intune Learn pages on Win32 supersedence, adding Win32
apps and troubleshooting Win32 apps: Uninstall previous behaviour, Available-only
auto-update with two check-ins, node limits, 100-dependency limit, default automatic
install, log location. Removed: the 0x87D1041C meaning, the MSI LOB supersedence claim,
example detection expressions and the IME log wording that the pages did not state.
Method: documentation only; no commands were run.
