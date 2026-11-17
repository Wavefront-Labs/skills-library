---
id: computing-software.it-support-helpdesk.intune-mdm.device-enrollment-managers-and-corporate-identifiers
name: device-enrollment-managers-and-corporate-identifiers
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, device-enrollment-manager, corporate-identifiers, enrollment-restrictions, intune-enrollment, ownership]
level: practitioner
status: docs-checked
description: "Intune device enrollment manager accounts (1,000-device limit, restrictions) and corporate identifiers (CSV formats, platform support, Windows enrollment-time ownership)."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/device-enrollment-manager-enroll"
  - "https://learn.microsoft.com/en-us/mem/intune/enrollment/corporate-identifiers-add"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# device-enrollment-managers-and-corporate-identifiers

## Device enrollment manager (DEM)
- A DEM is a nonadministrator user who can enroll and manage up to **1,000** devices; a
  standard nonadmin account can enroll 15. Needs an Intune user or device licence and an
  associated Entra user. Limit of 150 DEM accounts.
- Not needed with co-management, automatic enrollment + group policy, or Windows Autopilot,
  which let standard accounts enroll more than 15.
- Enrollment methods: bulk provisioning package, DEM-initiated Company Portal enrollment,
  DEM-initiated Entra join.
- Manage: Intune Administrator role (Update creates/deletes DEMs; Read lists them). Devices >
  Enrollment > **Device enrollment managers** tab > Add > enter UPN > Add. Remove with Delete,
  but do not delete a DEM account that enrolled devices, because those devices then have issues.
  Use dedicated accounts not assigned to an individual.
- Limitations: no users on DEM-enrolled devices so apps cannot be deployed as Available;
  Android Enterprise allows up to 10 personally owned work-profile devices, not corporate
  work-profile or fully managed; AOSP and Apple ADE are unsupported; Apple VPP apps need
  device licences, not user licences; use device-level certificates for Wi-Fi and email;
  Conditional Access only on Windows 10 1803+ and Windows 11; Windows devices enroll in
  shared device mode so device limit restrictions do not work (set a hard limit in Entra
  instead), and an Entra max device limit under 1,000 caps the DEM; Company Portal shows only
  the local device and cannot wipe it (wipe from the admin center); user-based VPN profiles
  do not work.

## Corporate identifiers
Intune marks devices that register with Entra as personal. These already enroll as
corporate with no identifiers: DEM accounts, Apple enrollment programs (iOS/iPadOS),
Windows Autopilot, co-management/GPO, Azure Virtual Desktop, provisioning packages, Knox
Mobile Enrollment, Android Enterprise corporate-owned/fully managed/dedicated, AOSP
corporate-owned, Google Zero Touch.

- Roles: Policy and Profile Manager (Intune role) or Intune Administrator (Entra role).
- Types (one per CSV): IMEI, serial number, or serial + manufacturer + model (Windows only).
  Windows needs the manufacturer/model/serial form (Windows 11 22H2+ with KB5035942;
  Windows 10 22H2 with KB5039299). macOS: serial. iOS/iPadOS: serial recommended.
  Android device admin: IMEI/serial on Android 9 and earlier; Android Enterprise
  personally owned work profile: Android 11 and earlier.
- CSV: no headers, up to 5,000 rows or 5 MB, remove periods from serials. Android/iOS lines
  are `IMEI-or-serial,details` (details up to 128 chars). Windows lines are
  `manufacturer,model,serial` and take no details. Up to 10 Windows CSVs in the admin
  center; use PowerShell or Graph for more.
- Upload: Devices > Enrollment > **Corporate device identifiers** tab > Add > Upload CSV
  file (or Enter manually, Android and iOS/iPadOS only). Duplicates with different details
  prompt for overwrite. Statuses: Enrolled, Not contacted, Not applicable, Failed.
- Windows identifiers apply only **at enrollment time**; a matching device is corporate for
  enrollment restriction evaluation, then Intune's normal logic decides the stored
  ownership (for example, Add Work Account or Company Portal enrollment ends up Personal).
  Once any Windows identifiers exist, enrolling devices not matching them are personal.
- Get Windows values:
  ```powershell
  Get-CimInstance -ClassName Win32_ComputerSystem | ForEach-Object {$_.Manufacturer, $_.Model, (Get-CimInstance -ClassName Win32_BIOS).SerialNumber -join ','}
  ```
- Android and iOS: an IMEI differing from the one Intune recorded marks the device personal.
  Android serial numbers are not guaranteed unique or present.
- Apple user enrollment with Company Portal and account-driven user enrollment cannot use
  corporate identifiers.
- Deleting an identifier does not change an enrolled device's ownership. Change it at
  Devices > All devices > device > Properties > Device ownership. Corporate to personal
  deletes collected app information within seven days and the phone number.
- Block personal devices with an enrollment platform restriction; a blocked device shows
  failure reason "Enrollment restriction not met" under Devices > Enrollment failures.

## Checked
Date: 2026-11-07. Read in full: "Add device enrollment managers" and "Identify devices as corporate-owned" (both updated
2026-04-09). The enrollment-restrictions-set source was not read and was dropped. Corrections: the DEM limit is 1,000 versus 15 for
a standard account (not a vague "per-user limit"); DEM does not apply to Autopilot/ADE as a substitute. Removed as unconfirmed:
kiosk/shared-device guidance, "odd" Conditional Access compliance, MFA/vault advice, the Get-CimInstance Win32 two-command
instruction (replaced with the page script), "Android serial for Android 10+" claim, troubleshooting CSV-header and
stale-device-delete advice, and the Verify step.
Method: documentation only; no commands were run.
