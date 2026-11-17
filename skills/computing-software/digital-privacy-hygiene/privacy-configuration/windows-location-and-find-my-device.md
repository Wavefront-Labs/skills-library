---
id: computing-software.digital-privacy-hygiene.privacy-configuration.windows-location-and-find-my-device
name: windows-location-and-find-my-device
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, windows-location, find-my-device, windows-privacy, location-history]
level: practitioner
status: docs-checked
description: "Turn off or restrict Windows location, per-app access and location history, and Find My Device, with the Microsoft-documented Group Policy and registry equivalents."
sources:
  - "https://learn.microsoft.com/en-us/windows/privacy/manage-connections-from-windows-operating-system-components-to-microsoft-services"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Windows location and Find my device

**Goal:** Windows and apps get your location only when it is worth it. Source: Microsoft's "Manage connections from
Windows operating system components to Microsoft services" (sections 5 and 18.2). Its UI paths are written for older
Windows 10 builds, so on Windows 11 look for the same labels under Settings > Privacy & security > Location.

## Location (section 18.2)
| Goal | UI | Group Policy | Registry (REG_DWORD) |
|---|---|---|---|
| Location off for the device | Click **Change** on the Location page | Computer Configuration > Administrative Templates > Windows Components > Location and Sensors > Turn off location | `DisableLocation` = 1 under HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\LocationAndSensors |
| Apps cannot access location | Turn off **Allow apps to access your location** | Windows Components > App Privacy > Let Windows apps access location, Select a setting box = Force Deny | `LetAppsAccessLocation` = 2 under HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\AppPrivacy |
| Choose apps that can use location | Turn each app off in the UI | n/a | n/a |
| Location history | Erase it with the **Clear** button | n/a | n/a |

Microsoft states location history is erased with the Clear button; it does not describe a separate switch.

## Find My Device (section 5)
Documented way to turn it off: Settings > Update & Security > Find My Device > **Change** > Off (older Windows 10 path).
Managed devices: disable Group Policy Computer Configuration > Administrative Template > Windows Components > Find My
Device > Turn On/Off Find My Device, or set `AllowFindMyDevice` = 0 under
HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\FindMyDevice.

Decision: leave it on for a laptop you travel with if you want to be able to locate it; turn it off if you do not want
the device locatable. The page does not describe what Find My Device sends, so check Microsoft's current
documentation before relying on any claim about its data.

## Verify
- [ ] The Location page shows the master switch and per-app list as you set them.
- [ ] After Clear, location history is empty.

## Checked
Checked 2026-11-08 against the full text of the Microsoft Learn connections page (Find My Device and Location
sections). Removed what it does not state: Wi-Fi positioning data being sent, Find My Device needing a Microsoft
account and admin rights, the account.microsoft.com/devices portal, the default location, desktop-app toggle,
location notification, Weather and Maps advice, and the taskbar icon check. The support.microsoft.com/windows landing
page has no specifics and was dropped.
Method: documentation only; no commands were run.
