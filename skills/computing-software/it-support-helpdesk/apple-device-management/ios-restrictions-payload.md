---
id: computing-software.it-support-helpdesk.apple-device-management.ios-restrictions-payload
name: ios-restrictions-payload
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, supervised-ios, ios-restrictions-payload, restrictions, ios-restrictions]
level: practitioner
status: docs-checked
description: "Restrictions payload (com.apple.applicationaccess) keys for iPhone and iPad: AirDrop, camera, iCloud backup, app removal, profile install and which need supervision."
sources:
  - https://github.com/apple/device-management/blob/release/mdm/profiles/com.apple.applicationaccess.yaml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ios-restrictions-payload

Goal: lock down corporate devices sensibly using the restrictions payload, `com.apple.applicationaccess`.

Key facts from Apple's published payload definition (apple/device-management):
- `allowAirDrop` (default true): `false` disables AirDrop. On iOS it needs a supervised device and is not allowed under User Enrollment.
- `allowCamera` (default true): `false` disables the camera and removes its icon. Support on unsupervised devices is deprecated.
- `allowCloudBackup` (default true): `false` disables backup to iCloud. Support on unsupervised devices is deprecated.
- `forceEncryptedBackup` (default false): `true` makes the system encrypt all backups.
- `allowAppRemoval` (default true, iOS supervised): `false` disables removal of apps, including App Store, marketplace and locally installed apps.
- `allowAppInstallation` (default true, iOS supervised): `false` disables the App Store and removes its icon, so users cannot install or update apps; MDM commands can override it.
- `allowUIConfigurationProfileInstallation` (default true, iOS supervised): `false` stops the user installing configuration profiles and certificates interactively.
- `allowAppClips` (default true, iOS 14.0 and later, supervised): `false` stops users adding App Clips and removes existing ones.
- `allowPersonalHotspotModification` (default true, supervised): `false` disables changes to the Personal Hotspot setting.
- `ratingApps` (integer 0 to 1000, default 1000): maximum app content rating allowed; for example 600 is 17+, 300 is 12+ and 1000 is All.
- `blacklistedAppBundleIDs` (supervised, iOS 9.3 to 15.0, deprecated): Apple points to the declarative `com.apple.configuration.app.settings` configuration instead.
- Managed Open In: `allowOpenFromManagedToUnmanaged` and `allowOpenFromUnmanagedToManaged` (default true each) keep documents in managed apps and accounts opening only in other managed ones, and the reverse.

Practice: keep restrictions in layered profiles (baseline plus role-specific) so exceptions are small, apply by group with a pilot first, and keep a test iPad on the strictest profile to find usability breakage early. Re-read the payload definition after each OS release, since keys are introduced and deprecated over time.
Gotcha: over-restricting blocks features users depend on, for example `allowPersonalHotspotModification` set to `false` stops hotspot changes; test the common support scenarios.
Verify:
- Setting is greyed out on the device.
- Support scenarios still pass.

## Checked
2026-11-08. Checked each key above against the YAML payload definition in Apple's device-management repository (default, supervision requirement, deprecation, description, rating values). Removed: the Apple Support deployment-guide sources (they load as a JavaScript shell of the guide welcome page), the old "supervised-only" grouping (the definition also marks `allowAirDrop` and `allowAppRemoval` supervised on iOS, and lists `blacklistedAppBundleIDs` as deprecated), the Wi-Fi Assist reference, and the "passcode rules" scope. Fetched as the raw file of the same path.

Method: documentation only; no commands were run.
