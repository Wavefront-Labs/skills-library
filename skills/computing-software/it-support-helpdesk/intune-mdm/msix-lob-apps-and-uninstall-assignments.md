---
id: computing-software.it-support-helpdesk.intune-mdm.msix-lob-apps-and-uninstall-assignments
name: msix-lob-apps-and-uninstall-assignments
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, msix, app-uninstall-assignment, lob-apps, msi-lob, intune-apps, app-removal]
level: practitioner
status: docs-checked
description: "Deploy Windows LOB MSI and MSIX/APPX apps with Intune, update them, and remove apps with Uninstall assignments and resolve conflicting intents."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/apps/lob-apps-windows
  - https://learn.microsoft.com/en-us/windows/msix/overview
  - https://learn.microsoft.com/en-us/mem/intune/apps/apps-deploy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# msix-lob-apps-and-uninstall-assignments

## Add a Windows LOB app
Apps > All Apps > Create > Windows platform > Line-of-business app. Select a package file with extension `.msi`, `.appx` or `.appxbundle` (the .msix and .msixbundle extensions are listed as Windows app file extensions on the same page).
- **App Install Context**: choose for dual mode apps; otherwise preselected from the package.
- **Ignore app version**: Yes for self-updating apps (for example Chrome MSI) to avoid a race between the developer's updater and Intune.
- **Command-line arguments** (MSI): only one argument, without `msiexec`, `/i` or `/x`. For more than one, use Win32 app management.
- Mixing Win32 and LOB apps during Windows Autopilot enrollment can fail because both use the Trusted Installer service; Autopilot device preparation supports mixing. For `.msi` files wrapped as `.intunewin`, Microsoft suggests the Intune Management Extension.
- To update an APPX, upload the new file under the app's Properties > App information, and increment the Version in `AppxManifest.xml` or deployment fails.
- Store-signed LOB apps (.appx, .msix, .appxbundle, .msixbundle) can be deployed to Surface Hub.
- MSIX is Microsoft's packaging format; all MSIX packages must be signed before installation, and the package supports clean uninstall.

## Assignment intents
- **Available for enrolled devices**: users install from the Company Portal; for most types only valid for user groups (Win32 may use device groups).
- **Required**: installed on the devices in the group.
- **Uninstall**: removes the app only if Intune previously installed it via Available or Required using the same deployment. Uninstall and Required assignments are not supported for non-enrolled devices.
- One group cannot be targeted with multiple intents; conflicts arise when a user or device sits in groups with different intents. Microsoft says not to create them, and an assignment filter may not work as expected because intent is evaluated before the filter.

| Group 1 | Group 2 | Result |
|---|---|---|
| User Required | User Uninstall | Required |
| User Available | User Uninstall | Uninstall |
| User Required | Device Uninstall | Required |
| User Available | Device Uninstall | Available; if already installed as Required, it is uninstalled; if the user installs it from the Company Portal the uninstall is not honored |
| Device Required | Device Uninstall | Required |
| Device Available | Device Uninstall | Uninstall |

## Removing an app
Add an Uninstall assignment to the same group that held the install (the intent is honored only for apps Intune installed). Check the intent table for users in several groups, and use Exclude Groups in assignments to avoid overlaps. Soft-deleted Entra groups show as Soft-Deleted and their assignments do not apply.

## Checked
Date: 2026-11-08. Read in full: "Add a Windows Line-of-Business App to Microsoft Intune" (updated 2026-04-14), "Assign Apps to Groups With Microsoft Intune" (updated 2026-08-06) and "What is MSIX?" (updated 2026-10-12). Corrections: Uninstall only works for apps Intune installed; the conflict outcomes are taken from the page's table, replacing "unpredictable". Removed as unconfirmed: trusted certificate store placement for signing, uploading framework dependencies such as VCLibs, MSI LOB being installed by the MDM stack rather than IME, MSIX app attach, the PsExec test, MSI product-code detection behaviour, and the Verify section.
Method: documentation only; no commands were run.
