---
id: computing-software.digital-privacy-hygiene.device-hardening.windows-update-settings
name: windows-update-settings
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, windows-update, automatic-updates, end-of-support]
level: practitioner
status: docs-checked
description: "Install Windows updates, set active hours to avoid disruptive restarts, and note that Windows 10 support ended on 14 October 2025."
sources:
  - "https://support.microsoft.com/windows/update-windows-3c5ae7fc-9fb6-9af1-1984-b5e0412c556a"
  - "https://learn.microsoft.com/windows/deployment/update/waas-delivery-optimization"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows Update settings

**Goal:** security fixes install promptly, restarts don't ambush you, and the PC is on a supported Windows version.

## Check and install
Settings > Windows Update > select **Download & install** if updates are available, and restart when prompted. Use active
hours to prevent inconvenient installs and restarts while you are using the device (Microsoft Support: "Keep your device up
to date with active hours").

## Supported version
Support for Windows 10 ended on 14 October 2025: after that date Microsoft no longer provides free software updates from
Windows Update, technical assistance or security fixes for Windows 10. The PC keeps working, but Microsoft recommends
moving to Windows 11. Unsupported means no security fixes.

## Delivery Optimization
In Windows client Enterprise, Professional and Education editions, Delivery Optimization is on by default for peer-to-peer
sharing on the local network (devices behind the same NAT). Administrators can change this by Group Policy or MDM.

## Gotchas
- BitLocker-protected machines may ask for the recovery key after firmware updates; have it ready (see
  `computing-software.digital-privacy-hygiene.device-hardening.suspending-bitlocker-for-firmware-updates`).

## Checked
2026-10-28. Confirmed on Microsoft Support (Update Windows) and Microsoft Learn (Delivery Optimization): Download &
install, active hours reference, Windows 10 end of support date and consequences, Delivery Optimization default.
Removed (not on the fetched pages): the 5-week pause limit, Advanced options table and wording, the Windows 10 consumer
ESU claim, the troubleshooting commands (sfc, DISM, winver), the metered connection setting.
Method: documentation only; no commands were run.
