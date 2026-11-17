---
id: computing-software.digital-privacy-hygiene.device-hardening.locked-and-hidden-apps-on-iphone
name: locked-and-hidden-apps-on-iphone
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, locked-hidden-apps, ios-18, face-id, mobile-privacy]
level: practitioner
status: draft
description: "Use iOS 18 Require Face ID and Hide and Require Face ID for apps, know what hiding conceals, and why it does not protect against someone with your passcode."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://support.apple.com/guide/personal-safety/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Locked and hidden apps

**Goal:** keep a few apps (photos vault, banking, messages, dating) private when you hand your unlocked phone to
someone.

## Lock an app (iOS 18+)
Long-press the app icon > **Require Face ID** (or Touch ID/Passcode) > Require Face ID. Opening it now needs
authentication, and its content doesn't appear in Search, notifications previews or Siri suggestions.

## Hide an app
Long-press > Require Face ID > **Hide and Require Face ID**. The app disappears from the Home Screen and moves to a
locked **Hidden** folder at the bottom of the App Library. Notifications and calls from hidden apps are suppressed.
Built-in Apple apps can be locked but not all can be hidden.

## Limits
- Anyone who knows your **passcode** can open locked/hidden apps; biometric failure falls back to the passcode.
- Hidden apps still appear in Settings > Apps and in purchase history in the App Store.
- Screen Time and family organiser may see app usage.
- In a coercive or abusive situation, hiding can be noticed; see Safety Check and the personal safety guide.

## Android equivalents
Private Space (Android 15), Samsung Secure Folder, or per-app locks offered by some OEM launchers.

## Verify
Hand the phone over unlocked and confirm the app asks for Face ID and the Hidden folder is locked.
