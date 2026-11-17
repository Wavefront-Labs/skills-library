---
id: computing-software.it-support-helpdesk.apple-device-management.activation-lock-management
name: activation-lock-management
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, lost-mode, activation-lock-management, activation-lock, bypass-code]
level: practitioner
status: docs-checked
description: "Manage Activation Lock on organisation-owned Apple devices: organisation-linked vs user-linked, bypass code retrieval within 15 days, and clearing the lock."
sources:
  - "https://support.apple.com/guide/deployment/depf4ab94ef1/web"
  - "https://support.apple.com/guide/deployment/depb980a0be4/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.activationlock.bypasscode.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/device.activationlock.clearbypasscode.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# activation-lock-management

Goal: keep organisation-owned devices recoverable while Activation Lock is on.

Two types:
- Organisation-linked: needs Apple School Manager or Apple Business. The MDM service contacts Apple servers directly to lock or unlock, using its own bypass code, with no dependency on the user or the device state. Apple says to use this method when devices are assigned to an MDM service linked to Apple School Manager or Apple Business.
- User-linked: the user turns on Find My with a personal Apple Account (not a Managed Apple Account) and can lock an organisation-linked device to it if the MDM service allows Activation Lock. Some services support both; the first successful Activation Lock event takes precedence.

User-linked steps and bypass codes:
- Activation Lock is disallowed by default on supervised devices. Before allowing it, the MDM service must fetch and store the bypass code the device creates, with the `ActivationLockBypassCode` command (response key `ActivationLockBypassCode`). It needs a supervised device (iOS 7.1, macOS 10.15, visionOS 2.0 or later), and is forbidden for User Enrolment and Shared iPad.
- The code is only available for 15 days after supervision (on iPhone and iPad, until the MDM service obtains and clears it); after 15 days without retrieval it cannot be retrieved. `ClearActivationLockBypassCode` clears it from the device.
- A device creates a new bypass code at first set-up, after an erase not restored from backup, and after an erase restored from a different device's backup.
- The MDM service needs to keep two codes: the device-generated one and the one the server creates when it initiates Activation Lock. Secure and back them up; when changing MDM service, obtain the codes or have the old service clear Activation Lock on every enrolled device.
- Devices with dual SIMs: the clear request must include both IMEI values.
- Entering a code with the device in hand: on iPhone or iPad, put the bypass code in the Apple Account password field and leave the username blank; on a Mac, choose Recovery Assistant in the menu bar, then "Activate with MDM key".
- If the MDM service cannot remove organisation-linked Activation Lock, enter the username and password of the account that created the server token linking the MDM service to Apple School Manager (Administrator, Site Manager or Device Enrolment Manager) or Apple Business (a role with permission to view, add and delete device management services).
- In Apple School Manager or Apple Business a user with Manage Device privileges can turn off both types for an owned iPhone, iPad, Mac, Apple Watch or Apple Vision Pro; the device must be in the service and not released, but need not be assigned to an MDM service.

Mac specifics: needs Apple silicon or an Apple T2 Security Chip. A Mac on Device Enrolment upgraded to macOS 10.15 or later has Activation Lock disallowed by default but you can allow it; managing it on a fresh macOS 10.15+ install needs supervision. On macOS 11 or later supervised via Device Enrolment, you cannot manage it until the Mac is enrolled in an MDM service, so Activation Lock may already be on at enrolment and the MDM service cannot turn it off.

Gotcha: a missed 15-day window means no stored bypass code; only the user's Apple Account (or the Apple School Manager / Apple Business route above) clears the lock.

Verify:
- A bypass code is stored for each device that allows user-linked Activation Lock.
- The device-generated code is re-fetched after any erase that creates a new one.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Activation Lock on Apple devices" and "Lock and locate Apple devices", plus the apple/device-management command definitions `device.activationlock.bypasscode.yaml` and `device.activationlock.clearbypasscode.yaml` (supported OS minimums, supervised and User Enrolment rules, 15-day note, bypass-code regeneration list). Removed as unconfirmed: the `allowActivationLock` restriction wording, the `IsActivationLockSupported` check, the "Jamf Pro stores the bypass code" line and the developer.apple.com EnableLostMode link (not about Activation Lock, JavaScript page). Verify steps were rewritten.
Method: documentation only; no commands were run.
