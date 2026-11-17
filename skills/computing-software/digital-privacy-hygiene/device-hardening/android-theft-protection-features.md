---
id: computing-software.digital-privacy-hygiene.device-hardening.android-theft-protection-features
name: android-theft-protection-features
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, android-theft-protection, android, android-security, theft-detection-lock, offline-device-lock, remote-lock, identity-check, factory-reset-protection]
level: intro
status: draft
description: "Enable Android's theft protection: Theft Detection Lock, Offline Device Lock, Remote Lock by phone number, Identity Check, and factory reset protection."
sources:
  - "https://support.google.com/android/answer/15146908"
  - "https://security.googleblog.com/2024/05/io-2024-whats-new-in-android-security.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android theft protection

**Goal:** a snatched-while-unlocked phone should lock itself before the thief can reset
accounts, and be useless to resell.

## Settings (Android 10+ via Google Play services; Identity Check on Android 15+ Pixel/Samsung)
Settings > Google > All services > **Theft protection** (or Security & privacy > Device
unlock > Theft protection):
- **Theft Detection Lock**: on-device AI detects a snatch-and-run motion and locks the screen.
- **Offline Device Lock**: locks the screen if the phone is kept offline for an extended
  period (thieves turn off data to stop remote wipe).
- **Remote Lock**: lock the phone from `android.com/lock` using only your phone number +
  a security challenge, when you can't remember your Google password under stress.
- **Identity Check**: outside trusted places, requires biometrics (no PIN fallback) to
  change Google account settings, turn off theft protection, or access passkeys/passwords.
- Find Hub (Find My Device) on, with "Store recent location".

## Also
- **Factory Reset Protection** is automatic with a Google account: after reset, the phone
  needs the previous account. Remove your account before selling.
- Stronger lock: 6+ digit PIN or alphanumeric; short screen timeout.
- Lock screen: hide sensitive notification content.

## Verify
- [ ] Theft protection toggles on; Remote Lock tested from another device.
- [ ] Find Hub shows the phone.
