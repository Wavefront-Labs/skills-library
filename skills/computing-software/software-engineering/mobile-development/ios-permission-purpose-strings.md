---
id: computing-software.software-engineering.mobile-development.ios-permission-purpose-strings
name: ios-permission-purpose-strings
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, purpose-strings, info-plist, usage-description, nscamerausagedescription, app-store-review, privacy-permissions]
level: intro
status: draft
description: "Write iOS permission purpose strings that pass review: required Info.plist keys per API, specific wording, localisation and the crash when a key is missing."
sources: ["https://developer.apple.com/documentation/bundleresources/information-property-list/protected-resources", "https://developer.apple.com/design/human-interface-guidelines/privacy", "https://developer.apple.com/app-store/review/guidelines/#5.1.1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# iOS permission purpose strings

Each protected resource needs an Info.plist key whose value is shown in the system permission alert. A missing key makes the app terminate on first access (crash log: `This app has crashed because it attempted to access privacy-sensitive data without a usage description`), and App Store Connect rejects uploads for some missing keys.

| Resource | Key |
|---|---|
| Camera | `NSCameraUsageDescription` |
| Microphone | `NSMicrophoneUsageDescription` |
| Photo library read | `NSPhotoLibraryUsageDescription` |
| Photos add-only | `NSPhotoLibraryAddUsageDescription` |
| Location while in use | `NSLocationWhenInUseUsageDescription` |
| Location always | `NSLocationAlwaysAndWhenInUseUsageDescription` |
| Contacts | `NSContactsUsageDescription` |
| Face ID | `NSFaceIDUsageDescription` |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` |
| Tracking (ATT) | `NSUserTrackingUsageDescription` |

```xml
<key>NSCameraUsageDescription</key>
<string>Scan a receipt so we can add it to your expenses.</string>
```

## Writing them
- State the concrete user benefit and the feature that needs it; not "required for the app to work".
- Guideline 5.1.1 requires purpose strings that clearly and completely describe use; vague strings are a common rejection reason.
- Ask in context, just before the feature, not at launch.
- Localise via `InfoPlist.strings` per language (or a String Catalog named `InfoPlist`).

## Gotchas
- Linking an SDK that touches a protected API adds the requirement to your app even if you never call it; scan with `plutil -p Info.plist` and a binary string search.
- Location needs two steps for "Always": request when-in-use first, then upgrade.
- After denial the system will not show the alert again; send users to Settings with `UIApplication.openSettingsURLString`.

Verify: on a clean simulator, trigger each feature and confirm the alert text; run `plutil -p Info.plist | grep UsageDescription` on the archive to compare with the list of frameworks you link.
