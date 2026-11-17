---
id: computing-software.it-support-helpdesk.apple-device-management.ddm-software-update-enforcement
name: ddm-software-update-enforcement
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, ddm, ddm-software-update-enforcement, ddm-updates, enforcement]
level: practitioner
status: docs-checked
description: "Enforce an OS version by a date with the DDM softwareupdate.enforcement.specific configuration and read its status, instead of the removed ScheduleOSUpdate command."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/configurations/softwareupdate.enforcement.specific.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/configurations/softwareupdate.settings.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/system.update.schedule.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/status/softwareupdate.install-state.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ddm-software-update-enforcement

Goal: enforce a specific OS version by a date.
- Declaration type `com.apple.configuration.softwareupdate.enforcement.specific`. Keys: `TargetOSVersion` (required, for example `16.1`), `TargetLocalDateTime` (required, format `yyyy-mm-ddThh:mm:ss`, no time zone offset or fractional seconds), optional `TargetBuildVersion` (for example `20A242`, may carry a supplemental suffix such as `20A242a`) and optional `DetailsURL`.
- If the user has not triggered the update before the target time, the device force installs it. If the device is not running at that time, enforcement happens 1 hour after restart or when all required conditions (such as minimum battery level) are met.
- Availability: iOS 17, macOS 14, tvOS 18.4, visionOS 26 and later. macOS needs a supervised device; iOS also accepts a device enrolment. Multiple configurations may apply (`apply: multiple`).
- The system installs exactly the version in `TargetOSVersion`; it will not install a patch version if only a minor version is set. A supplemental update (for example `16.1(a)`) installs only on a device already on the base version, so use two configurations to go from an older base.
- If no available update matches the target, the configuration stays active and the device cannot update until one appears. Servers learn available versions from Apple's GDMF service (`https://gdmf.apple.com/v2/pmv`) and should check it no more than once a day.
- `com.apple.configuration.softwareupdate.settings` (iOS 18, macOS 15 and later) sets `Notifications`, `Deferrals`, `AutomaticActions`, `RapidSecurityResponse` and `Beta`.
- The old `ScheduleOSUpdate` MDM command is deprecated in iOS/macOS/tvOS 26 and removed in 27. The device ignores it and returns an informational error when a `SoftwareUpdateEnforcementSpecific` configuration manages the update.
Practice: pair the declaration with user communication and set the target date after your pilot has validated the version.
Verify: status items `softwareupdate.install-state` (`none`, `downloading`, `prepared`, `installing`, `failed`), `softwareupdate.pending-version`, `softwareupdate.failure-reason` and `softwareupdate.install-reason` are the related items the configuration may affect.

## Checked

Date: 2026-11-07. Read in full from apple/device-management raw YAML: `softwareupdate.enforcement.specific` (keys, notes on GDMF, supplemental versions, restart rule, OS minimums and enrolments), `softwareupdate.settings` (top-level keys), `system.update.schedule` (deprecated 26.0, removed 27.0, precedence note) and the `softwareupdate.install-state` status item. Removed: bootstrap-token gotcha for Apple silicon, the "increasing notifications" sequence, Jamf Pro product claims and the invented Verify steps. Replaced unreadable developer.apple.com and guessed Apple guide sources.
Method: documentation only; no commands were run.
