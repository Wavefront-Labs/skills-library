---
id: computing-software.systems-network-administration.patch-management.intune-win32-app-supersedence
name: intune-win32-app-supersedence
category: computing-software
field: systems-network-administration
product: patch-management
tags: [intune-supersedence, win32-app, intune, intunewinapputil, third-party-patching, detection-rules]
level: practitioner
status: docs-checked
description: "Update third-party apps via Intune Win32 supersedence: IntuneWinAppUtil packaging, detection rules, uninstall-previous option, auto-update for available apps and graph limits."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-supersedence
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-win32-prepare
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating Win32 apps via Intune supersedence

**Goal:** replace old versions of an app with a new one across devices, without separate uninstall jobs.

## Package the new version
```cmd
IntuneWinAppUtil.exe -c <PKG_DIR>\7zip-24.08 -s 7z2408-x64.msi -o <PKG_DIR>\out
```
Upload as a Win32 app with install/uninstall commands (`msiexec /i 7z2408-x64.msi /qn`).

## Detection rule
Must identify the **new** version specifically (for example a version-aware file, MSI or registry rule). A detection rule that also matches the old version makes Intune think the update is already installed.

## Supersedence
In the new app: Supersedence > Add the old app. Option **Uninstall previous version**:
- Yes: Intune uninstalls the old app first (needed when versions install side by side or the vendor installer cannot upgrade).
- No: new installer runs over the old one (for installers that upgrade in place, such as most MSIs with proper upgrade codes).

## Assignment behaviour
- Devices with the superseded app **required**: the new app replaces it when the new app is assigned.
- **Auto-update** setting on available assignments upgrades devices that installed the old version from Company Portal.
- Limits: Microsoft documents a maximum of 10 nodes in a supersedence chain (a later section of the same page says 11 for a graph); keep chains short and retire old versions.
- Auto-update needs two available-app check-ins, so expect hours, not minutes, and it does not apply to required assignments.

## Gotchas
- When replacing a different app, turn Uninstall previous version on; if detection keeps finding the old app, the new one is not installed.
- Test on a pilot group first, and review detection rules after any update.

## Verify
Device install status shows the new app Installed and the old app Not applicable/Uninstalled; inventory reports only the new version.

## Checked
2026-11-01. Confirmed on the Intune Win32 supersedence and Win32 prepare pages: IntuneWinAppUtil -c, -s, -o parameters, the Uninstall previous version option and its update vs replacement meaning, the node limit (page is inconsistent, 10 vs 11), auto-update for Available assignments only, and the two check-in timing. Removed: the DisplayVersion detection example, the claim that separately assigned superseded apps are reinstalled, and the install-loop claim.
Method: documentation only; no commands were run.
