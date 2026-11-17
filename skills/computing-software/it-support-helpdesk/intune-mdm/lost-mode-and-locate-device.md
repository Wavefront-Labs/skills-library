---
id: computing-software.it-support-helpdesk.intune-mdm.lost-mode-and-locate-device
name: lost-mode-and-locate-device
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, lost-mode, locate-device, remote-lock, play-lost-mode-sound, lost-device, stolen-device, intune]
level: practitioner
status: docs-checked
description: "Handle a lost or stolen managed device: Intune remote lock, Lost mode with message, locate device, platform support, roles, location data retention, and when to escalate to wipe."
sources:
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-lost-mode"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-locate"
  - "https://learn.microsoft.com/en-us/mem/intune/remote-actions/device-remote-lock"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lost-mode-and-locate-device

## Platform support (per the three Intune action pages)
| Action | Supported platforms |
|---|---|
| Remote lock | Android Enterprise corporate-owned (dedicated, fully managed, work profile), AOSP, iOS/iPadOS, macOS, visionOS 2.0+ |
| Lost mode (message and optional phone number on the lock screen) | iOS/iPadOS in Supervised mode, ChromeOS |
| Locate device | Android Enterprise corporate-owned (dedicated, fully managed, work profile), iOS/iPadOS in Supervised mode, Windows |

Windows is not on the remote-lock or Lost mode lists. Re-check the pages before promising a capability to a user: they change.

## Roles
Run these actions with Help Desk Operator or School Administrator (remote lock also allows Endpoint Security Manager), or a custom role with the matching Remote tasks permissions (Remote lock; Enable/Disable lost mode; Locate device and Play sound to locate lost devices) plus read access to managed devices (for example Organization/Read, Managed devices/Read).

## Procedure for a reported lost device
1. Ticket: owner, device, when and where last seen, data sensitivity, police report number if stolen.
2. Protect cloud data independently of the device (sign-out of sessions, password reset) according to your identity runbook.
3. **Lost mode** (iOS/iPadOS supervised): Intune admin center > Devices > All devices > the device > Locate > Lost mode (supervised only) > Enable. Enter the lock-screen message (include specifics for returning it) and optionally a phone number, then OK. The device is locked and the user can't access it until an admin disables Lost mode. Some built-in functions such as Siri may still work unless disabled.
4. **Locate device**: select Locate device (or Locate > Locate device) on the overview pane; select the pin on the map to see the address and coordinates.
5. **Remote lock** (see platforms above): Secure > Remote lock, then set a six-digit recovery PIN. It only helps when a passcode or PIN already exists (otherwise the screen may just turn off), so enforce a passcode policy beforehand. The recovery PIN shows on the overview for up to 30 days or until another device action is sent, and can't be retrieved afterwards, so record it. Do not resend remote lock to the same macOS device until that PIN has been used; extra attempts show Failed.
6. Windows: use Locate device if location is enabled, and decide on wipe per your policy.
7. Decide a review time for escalating to **Wipe** and record the decision in the ticket and asset system.

## Locate prerequisites
- Location services on and the Intune app installed.
- Android fully managed and corporate-owned work profile: the Locate Device feature must be explicitly enabled with a device restrictions profile; work profile users must also grant the Intune app location permission (Allow all the time). Dedicated devices have it enabled by default unless blocked by a restrictions profile.
- Windows: a Settings catalog policy with Privacy > Let Apps Access Location = Force allow, assigned to the devices.
- For Android the admin also needs Device configuration/Read and scope tag visibility of the policy that enables location.
- Dedicated Android devices that are offline can show a last known location: collected every eight hours or at check-in, kept up to seven days.

## Privacy gotchas
- Location data is collected only when the action is triggered; it is encrypted in transit and at rest, stored for 24 hours, then deleted automatically (manual deletion is not supported). Last known location can be kept up to seven days.
- On Android fully managed and work profile devices, users get a notification when Locate is used if notifications are enabled.
- Use Locate only for reported loss, not for tracking staff on a manager's request.

## Recovered
Select Lost mode > Disable on the device, check for tampering, sync, confirm compliance, return to the user.

## Verify
Device action status shows Complete, the lock screen shows your message (test on a spare device first), and the ticket records each action and the wipe decision.

## Checked
Method: documentation only; no commands were run. Checked 2026-11-08 against the Intune Learn pages device-lost-mode, device-locate and device-remote-lock (read in full). Confirmed: platform lists, roles, menu paths, six-digit recovery PIN and 30-day display, macOS resend warning, Windows Force allow setting, eight-hour and seven-day last known location, 24-hour retention. Removed because the pages do not state them: the play-sound platform row, Activation Lock/bypass code advice, BitLocker rotation, Entra revoke-sessions step as a specific action, and the 24-72 h review window.
