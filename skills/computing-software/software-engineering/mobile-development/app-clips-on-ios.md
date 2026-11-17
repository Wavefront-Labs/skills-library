---
id: computing-software.software-engineering.mobile-development.app-clips-on-ios
name: app-clips-on-ios
category: computing-software
field: software-engineering
product: mobile-development
tags: [mobile-development, ios, app-clips, app-clip-experience, invocation-urls, size-limit, nfc, app-store-connect]
level: practitioner
status: draft
description: "Build and ship an iOS App Clip: target setup, invocation URLs and AASA, size limits, shared code with the full app, and App Store Connect experiences."
sources: ["https://developer.apple.com/documentation/appclip", "https://developer.apple.com/documentation/appclip/creating-an-app-clip-with-xcode", "https://developer.apple.com/documentation/appclip/configuring-your-app-clip-s-launch-experience"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# App Clips on iOS

An App Clip is a small part of your app launched from a link, QR code, NFC tag, Maps place card or Messages without installing the app.

## Setup
1. In Xcode add a target: File > New > Target > App Clip. Bundle id must be `<app-bundle-id>.Clip`.
2. Share code through a Swift package or by adding files to both targets; guard clip-only paths with the `APPCLIP` active compilation condition.
3. Add the Associated Domains entitlement to the clip: `appclips:example.com`; the app also needs `applinks:example.com`.
4. Host the `apple-app-site-association` file at `https://example.com/.well-known/apple-app-site-association` with an `appclips` section listing the app id.
5. In App Store Connect configure the default App Clip experience (title, subtitle, header image) and optional advanced experiences per URL prefix.

## Handling the launch
```swift
.onContinueUserActivity(NSUserActivityTypeBrowsingWeb) { activity in
    guard let url = activity.webpageURL else { return }
    route(url)           // jump straight into the task, no onboarding
}
```

## Limits and gotchas
- Size cap: the thinned App Clip binary must be under 15 MB for iOS 17 and later (10 MB on iOS 16 and earlier); check Apple's current figure.
- Clips cannot use some frameworks and have limited persistence and permissions (notifications and location are time-limited, confirm current rules).
- Use `SKOverlay` / `StoreKit` to offer the full app; data in the shared app-group container can be handed over.
- Test invocations with the Local Experiences setting on a device (Settings > Developer > Local Experiences).

Verify: archive and check the App Clip size in the App Thinning Size Report; launch from a registered URL on a device and confirm the clip opens to the right screen.
