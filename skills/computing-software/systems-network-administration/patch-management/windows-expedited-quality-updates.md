---
id: computing-software.systems-network-administration.patch-management.windows-expedited-quality-updates
name: windows-expedited-quality-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [expedited-updates, windows-autopatch, intune, quality-update, windows-patch-tooling, patch-management]
level: practitioner
status: docs-checked
description: "Push a Windows security update fast with Intune expedited quality update policies or Autopatch: prerequisites, deadlines, reboot behaviour and reporting."
sources:
  - https://learn.microsoft.com/en-us/intune/device-updates/windows/configure-expedite-policy
  - https://learn.microsoft.com/en-us/intune/device-updates/windows/manage-quality-updates
  - https://learn.microsoft.com/en-us/windows/deployment/windows-autopatch/manage/windows-autopatch-windows-quality-update-overview
  - https://learn.microsoft.com/en-us/windows/deployment/update/wufb-reports-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expedited quality updates (Intune / Autopatch)

Expediting overrides ring deferrals and deadlines to install a specific security update level as fast as possible, for emergencies (zero-days, out-of-band fixes).

## Prerequisites
- Windows Pro, Pro Education, Enterprise or Education (Enterprise LTSC is not supported; use update rings). Devices managed by Intune, Entra joined or Entra hybrid joined, telemetry at Required or higher, and the Microsoft Account Sign-In Assistant service (wlidsvc) running.
- Licensing: Microsoft Intune Plan 1 and a Windows licence that includes the Autopatch entitlement.
- **Microsoft Update Health Tools** are required for Windows versions earlier than 24H2 (install via KB4023057); on Windows 11 24H2 and later do not install them (a device that has them should have them removed).
- Policy settings that interfere (intranet update service location, Configure Automatic Updates, feature-update deferral and Disable Dual Scan) should be Not configured; Enable pre-release builds should be Not configured.

## Create the policy
Intune admin center > Devices > Windows Updates > Quality updates > Create > Expedite policy:
- Select the quality update to expedite (one update per policy, identified by release date; updates with B in the name are the second-Tuesday releases).
- Set the number of days before a required restart is enforced.
- Assign to groups (pilot first if time allows, but expediting is for speed).

Windows Autopatch quality update policies also support expedite; see the Autopatch quality updates page.

## Behaviour
- Devices that already have the selected update or a newer applicable one do not receive it; Windows Update may install a newer update than the one selected.
- Install begins after the device's next update scan; restart is enforced after the configured deadline, with notifications.
- The policy can be deleted once all targets report compliant.

## Reporting
Intune provides summary and device reports for each expedite policy (devices installing, completed or in error). Windows Update for Business reports give fleet-wide state.

## Gotchas
- Only supported Windows security updates can be expedited; the dropdown lists only eligible updates.
- Offline devices expedite when they come online; track the long tail.
- Group-policy settings such as an intranet update service location or Disable Dual Scan can block expedite; restore them to Not configured.

## Verify
Report shows your target percentage installed within your agreed window; device OS build (`(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').UBR`) at or above the expedited build.

## Checked
Date: 2026-10-27. Documentation: Microsoft Learn "Expedite policies for Windows quality updates", "Manage Windows quality updates" (prerequisites: editions, LTSC unsupported, Intune Plan 1 plus Autopatch entitlement, telemetry Required, wlidsvc) and Windows Autopatch quality update overview. Corrected the Update Health Tools requirement (only before Windows 11 24H2) and licensing; removed the unconfirmed registry key, setting names and report path.
Method: documentation only; no commands were run.
