---
id: computing-software.qa-testing-engineering.exploratory-testing.deep-links-and-push-notification-testing
name: deep-links-and-push-notification-testing
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [deep-link-testing, push-notification-testing, universal-links, app-links, mobile-testing]
level: practitioner
status: draft
description: "Test deep links (universal links, App Links, custom schemes) and push notifications: cold and warm starts, logged-out routing, adb/simctl triggers and payload variants."
sources:
  - https://www.istqb.org/certifications/mobile-application-testing
  - https://developer.android.com/training/app-links
  - https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Deep links and push notification testing

**Goal:** every link and notification opens the right screen in every app state, or degrades gracefully.

## Deep links
Types: custom schemes (`myapp://order/42`), Android App Links and iOS Universal Links (https URLs verified via `/.well-known/assetlinks.json` and `/.well-known/apple-app-site-association`).

Trigger them:
```bash
adb shell am start -W -a android.intent.action.VIEW -d "https://shop.example.com/order/42" com.example.app
adb shell pm get-app-links com.example.app          # verification state per domain (Android 12+)
xcrun simctl openurl booted "https://shop.example.com/order/42"
```
Also from real sources: email, SMS, chat apps, QR codes, browsers (in-app browsers often do not open universal links).

Cases: app not installed (falls back to web or store), installed but cold start, warm (backgrounded), already on another screen, logged out (route after login to the original target), invalid or expired IDs, links to content the user may not access, verification file broken or served with redirects (universal links then fail silently).

## Push notifications
- Send test pushes: Firebase console or FCM HTTP v1 API, APNs via provider tools or `xcrun simctl push booted com.example.app payload.apns` on the simulator.
- States: foreground (app shows in-app banner or not), background, killed, device locked, Do Not Disturb/Focus.
- Tap opens the right screen (deep link in payload); action buttons work.
- Permission flows: denied, later enabled in settings; Android 13+ runtime permission `POST_NOTIFICATIONS`.
- Payload variants: long text, emoji, missing optional fields, localisation, images (rich push), silent/data-only pushes triggering sync.
- Token refresh after reinstall or login as another user; logout stops pushes for that account.

## Verify
A matrix of link and push types against app states (not installed, killed, background, foreground, logged out) is all green on both platforms.
