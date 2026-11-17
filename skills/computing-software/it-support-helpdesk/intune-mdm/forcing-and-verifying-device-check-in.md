---
id: computing-software.it-support-helpdesk.intune-mdm.forcing-and-verifying-device-check-in
name: forcing-and-verifying-device-check-in
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, device-check-in, intune-sync, last-check-in, policy-refresh, pushlaunch, company-portal, intune]
level: practitioner
status: docs-checked
description: "Force an Intune device to check in on Windows, iOS, Android and macOS, know the default refresh intervals, and prove the check-in happened from the device and the portal."
sources:
  - "https://learn.microsoft.com/en-us/intune/device-management/actions/sync"
  - "https://learn.microsoft.com/en-us/intune/device-configuration/troubleshoot-device-profiles"
  - "https://learn.microsoft.com/en-us/intune/user-help/device-actions/sync-device-windows"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forcing-and-verifying-device-check-in

## Default refresh cadence (approximate)
| Platform | After enrollment | Steady state |
|---|---|---|
| Windows | Every 3 min for 15 min, then every 15 min for 2 h | About every 8 h |
| iOS/iPadOS | Every 15 min for 1 h | About every 8 h |
| macOS | Every 3 min for 15 min, then every 15 min for 2 h | About every hour |
| Android, AOSP | Every 3 min for 15 min, then every 15 min for 2 h | About every 8 h |
Maintenance syncs: estimated about every 8 hours on all platforms, and a device is allowed
only one maintenance sync every 6.5 hours. Admin actions such as sync, remote lock or reset
passcode, and user actions in Company Portal, also trigger a check-in.

## Force it
| Where | How |
|---|---|
| Intune portal | Devices > All devices > device > **Sync** (Android, iOS/iPadOS, macOS, tvOS, visionOS, Windows; needs Help Desk Operator or similar role) |
| Windows | Settings > Accounts > Access work or school > your account > Info > **Sync**; or Company Portal > Settings > Sync; or right-click Company Portal > Sync this device |
| Any platform | Company Portal > Devices > Check Status, or Settings > Sync |

## Verify the check-in
- Portal: the device's last check-in time updates. On Windows and iOS/iPadOS, the Device
  sync status tab in the device overview tracks the Sync action (with the Preview new device
  view toggle on).
- Windows: Access work or school > Info shows the sync status.

## When sync doesn't happen
- Push blocked: devices must reach the Intune network endpoints for their platform
  (see Network endpoints for Microsoft Intune).
- Device offline: devices must be connected to the internet to receive remote commands.
- Apps failing with a nonretryable error code wait seven days before being offered again.

## Gotchas
- Sync from the portal only requests a check-in; the device must be online.
- A successful check-in doesn't mean every policy applied; check per-profile status.

## Verify
Last check-in within a few minutes of the request, and the profile or app you were
waiting for changes status (Succeeded/Installed) in the next report.

## Checked
2026-11-01. Confirmed against Intune Learn pages "Device action: sync", the device profile
troubleshooting page (refresh cycles, 8 h and 6.5 h figures) and the Windows manual sync
user-help page. Corrected the macOS cadence. Removed: PushLaunch scheduled-task commands,
Event Viewer event IDs, specific push ports and hostnames, certificate-expiry and clock
claims, throttling claim, IME service restart and the per-platform Company Portal menu
names that the pages don't state.
Method: documentation only; no commands were run.
