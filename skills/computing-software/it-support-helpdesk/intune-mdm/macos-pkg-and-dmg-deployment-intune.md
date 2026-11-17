---
id: computing-software.it-support-helpdesk.intune-mdm.macos-pkg-and-dmg-deployment-intune
name: macos-pkg-and-dmg-deployment-intune
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-pkg-deployment, macos-lob-app, unmanaged-pkg, dmg-app, intune-agent, app-deployment]
level: practitioner
status: docs-checked
description: "Deploy macOS apps from Intune: LOB pkg vs unmanaged PKG vs DMG app types, size and signing limits, detection by bundle ID, pre/post scripts, assignment types and error codes."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/apps/macos-unmanaged-pkg"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/lob-apps-macos-dmg"
  - "https://learn.microsoft.com/en-us/mem/intune/apps/lob-apps-macos"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macos-pkg-and-dmg-deployment-intune

Intune has three ways to push a non-store Mac app. Picking the wrong one is the usual cause of failed installs. Add each at Apps > All Apps > Create > platform macOS.

## App types
| Type (app type name) | Limits and requirements | Assignment types |
|---|---|---|
| **macOS app (PKG)** (unmanaged PKG) | Device managed by Intune; PKG under 8 GB; Intune management agent for macOS 2308.006 or later; the PKG must run with the `installer` command in Terminal. Handles nonflat, component, unsigned and payload-less packages, packages that install outside /Applications, and custom packages with scripts | Required, Available (no Uninstall) |
| **Line-of-business app** (.pkg) | 2 GB maximum per app; needs a logo or it does not show in the apps list; .pkg must be a component package or a package of multiple packages, contain no bundle, disk image or .app file, be signed with a "Developer ID Installer" certificate, and contain a payload (payload-less packages attempt to reinstall while assigned) | Required, Available for enrolled devices, Uninstall (only when Install as managed = Yes) |
| **macOS app (DMG)** | DMG under 8 GB; must contain one or more `.app` files (other installer types will not install); Intune management agent for macOS installed; full disk access is needed to update or delete DMG apps and Intune requests it automatically on macOS 13 and later | Required (installs to /Applications), Available, Uninstall |

Use the DMG type for .dmg or .app files; the LOB type only takes .pkg. Wrapped .intunemac uploads were removed in August 2022.

## Settings that matter
- **Included apps**: bundle IDs and build numbers detect and report install status. Keep only the apps the file installs (to /Applications for DMG/LOB); if the list contains non-apps or an app that is not installed, status never reports success. The first app is the one used in reports; reorder if needed. If a package holds several apps, Intune reports success only when all are detected (DMG and LOB).
- **Ignore app version**: Yes looks only for the bundle ID (use for self-updating apps); No reinstalls when the version differs. For DMG Uninstall assignments, No requires bundle ID and version to match, Yes only the bundle ID.
- **Install as managed** (LOB): macOS 11 and later; only for a single app, no nested packages, installing to /Applications. Removing the MDM profile removes managed apps.
- **Minimum operating system**: devices below it do not install.
- **Pre-install and post-install scripts** (unmanaged PKG, agent 2309.007 or later, each under 15360 characters): a non-zero pre-install exit means the app is not installed and reports failed, retried at next check-in; post-install failures are not reported (status still success).
- Keep DMGs to one app, or apps that depend on each other; a failed independent app causes the others to reinstall.

## Get a bundle ID and version
```
defaults read /Applications/Company\ Portal.app/Contents/Info CFBundleIdentifier
defaults read /Applications/Company\ Portal.app/Contents/Info CFBundleShortVersionString
```
The same values are in the app's Contents/Info.plist (or a mounted DMG), and the Intune admin center shows bundle IDs for apps already added.

## Updating
- DMG: edit the app and upload the new DMG with the same bundle identifier (agent 2304.039 or later). Required apps update automatically; Available apps need the user to Reinstall in Company Portal.
- LOB: increment CFBundleShortVersionString of the .pkg; Required installs are retried at next check-in and, if they fail, every 24 hours.

## Troubleshooting
- Failed installs are retried at the next agent check-in up to three times while assigned.
- 0x87D30137: below minimum OS. 2016214710: pre-install script failed (may be expected while waiting on a condition). 0x87D3013E: DMG has no .app. 0x87D30139: DMG could not be mounted (mount it manually to test). 0x87D3013B / 0x87D30135: cannot write to Applications (check disk space/permissions). 0x87D30131, 0x87D30132: download failed. 0x87D3013A: disk resources exhausted; restart the Microsoft Intune Management Extension service.
- Company Portal can show Pending after a successful install (known issue); the user can use Check status in the Devices tab. Admin center reporting is not affected.
- Apps installed through the Intune agent are not removed on retire; remove them first.
- The cited pages do not document agent log paths, so verify those against Microsoft's current macOS troubleshooting guidance.

## Verify
A pilot Mac installs the app unattended, the device app status in Intune shows Installed, and the app opens without prompts (a launch warning for internet-downloaded DMG apps is a known issue).

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the three Intune Learn pages (macos-unmanaged-pkg, lob-apps-macos-dmg, lob-apps-macos), read in full. Corrected: LOB requirement is a component or multi-package .pkg signed with Developer ID Installer (not a distribution package); "no agent type uninstalls" was wrong (DMG supports Uninstall). Removed as not in the sources: mdls, pkgutil and productbuild tips, log file paths, install.log, the large-DMG timeout claim, and the auto-install trigger of the agent.
