---
id: computing-software.it-support-helpdesk.apple-device-management.managed-software-updates
name: managed-software-updates
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, sw-updates, managed-software-updates, software-updates, managed-updates]
level: practitioner
status: docs-checked
description: "Control macOS and iOS update timing: the legacy ScheduleOSUpdate command and delay restrictions, their replacement by DDM, and the device power and network preconditions."
sources:
  - "https://support.apple.com/guide/deployment/manage-software-updates-depc4c80847a/web"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/commands/system.update.schedule.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.applicationaccess.yaml"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# managed-software-updates

Goal: control update timing safely, using the current mechanism where the OS supports it.
- Current: the DDM `com.apple.configuration.softwareupdate.enforcement.specific` configuration (see ddm-software-update-enforcement) and `com.apple.configuration.softwareupdate.settings`.
- Legacy MDM command `ScheduleOSUpdate` (deprecated in 26.0, removed in 27.0 on iOS, macOS and tvOS; supervised devices only; not allowed with User Enrolment). `InstallAction` values: `Default`, `DownloadOnly`, `InstallASAP`, `NotifyOnly`, `InstallLater`, `InstallForceRestart` (the last warns it may cause data loss). `NotifyOnly`, `InstallLater` exist on macOS only; `MaxUserDeferrals` works only with `InstallLater` on minor macOS updates.
- On iOS and tvOS, download and install are two steps: send `ScheduleOSUpdate` with `Default` to download, then again with `Default` to install.
- Legacy delay restrictions (`com.apple.applicationaccess`, deprecated 26.0, removed 27.0): `forceDelayedSoftwareUpdates` (boolean, default false; user sees updates only after the delay) and `enforcedSoftwareUpdateDelay` (days, 1 to 90, default 30). On iOS these need a supervised device; none work with User Enrolment.
- Preconditions Apple lists: minimum battery for a user-initiated update is 20% on iPhone, iPad and Apple silicon Macs and 50% on Intel Macs; for an automatic update it is 30% on iPhone and iPad and 50% on Macs, and the device must be on power to download and prepare it. The device needs enough free space.
- Networks: Apple services fail any connection that uses HTTPS interception (SSL inspection), so exclude the update hosts from it. Content Caching on a Mac with macOS 10.13 or later can cache update downloads, but devices still contact Apple servers to complete the update.
Practice: publish an update calendar, run a pilot group before everyone else, and check power, disk space and network before blaming MDM.
Verify: the status items `softwareupdate.install-state` and `softwareupdate.pending-version` (DDM) or the `UpdateResults` `Status` values in the command response (`Idle`, `Downloading`, `InstallInsufficientSpace`, `InstallInsufficientPower` and others) show the current state.

## Checked

Date: 2026-11-07. Read in full: Apple Platform Deployment "About software updates for Apple devices" (types of updates, power requirement table, HTTPS interception, Content Caching macOS 10.13, release table); apple/device-management YAML for `ScheduleOSUpdate` (InstallAction list, supervised, deprecated/removed versions, two-step iOS note, MaxUserDeferrals, UpdateResults Status values); and the `com.apple.applicationaccess` entries for `forceDelayedSoftwareUpdates`, `enforcedSoftwareUpdateDelay` (read only those key entries, not the whole file). Removed: "Apple silicon needs a bootstrap token or admin credentials", the Jamf Pro menu path, `softwareupdate -l` Verify, "a week before the main ring", the Terminal-install gotcha and the "blocking only with the restrictions payload" claim, none of which the pages state.
Method: documentation only; no commands were run.
