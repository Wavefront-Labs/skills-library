---
id: computing-software.software-engineering.mobile-development.mobile-analytics-and-event-tracking
name: mobile-analytics-and-event-tracking
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, mobile-analytics, firebase-analytics, event-tracking, tracking-plan, consent-mode, debugview, product-analytics]
level: practitioner
status: docs-checked
description: "Instrument mobile product analytics: a tracking plan, Firebase Analytics events and default parameters, consent mode v2, and debugging events with DebugView."
sources:
  - https://firebase.google.com/docs/analytics/get-started
  - https://firebase.google.com/docs/analytics/events
  - https://firebase.google.com/docs/analytics/debugview
  - https://developers.google.com/tag-platform/security/guides/app-consent
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Product analytics and event tracking

**Goal:** analytics data that answers product questions reliably, collected with consent, and that does not rot as the app changes.

## Start with a tracking plan
Before code, write a table (in the repo): event name, trigger, properties, platforms, owner, the question it answers. Review changes like code. The conventions below are team practice, not Firebase requirements:
- `object_action` in snake_case, for example `signup_completed`, `checkout_started`.
- Consistent parameter names across events; track outcomes rather than every tap.
- Event names are case-sensitive: names differing only in case are two distinct events, so fix one spelling in the plan.

## Firebase Analytics (Google Analytics for Firebase)
```swift
Analytics.logEvent("share_image", parameters: [
  "name": name,
  "full_text": text,
])
```
- Analytics logs some events automatically. Beyond those you can log up to 500 different event types; there is no limit on total event volume.
- Prefer the SDK's **recommended events** with their prescribed parameters for maximum detail in reports and to benefit from new Google Analytics features.
- Custom parameters can be used as custom dimensions (non-numerical) or custom metrics (numerical). After logging one, register it in the Firebase console under Analytics > Custom Definitions or it will not appear in reports. Custom parameters are also included in the BigQuery export if the app is linked to a BigQuery project.
- `setDefaultEventParameters` attaches parameters to all future events; a value passed in `logEvent` overrides the default, and setting a default to nil clears it. Register default parameters too.
- The `value` parameter (`kFIRParameterValue` on Apple platforms) is general purpose for accumulating a key metric such as revenue, distance, time or points.

## Consent
Consent mode adjusts SDK behaviour to users' consent status. Prerequisites: the Analytics for Firebase SDK and a consent banner or consent management platform (CMP).
- By default no consent values are set. On Apple platforms set defaults in `Info.plist` with `GOOGLE_ANALYTICS_DEFAULT_ALLOW_ANALYTICS_STORAGE`, `..._ALLOW_AD_STORAGE`, `..._ALLOW_AD_USER_DATA` and `..._ALLOW_AD_PERSONALIZATION_SIGNALS` (true = granted, false = denied; `eu_consent_policy` for the last two denies consent only in regions under the EU user consent policy).
- Update later with `setConsent`; the value overrides the default, persists across launches, and only updates the parameters you pass.
```swift
Analytics.setConsent([
  .analyticsStorage: .granted,
  .adStorage: .granted,
  .adUserData: .granted,
  .adPersonalization: .granted,
])
```
- Consent mode v2 (Oct 30 2023) added `ad_user_data` and `ad_personalization`; existing users must upgrade both the plist and the consent calls.
- If a user withdraws analytics or ad storage consent, Google Analytics deletes all user properties, including the ad personalization consent; restore that value with `setConsent` to keep the user's choice.
- Verify by enabling verbose logging and looking in the Xcode console for `ad_storage`, `analytics_storage`, `ad_user_data` and `ad_personalization` messages.

## Debugging
- Events are normally batched and uploaded about once an hour. For validation enable debug mode to upload with minimal delay: iOS launch argument `-FIRDebugEnabled` (disable with `-FIRDebugDisabled`); Android `adb shell setprop debug.firebase.analytics.app PACKAGE_NAME` (disable with `adb shell setprop debug.firebase.analytics.app .none.`). The setting persists until disabled.
- Firebase console: Analytics > DebugView shows a seconds stream (last 60 seconds), a minutes stream (last 30 minutes), top events and current user properties, with a device selector. Error events and events with a `firebase_error` parameter appear there (click the event to see the parameter).
- Events logged in debug mode are included in the daily BigQuery export by default; configure a developer traffic data filter in the Analytics property to keep test traffic out of reports and exports.
- To see events in the Xcode console add `-FIRAnalyticsVerboseLoggingEnabled`. The Events dashboard updates periodically through the day, so use the console for immediate checks.

## Verify
- [ ] Every event in code exists in the tracking plan.
- [ ] Custom parameters registered under Custom Definitions.
- [ ] Consent values logged as expected in the console; key events visible in DebugView from a test device.

## Checked
Confirmed on 2026-11-08 against the four cited Firebase and Google tag-platform pages: 500 event types, case sensitivity, recommended events, custom definitions, default parameters, BigQuery inclusion, DebugView behaviour and commands, consent mode keys, v2 parameters and withdrawal behaviour. Removed because the pages do not state them: parameter and name length limits, user property limits, the Kotlin and Android code, `setUserId`, `setAnalyticsCollectionEnabled`, `resetAnalyticsData`, automatic `screen_view` details, GA4 sampling claims, ATT, privacy manifest and Data safety statements, and third-party tooling suggestions.
Method: docs-only read of cited pages, 2026-11-08
