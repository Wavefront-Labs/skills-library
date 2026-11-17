---
id: computing-software.it-support-helpdesk.apple-device-management.update-deferrals
name: update-deferrals
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, sw-updates, update-deferrals, update-deferral, beta-control]
level: practitioner
status: docs-checked
description: "Configure update deferral windows and control beta enrolment on managed devices with the DDM softwareupdate.settings configuration and the legacy restriction keys."
sources:
  - "https://raw.githubusercontent.com/apple/device-management/release/declarative/declarations/configurations/softwareupdate.settings.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.applicationaccess.yaml"
  - "https://raw.githubusercontent.com/apple/device-management/release/mdm/profiles/com.apple.SoftwareUpdate.yaml"
  - "https://support.apple.com/guide/deployment/manage-software-updates-depc4c80847a/web"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# update-deferrals

Goal: predictable update cadence.
- Current method: `com.apple.configuration.softwareupdate.settings` (iOS 18, macOS 15, tvOS 18.4, visionOS 26 and later). Its `Deferrals` dictionary: `CombinedPeriodInDays` (not on macOS), `MajorPeriodInDays`, `MinorPeriodInDays` and `SystemPeriodInDays` (macOS only), each 1 to 90 days. On iOS, tvOS and visionOS deferrals need a supervised device; on macOS the configuration needs supervision. `MinorPeriodInDays` also defers major updates on iOS, `SystemPeriodInDays` covers system or non-OS updates, and Background Security Improvements are not covered by these deferrals.
- Beta control: the `Beta` dictionary (macOS 15.4 and later, supervised) with `ProgramEnrollment` of `Allowed`, `AlwaysOn` or `AlwaysOff` (default `Allowed`); `AlwaysOff` removes the device from any beta programs. `OfferPrograms` and `RequireProgram` take programs identified by an Apple School Manager or Apple Business seeding token.
- Legacy restriction keys (`com.apple.applicationaccess`, deprecated 26.0, removed 27.0, macOS 11.3 and later): `enforcedSoftwareUpdateMajorOSDeferredInstallDelay`, `enforcedSoftwareUpdateMinorOSDeferredInstallDelay`, `enforcedSoftwareUpdateNonOSDeferredInstallDelay`, each 1 to 90 days with default 30, controlling `forceDelayedMajorSoftwareUpdates`, `forceDelayedSoftwareUpdates` and `forceDelayedAppSoftwareUpdates`. `enforcedSoftwareUpdateDelay` (1 to 90, default 30) applies to the OS delay.
- Legacy macOS payload `com.apple.SoftwareUpdate` has `AllowPreReleaseInstallation` (default true; also deprecated 26.0, removed 27.0).
- Apple publishes a table of the dates when each release becomes visible on a device with a 90-day deferral.
Gotcha: a delay hides the release for that many days after its release date, so a long delay also delays security updates; keep minor windows short.
Verify: the `softwareupdate.beta-enrollment` and `softwareupdate.pending-version` status items are the related status items the settings configuration lists.

## Checked

Date: 2026-11-07. Read in full: apple/device-management `softwareupdate.settings` (Deferrals, Beta, ranges, OS minimums, enrolments) and the Apple Platform Deployment "About software updates" page (release table with the 90-day deferral column). Read the key entries (not the whole file) for `enforcedSoftwareUpdateMajor/Minor/NonOSDeferredInstallDelay`, `enforcedSoftwareUpdateDelay` and the force* keys in `com.apple.applicationaccess`, and the first 60 lines of `com.apple.SoftwareUpdate`. Removed: `allowBetaSoftwareUpdates` (no such key in the restrictions payload), "minor typically shorter", the "Beta channel absent in Settings" and "update list matches the window" Verify steps, and the staff-communication advice.
Method: documentation only; no commands were run.
