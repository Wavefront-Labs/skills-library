---
id: computing-software.systems-network-administration.patch-management.macos-software-update-management
name: macos-software-update-management
category: computing-software
field: systems-network-administration
product: patch-management
tags: [macos-updates, softwareupdate, declarative-device-management, mdm, nudge, bootstrap-token, third-party-patching]
level: practitioner
status: gated
description: "Manage macOS updates: softwareupdate CLI, MDM declarative update enforcement with deadlines, deferrals, bootstrap token and volume owner needs on Apple silicon, and user nudging."
sources:
  - https://github.com/apple/device-management
  - https://support.apple.com/guide/deployment/manage-software-updates-dep0f4f1f2d9/web
  - https://support.apple.com/guide/deployment/use-declarative-device-management-depb1bab77f8/web
  - https://ss64.com/mac/softwareupdate.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# macOS software update management

**Goal:** Macs install security updates by a deadline, without users ignoring prompts forever.

## CLI (scripts, troubleshooting)
```bash
softwareupdate --list
softwareupdate --install --all --restart       # Apple silicon: --user and --stdinpass options exist for an owner user to authorise
softwareupdate --list-full-installers
softwareupdate --fetch-full-installer --full-installer-version <version>
```

## MDM: declarative device management (macOS 14+)
Use the software update enforcement declaration (`com.apple.configuration.softwareupdate.enforcement.specific`, introduced in macOS 14.0, supervised enrolments, per Apple's device-management schema) with the required `TargetOSVersion` and `TargetLocalDateTime`. If the Mac is not running at the target time, the system enforces the update one hour after restart or when conditions such as battery level are met. If the target version does not match an available update the configuration stays active but cannot update the device.

## Deferrals
The restrictions keys `forceDelayedSoftwareUpdates` and `enforcedSoftwareUpdateDelay` (1-90 days, default 30) are marked deprecated in macOS 26 and removed in macOS 27 in Apple's schema; use the declarative `com.apple.configuration.softwareupdate.settings` configuration instead (it has Deferrals, RecommendedCadence and AutomaticActions settings).

## Apple silicon prerequisites
MDM-initiated installs on Apple silicon rely on a **bootstrap token** escrowed to the MDM so the device can authorise updates without a volume owner typing a password (gated: unconfirmed, source is paywalled or blocked). Check Apple's deployment guide on secure and bootstrap tokens.

## User experience
Tools like Nudge (open source) remind users with increasing urgency before the deadline. Communicate the deadline in plain terms.

## Third-party apps
Use your MDM's app catalogue or a patch-management product for browsers, Office and other apps.

## Verify
MDM inventory shows OS build at or above the target for the ring by the deadline; laggards are listed with last check-in.

## Checked
Date: 2026-10-27. Documentation: Apple device-management schema repository (softwareupdate.enforcement.specific: macOS 14.0, TargetOSVersion and TargetLocalDateTime required, enforcement one hour after restart; restrictions forceDelayedSoftwareUpdates and enforcedSoftwareUpdateDelay deprecated 26 and removed 27, range 1 to 90 default 30; softwareupdate.settings keys) and the ss64 softwareupdate reference (--install, --restart, --list-full-installers, --fetch-full-installer --full-installer-version, --user). The bootstrap-token requirement could not be confirmed from a readable Apple page and is gated. Removed the unconfirmed ScheduleOSUpdate deprecation, profiles command and product names.
Method: documentation only; no commands were run.
