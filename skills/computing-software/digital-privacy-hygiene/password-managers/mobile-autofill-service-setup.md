---
id: computing-software.digital-privacy-hygiene.password-managers.mobile-autofill-service-setup
name: mobile-autofill-service-setup
category: computing-software
field: digital-privacy-hygiene
product: password-managers
tags: [digital-privacy-hygiene, password-managers, mobile-autofill-service, autofill, ios-autofill, android-autofill-framework, accessibility-autofill, inline-autofill, passkeys]
level: intro
status: draft
description: "Make a third-party password manager the autofill provider on iOS and Android, including passkeys, and avoid the accessibility-service fallback where possible."
sources:
  - "https://bitwarden.com/help/auto-fill-ios/"
  - "https://bitwarden.com/help/auto-fill-android/"
  - "https://support.apple.com/guide/iphone/automatically-fill-in-passwords-iphf9219d8c9/ios"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mobile autofill service setup

**Goal:** the manager should fill logins in apps and browsers on the phone; when it
doesn't, people fall back to weak memorable passwords.

## iOS / iPadOS
1. Settings > General > **AutoFill & Passwords** (older iOS: Settings > Passwords >
   Password Options).
2. Turn on **AutoFill Passwords and Passkeys**, enable your manager under "AutoFill
   From". Leave Passwords (iCloud Keychain) on only if you deliberately use both.
3. In the manager app, approve its extension setup if prompted, then use the key icon
   above the keyboard (QuickType bar).
4. Passkeys: with the manager enabled, sites offer to save new passkeys to it.

## Android
1. Settings > Passwords & accounts (or System > Languages & input > Autofill service,
   varies by manufacturer) > **Preferred service** > your manager.
2. Android 14+ also has **Passwords, passkeys & accounts** where multiple credential
   providers can be enabled; enable your manager for passkeys there.
3. Inline autofill in keyboards (Gboard) shows suggestions in the suggestion strip;
   enable "Use inline autofill" in the manager if offered.
4. **Accessibility-based autofill** (draw-over + accessibility service) is a fallback for
   apps that don't support the Autofill Framework. It grants broad screen-reading
   power; enable only if needed and only for a trusted manager.

## Troubleshooting
- No suggestion in an app: the app may not declare its domain; add the
  `androidapp://package.name` URI or associated domain to the item.
- Samsung devices: Samsung Pass may be the default; switch it off.
- Chrome on Android: Settings > Autofill services > "Autofill using another service".

## Verify
- [ ] Login fill works in one browser and one native app.
- [ ] Creating a passkey on a test site offers your manager as destination.
