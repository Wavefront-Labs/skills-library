---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-patch-management
name: jamf-patch-management
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf, jamf-pro, jamf-patch-management, patch-software-titles, patch-policies, jamf-app-installers, installomator, third-party-patching, macos-management]
level: practitioner
status: draft
description: "Keep Mac third-party apps patched with Jamf Pro: patch software titles, patch policies with deadlines, Jamf App Installers, Installomator scripts, and patch reporting."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Patch_Management.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Jamf_App_Catalog.html"
  - "https://github.com/Installomator/Installomator"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-patch-management

Goal: Chrome, Zoom, Office and friends on every Mac are within days of the
latest version, without the help desk chasing them.

## Options (pick per app)
1. **Jamf App Installers** (Jamf App Catalog): Jamf hosts and updates the
   package; you choose deployment method, update behaviour and user
   notifications (deadline). Least effort for titles in the catalogue.
2. **Patch Management (software titles + patch policies)**: Settings →
   Computer Management → Patch Management → add title (Jamf patch source or
   external source like Title Editor). Define the **definition** (version
   list), upload packages per version, then create a **patch policy**:
   target version, distribution method (Self Service or automatic), grace
   period and user deferrals, scope.
3. **Installomator** (open-source script) in a policy: downloads the
   latest vendor build at run time — `Installomator.sh googlechromepkg
   NOTIFY=silent BLOCKING_PROCESS_ACTION=tell_user`. Low effort, but trust
   is in the script's download URL logic; pin a reviewed version.
4. Apps from the Mac App Store via VPP: auto-update from Apple when
   "Automatically Force App Updates" is set.

## Patch reports
Patch Management → title → Report: count per version, "latest version"
percentage, computers on outdated versions. Smart group criteria "Patch
Reporting: <title>" `is` `Latest Version` / `less than` drive alerts.

## User experience
- Quit-app prompts: running apps can't be replaced safely — use
  deferrals with a deadline, or the installer's "tell user to quit".
- Communicate grace periods in release notes; Self Service as the
  "update now" button.

## Gotchas
- Patch definitions only report what's installed in `/Applications` by
  bundle ID — user-installed copies in `~/Applications` are invisible.
- Apps with their own updaters (Chrome Keystone, Microsoft AutoUpdate) may
  already handle it — configure them (MAU channel via profile) instead of
  fighting them.
- Major-version upgrades (licensing changes) shouldn't ride the patch
  policy automatically.

## Verify
Patch report shows ≥ 95 % on latest within the SLA window for critical
titles; no rising Failed counts in patch policy logs.
