---
id: computing-software.it-support-helpdesk.apple-device-management.lost-mode-and-find-my
name: lost-mode-and-find-my
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, lost-mode, lost-mode-and-find-my, find-device]
level: practitioner
status: docs-checked
description: "Put a supervised iPhone or iPad in Managed Lost Mode, show a message, request its location, play a sound and release it, with the error codes."
sources:
  - "https://support.apple.com/guide/deployment/depb980a0be4/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.lostmode.enable.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.lostmode.location.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.lostmode.playsound.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.lostmode.disable.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# lost-mode-and-find-my

Goal: respond to a lost or stolen supervised iPhone or iPad.

- Managed Lost Mode locks the current user out until it is turned off. The Lock Screen shows an administrator-defined message, such as a phone number to call. It automatically enables Low Power Mode and does not need Find My turned on.
- `EnableLostMode` (iOS 9.3 and later, supervised): keys `Message`, `PhoneNumber` and `Footnote`, all optional, but a `Message` or a `PhoneNumber` must be provided. Not available on macOS, tvOS, visionOS or watchOS, forbidden with User Enrolment, allowed on the Shared iPad device channel.
- `DeviceLocation`: returns `Latitude` and `Longitude`, plus `HorizontalAccuracy`, `VerticalAccuracy`, `Altitude`, `Speed`, `Course` and an RFC 3339 `Timestamp` (iOS 10.3 and later for those). Unknown values come back negative. The device can be queried for its location even with location services off.
- `PlayLostModeSound` (iOS 10.3 and later) plays until Lost Mode is removed or the user disables the sound on the device.
- `DisableLostMode` is the only way to exit the mode. The user is then notified, through a Lock Screen message or Home Screen alert, that Lost Mode was turned off and the location was collected.
- Error codes: `12067` not in Lost Mode; `12068` location unknown (`DeviceLocation`); `12069` disabling Lost Mode failed; `12078` command invalid while in Lost Mode (an in-Lost-Mode device answers invalid commands with this).
- Erasing a device also disables Lost Mode. To restore it, the MDM server must store the Lost Mode state before the erase and re-apply it if the device enrols again.

Other ways to lock: Activation Lock (see activation-lock-management), and on a Mac a lock command with a six-digit PIN and short message; locking an Apple silicon Mac needs macOS 11.5 or later.

Gotcha: Lost Mode is supervised-only and forbidden on User Enrolment, so a BYOD enrolment has no remote Lost Mode.

Verify:
- The MDM command shows Acknowledged and the Lock Screen shows the message.
- `DeviceLocation` returns coordinates, or error `12068` if the location is not known yet.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Lock and locate Apple devices" and the apple/device-management command definitions `device.lostmode.enable.yaml`, `device.lostmode.location.yaml`, `device.lostmode.playsound.yaml` and `device.lostmode.disable.yaml` (keys, OS minimums, supervised and User Enrolment rules, error codes). Removed as unconfirmed: the Jamf Pro menu path, the privacy-approval and "user receives no prompt" claims, the police-report process advice and the unreadable developer.apple.com link. Verify steps were rewritten.
Method: documentation only; no commands were run.
