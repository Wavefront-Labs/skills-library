---
id: computing-software.it-support-helpdesk.intune-mdm.autopilot-reset-and-fresh-start
name: autopilot-reset-and-fresh-start
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, autopilot-reset, fresh-start, winre, device-actions, windows, intune]
level: practitioner
status: docs-checked
description: "Use Intune Autopilot Reset and Fresh Start: what each keeps and removes, prerequisites (WinRE, Entra join), the local Ctrl+Win+R reset and enabling policy, and the WinRE failure."
sources:
  - "https://learn.microsoft.com/en-us/autopilot/windows-autopilot-reset"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-fresh-start"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-management"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autopilot-reset-and-fresh-start

| | Autopilot Reset | Fresh Start |
|---|---|---|
| Does | Removes personal files, apps and settings; reapplies original settings; resets region, language and keyboard to original values | Removes apps, especially preinstalled OEM apps (device-actions list: reinstalls the latest Windows and removes manufacturer apps) |
| Keeps | Entra ID identity connection, Intune management connection, Wi-Fi details, applied provisioning packages (and one on USB at start), SCEP certificates | With **Retain user data**: Entra join, MDM re-enrollment when an Entra user signs in, the user's Home folder contents |
| Platform | Windows 11 and Windows 10; not Entra hybrid joined or Surface Hub | Windows |

## Autopilot Reset
- **Remote**: device must be MDM managed and Entra joined; Intune needs the Intune
  Service Administrator role. Intune admin center > Devices > All devices > select
  devices > More > **Autopilot Reset**. The user is blocked from the desktop until
  settings are restored and an MDM sync completes. Afterwards the primary user and Entra
  device owner are removed and the next user to sign in becomes both; shared devices stay shared.
- **Local**: at the lock screen press **CTRL + WIN + R** and sign in with an account that
  has local admin credentials. Local reset is disabled by default; enable the
  `CredentialProviders/DisableAutomaticReDeploymentCredentials` policy: in Intune, a
  Windows 10 and later Device restrictions profile > General > **Autopilot Reset =
  Allow**; with Windows Configuration Designer, set it to 0 in a provisioning package.
  A local reset does not update the primary user or Entra device owner; do that manually.
- Hybrid joined (and Surface Hub) devices need a full wipe; a hybrid device may take up
  to 24 hours to be ready to deploy again unless you re-register it.

## Fresh Start
Intune admin center > Devices > All devices > a device > Remove data > **Fresh Start**,
with **Retain user data on this device** ticked or not. If not retained, the device
returns to the OOBE-completed state keeping the built-in administrator account, and BYOD
devices are removed from Entra ID and MDM. Roles: Help Desk Operator, School
Administrator, Endpoint Security Manager, or a custom role with Remote tasks/Clean PC.
It uses the CleanPC CSP and the Graph `cleanWindowsDevice` action.

## Prerequisites and failures
- **WinRE must be configured and enabled.** Autopilot Reset checks first; if not, it
  fails immediately with an error such as `ERROR_NOT_SUPPORTED (0x80070032)` in the logs.
  Fix: run `reagentc.exe /enable`. If it still fails or WinRE cannot be enabled, contact
  Microsoft Support.
- Intune limits daily Wipe, Retire and Delete actions per tenant; Wipe, Retire and Delete
  override other pending actions on a device (device actions article).

## Checked
Date: 2026-11-07. Read in full: the Windows Autopilot Reset article, the Fresh Start
device action article. Searched (not read end to end) the device actions overview for
Autopilot reset, Fresh Start and wipe rows.
Corrections: the skill said to remove the previous user as primary user before a reset
and that "ESP doesn't rerun" (neither on the pages; the remote reset itself clears the
primary user); "Windows 10 1709+ Pro/Ent/Edu" and "1703+" version claims removed; Fresh
Start does not necessarily keep Entra join (only when Retain user data is selected).
Removed unconfirmed: `reagentc /info`, `manage-bde -status`, Panther/Logs\Reset log
paths and event log name, BitLocker comments, "reinstalls Win32 apps", the
"when not to use" malware advice and the org-branding Verify step.
Method: documentation only; no commands were run.
