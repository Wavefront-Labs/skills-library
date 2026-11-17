---
id: computing-software.software-engineering.mobile-development.privacy-manifests-and-app-tracking-transparency
name: privacy-manifests-and-app-tracking-transparency
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-platform-services, privacy-manifest, app-tracking-transparency, required-reason-apis, privacy-nutrition-labels, data-safety]
level: practitioner
status: draft
description: "Meet mobile privacy requirements: Apple privacy manifests and required-reason APIs, App Tracking Transparency prompts, privacy labels, and Google Play Data safety declarations."
sources:
  - https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
  - https://developer.apple.com/documentation/bundleresources/describing-use-of-required-reason-api
  - https://developer.apple.com/documentation/apptrackingtransparency
  - https://support.google.com/googleplay/android-developer/answer/10787469
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Privacy manifests and App Tracking Transparency

**Goal:** accurate privacy disclosures for your code and every SDK, compliant tracking consent, and no submission rejections for missing declarations.

## 1. Apple privacy manifest (PrivacyInfo.xcprivacy)
A plist in the app and in each third-party SDK declaring:
- `NSPrivacyTracking` (bool) and `NSPrivacyTrackingDomains` (domains that are blocked until ATT consent is given).
- `NSPrivacyCollectedDataTypes`: types collected, whether linked to the user, used for tracking, and purposes.
- `NSPrivacyAccessedAPITypes`: **required-reason APIs** with approved reason codes:
```xml
<key>NSPrivacyAccessedAPITypes</key>
<array>
  <dict>
    <key>NSPrivacyAccessedAPIType</key><string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key><array><string>CA92.1</string></array>
  </dict>
  <dict>
    <key>NSPrivacyAccessedAPIType</key><string>NSPrivacyAccessedAPICategoryFileTimestamp</string>
    <key>NSPrivacyAccessedAPITypeReasons</key><array><string>C617.1</string></array>
  </dict>
</array>
```
Categories: UserDefaults, file timestamp, system boot time, disk space, active keyboards. Missing declarations get flagged at upload (ITMS-91053). Commonly used SDKs on Apple's list must include their own signed manifest; update old SDK versions.
Generate the aggregated **Privacy Report** in Xcode (Archive -> Generate Privacy Report) to fill App Store privacy nutrition labels.

## 2. App Tracking Transparency (iOS 14.5+)
Tracking = linking your data with other companies' data for ads/measurement, or sharing with data brokers. It requires permission:
```swift
// Info.plist: NSUserTrackingUsageDescription = "Allows us to show you more relevant offers."
import AppTrackingTransparency
let status = await ATTrackingManager.requestTrackingAuthorization()
// .authorized -> IDFA available; otherwise ASIdentifierManager returns zeros
```
- Request when the app is active (not during launch before the UI is visible, where the prompt can fail silently).
- No incentives for allowing, no custom pre-prompt that mimics the system dialog; a neutral explanation screen is allowed.
- Without consent you must not track by other means (fingerprinting is prohibited). SKAdNetwork/AdAttributionKit for privacy-preserving attribution.

## 3. Google Play Data safety
Declare data collected and shared (including by SDKs), purposes, encryption in transit, and deletion options. Must match behaviour, privacy policy and SDK disclosures; Google cross-checks. Android's Advertising ID requires the `com.google.android.gms.permission.AD_ID` permission (targeting API 33+) and respects the user's opt-out/deletion of the ID.

## 4. Process
- Maintain an SDK inventory: what each collects, version, manifest present, consent dependencies.
- Gate analytics/ads SDK initialisation on consent where required (GDPR/ePrivacy consent management platforms, ATT).
- Re-review disclosures on every SDK addition or upgrade; privacy labels are per app, not per version, so keep them current.

## Gotchas
- Declaring "no tracking" while an ads SDK fingerprints devices is a policy violation and a review risk.
- Required-reason declarations must reflect actual use; picking a reason that does not apply is a guideline violation.
- Analytics on web views and backend-side data sharing also count toward disclosures.

## Verify
- The Xcode privacy report lists all SDKs with manifests, App Store Connect upload produces no ITMS-9105x warnings, ATT denial results in no tracking-domain traffic (proxy check), and the Play Data safety form matches the SDK inventory.
