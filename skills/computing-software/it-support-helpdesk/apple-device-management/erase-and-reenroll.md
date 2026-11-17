---
id: computing-software.it-support-helpdesk.apple-device-management.erase-and-reenroll
name: erase-and-reenroll
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, lifecycle, erase-and-reenroll, erase-device, reenrol]
level: practitioner
status: docs-checked
description: "Erase an Apple device with the EraseDevice command, handle Mac obliteration fallback and use Return to Service to re-enrol iPhone and iPad automatically."
sources:
  - "https://support.apple.com/guide/deployment/dep0a819891e/web"
  - "https://support.apple.com/guide/deployment/dep17cb455a0/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.erase.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# erase-and-reenroll

Goal: reset devices cleanly and bring them back under management.

EraseDevice command
- Needs the Device Erase right (`AllowDeviceErase`). Available from iOS 4.0, macOS 10.7, tvOS 10.2, visionOS 1.1 and watchOS 10.0. Forbidden with User Enrolment. It erases immediately, even a locked device, without warning the user, and the device does not retry if the first attempt fails.
- Optional keys: `PreserveDataPlan` (iOS 11.0, keeps the eSIM data plan), `DisallowProximitySetup` (iOS 11.3), `PIN` (macOS 10.8 and later, the six-character Find My PIN) and `ObliterationBehavior` (macOS 12.0 and later).
- Remote wipe can also be started from iCloud or Exchange ActiveSync; with ActiveSync the device checks in with Exchange first. Erase All Content and Settings remote wipe is not possible for User Enrolment accounts, or for Exchange ActiveSync accounts on supervised devices.

Mac erase
- macOS 12.0.1 or later with Apple silicon or the Apple T2 Security Chip: `EraseDevice` runs Erase All Content and Settings (Apple menu > System Settings > General > Transfer or Reset on macOS 13 or later). Requirements: Apple silicon needs a bootstrap token from the MDM service; both chips need to start from the first partition, have a signed system volume and not have been started from an external volume; T2 Macs also need Full Security and no EFI firmware password (remove it with `SetFirmwarePassword` first).
- If a requirement is not met the Mac falls back to obliteration and macOS must be reinstalled. `ObliterationBehavior` values: `Default`, `DoNotObliterate`, `ObliterateWithWarning`, `Always` (`Always` skips Erase All Content and Settings). An EACSPreflight check can report Success, Not supported or Unknown failure beforehand.
- Danger: a Mac enrolling with FileVault on that does not support Erase All Content and Settings can be erased this way and needs a full reinstall.

Re-enrolment with Return to Service (iPhone, iPad, Apple TV, Apple Vision Pro)
- Send `EraseDevice` with a `ReturnToService` dictionary (iOS 17.0, tvOS 18.0, visionOS 26.0). `Enabled` true makes the device re-enrol itself; the user needs to deactivate all Activation Locks first.
- `WiFiProfileData` is required when the device has no Ethernet or cellular connection. `MDMProfileData` is required for unsupervised devices and for supervised devices not enrolled with Automated Device Enrollment; for ADE devices it is only needed if the cloud configuration has `configuration-web-url`.
- If the device is in Apple School Manager or Apple Business you can omit the MDM service configuration and the device looks for an enrolment profile at activation. The language and region and any Apple Configurator supervision are kept.
- With app preservation (iOS 26, iPadOS 26, visionOS 26 or later) managed apps stay and the device uses a bootstrap token (the `BootstrapToken` key); the MDM service sends `DeviceConfigured` to release the Setup Assistant pane. Software and app updates are disabled until the next reset.

Gotcha: Clear Activation Lock before reuse; Return to Service does not work correctly while it is on.

Verify:
- The erase command status is Acknowledged (a Mac that falls back to obliteration returns Error or Acknowledged according to `ObliterationBehavior`).
- The device reaches Setup Assistant or, with Return to Service, the Home Screen and enrols again.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Erase Apple devices" and "Use Return to Service for Apple devices", and the apple/device-management `device.erase.yaml` (key list, OS minimums, ObliterationBehavior values, ReturnToService sub-keys). Removed as unconfirmed: the Jamf Pro wipe menu path, the "6-digit PIN for Mac" wording (the definition says six-character Find My PIN, optional), "back up first", the Apple silicon "network to activate" note and the stale-record advice. Verify steps rewritten.
Method: documentation only; no commands were run.
