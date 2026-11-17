---
id: computing-software.it-support-helpdesk.intune-mdm.declarative-software-update-enforcement-macos
name: declarative-software-update-enforcement-macos
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, macos-management, declarative-device-management, ddm, software-update-enforcement, macos-updates, ios-updates, update-deadline, nudge, softwareupdate]
level: practitioner
status: docs-checked
description: "Enforce macOS and iOS updates in Intune with declarative device management: latest-version and targeted-version policies, deadline behaviour, update settings, monitoring."
sources:
  - "https://learn.microsoft.com/en-us/intune/intune-service/protect/managed-software-updates-ios-macos"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# declarative-software-update-enforcement-macos

Goal: Apple devices reach the required OS version by a date, with fair
warning, and you can see who hasn't.

## Why DDM
Intune's Apple update policies use Apple's Declarative Device Management (DDM):
the device enforces the update itself, which Microsoft describes as more
reliable and autonomous than traditional MDM-based update policies, now
deprecated.

## Prerequisites
- iOS/iPadOS 17.0 or later, macOS 14.0 or later.
- Enrollment: Device Enrollment or Automated Device Enrollment.
- Older OS versions do not take these policies; update them by other means
  first.

## Two policy models
Create a settings catalog policy for iOS/iPadOS or macOS, then assign it to a
group of users or devices.

**Latest version** (category Declarative Device Management > Software Update
Enforce Latest): installs the latest eligible OS after a deferral.
- Delay in Days: days before the deadline is enforced, counted from Apple's
  release date of the update or from when the policy is configured. It sets the
  enforcement date only, not when the update is offered to users.
- Install Time: local device time, 24-hour format with a leading zero (01:00,
  02:00).

**Targeted version** (category Declarative Device Management > Software
Update): you pick the version and the moment.
- Target OS Version: for example 26.0, optionally with a supplemental
  identifier such as 26.0.1.
- Target Build Version: for example 25A354 (may carry a supplemental suffix
  like 25A354a). If it disagrees with Target OS Version, the OS version wins.
- Target Date Time: when installation is forced, in the device's local
  timezone.
- Details URL: a page of your own with organisation-specific help.

Use targeted for strict app-compatibility, phased rollouts or change
management; use latest for fast patching with low admin overhead.

## User experience at the deadline
If the user has not updated by Target Date Time, a one-minute countdown prompt
appears, then the device force-installs the update and restarts. If the device
is powered off at the deadline, it gets a one-hour grace period after powering
back on, then force-installs and restarts.

Once an enforcement is assigned, the device ignores its software update
settings, including automatic update actions. The update may install before the
deadline if the device is idle.

## Softer controls: Software Update Settings policy
A separate Software Update Settings policy controls the run-up to the
deadline. It can:
- Require that an admin or a standard user performs updates.
- Control manual interaction such as automatic download and install, and
  Rapid Security Responses behaviour.
- Hide updates from users for a period.
- Suppress update notifications up to one hour before the deadline.
- Limit users to the latest major update, the latest minor update, or both.

## Monitoring
- Policy status uses the normal device configuration reporting. Success only
  means the policy reached the device, not that the OS updated: check the OS
  version of the targeted devices.
- After a device is on a later OS than the policy specifies, the policy reports
  an error (the device reads it as a downgrade). Remove the old policy from
  such devices.
- Update status of Apple devices is in Intune's Software Update Reports for
  Apple devices.

## Stuck devices: what to check
- OS older than macOS 14 / iOS 17: not covered by these policies.
- Policy assigned but the device not yet checked in: force a sync and look at
  the policy's per-device status.
- A Software Update Settings policy that hides or limits updates can conflict
  with the target; review it.
- Space, battery and bootstrap-token requirements are Apple behaviours not
  covered by the Intune page; check Apple's deployment documentation.

## Verify
After the deadline, report on the OS version of targeted devices (not policy
success). Stragglers should have a known reason (offline, storage) and a ticket.

## Checked
2026-11-08. Confirmed against the Microsoft Learn page Configure update policies
for Apple devices (last updated 2026-02-26): DDM requirement versions,
enrollment methods, latest and targeted policy settings, deadline countdown and
grace period, Software Update Settings, monitoring. Removed as unconfirmed: Jamf
steps, notification cadence, space figure, 95 percent target, bootstrap token
advice, local softwareupdate commands, and the Apple sources (landing page and
developer page unreadable).
Method: documentation only; no commands were run.
