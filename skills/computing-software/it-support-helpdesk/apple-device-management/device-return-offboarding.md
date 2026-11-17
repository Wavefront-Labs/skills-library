---
id: computing-software.it-support-helpdesk.apple-device-management.device-return-offboarding
name: device-return-offboarding
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, lifecycle, device-return-offboarding, offboarding, device-return]
level: practitioner
status: docs-checked
description: "Offboarding returned Apple devices: erase through MDM, clear Activation Lock, use Return to Service where supported, and know what survives an erase."
sources:
  - "https://support.apple.com/guide/deployment/dep0a819891e/web"
  - "https://support.apple.com/guide/deployment/dep17cb455a0/web"
  - "https://support.apple.com/guide/deployment/depf4ab94ef1/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# device-return-offboarding

Goal: a repeatable checklist for devices handed back by leavers.

- Erase through MDM with `EraseDevice`; on Macs with Apple silicon or a T2 chip on macOS 12.0.1 or later this runs Erase All Content and Settings, which erases all user data and additional volumes and, on Apple silicon, resets security settings to Full Security. If the Mac fails the preconditions it falls back to obliteration and needs a macOS reinstall (see erase-and-reenroll).
- iPhone, iPad, Apple TV and Apple Vision Pro can use Return to Service: the erase command carries Wi-Fi details and the MDM service to enrol in, and the device erases and enrols itself ready for the next user. Supervision set manually in Apple Configurator is retained.
- Activation Lock: if the leaver locked a device with a personal Apple Account, use the stored bypass code, or have a user with Manage Device privileges turn it off in Apple School Manager or Apple Business (the device must still be in the service and not released). Return to Service needs all Activation Locks off.
- Account-based wipes: Erase All Content and Settings remote wipe is not possible for User Enrolment accounts; for those, remove the work account instead (see user-enrollment-managed-boundary).
- Record serial number and condition, and update the asset register, as local process.

Gotcha: do not release a device from Apple School Manager or Apple Business unless it is leaving the organisation; a released device can no longer have Activation Lock turned off from the service.

Verify:
- The device reaches Setup Assistant or the Home Screen after erase and enrols again if it is being reused.
- Activation Lock is off before the device goes back to stock.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "Erase Apple devices", "Use Return to Service for Apple devices" and "Activation Lock on Apple devices". Removed as unconfirmed: the "release cannot be undone for 30 days" claim, VPP licence revocation steps, the group-removal step, the Jamf-specific wording, the accessories note and the developer.apple.com link (unreadable). Remaining process items (asset register, serial/condition record) are local practice, not Apple claims.
Method: documentation only; no commands were run.
