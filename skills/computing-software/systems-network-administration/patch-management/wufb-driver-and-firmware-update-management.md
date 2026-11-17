---
id: computing-software.systems-network-administration.patch-management.wufb-driver-and-firmware-update-management
name: wufb-driver-and-firmware-update-management
category: computing-software
field: systems-network-administration
product: patch-management
tags: [wufb-driver-management, driver-updates, firmware-updates, intune, windows-patch-tooling, patch-management]
level: practitioner
status: docs-checked
description: "Control Windows driver and firmware updates with Intune driver update policies (WUfB deployment service): manual vs automatic approval, deferrals, exclusions and reporting."
sources:
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-driver-updates-overview
  - https://learn.microsoft.com/en-us/mem/intune/protect/windows-driver-updates-policy
  - https://learn.microsoft.com/en-us/windows/deployment/update/deployment-service-drivers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Driver and firmware update management (WUfB)

Windows Update offers OEM drivers and firmware. Unmanaged, they arrive unpredictably; blocked entirely, devices miss security firmware.

## Intune driver update policies
Devices > Windows updates > Driver updates > Create profile:
- **Manual approval**: Intune lists the driver updates available for the group's devices; you approve each one and can set a date on which it becomes available.
- **Automatic approval**: recommended drivers auto-approved after a deferral (0 to 30 days, counted from the day the driver is added to the policy); you can pause individual updates.
- Assign to groups aligned with update rings (pilot first).

Prerequisite: make sure no Windows update ring or settings catalog policy blocks driver installation; review the Windows drivers setting in your update rings before using driver policies.

## Excluding drivers entirely
- Block drivers in the Windows update ring (the Windows drivers setting); driver update policies then have no effect.
- Deliver drivers and firmware with the OEM's tools or packages instead.

## Firmware via OEM tools (common pattern)
- Use each OEM's documented command-line tool for BIOS and firmware updates, and follow its documentation for BitLocker handling and restart options.

## Gotchas
- Driver policies show only drivers Windows Update has for the hardware; OEM-only drivers stay outside.
- Driver update policies do not enforce OEM Computer Hardware ID (CHID) targeting, so devices can receive newer recommended drivers instead of CHID-targeted ones.

## Verify
Driver update report shows approved drivers installed per ring; BIOS version inventory converges on the approved version per model.

## Checked
Date: 2026-10-27. Documentation checked: Microsoft Learn Intune "Windows driver updates overview" and "Create and manage Windows driver update policies" (Devices > Windows updates > Driver updates; automatic or manual approval; "Make updates available after (days)" supports 0 to 30 days from the day the update is added to the policy; approve or pause; review update ring settings that block drivers; no CHID enforcement) and the Windows Autopatch driver controls page. Removed the OEM command lines, the group policy name and the unconfirmed BitLocker and graphics-driver statements.

Method: documentation only; no commands were run.
