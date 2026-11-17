---
id: computing-software.digital-privacy-hygiene.device-hardening.android-extend-unlock-risks
name: android-extend-unlock-risks
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, extend-unlock, screen-lock, android-theft-protection]
level: practitioner
status: draft
description: "Review Android Extend Unlock (Smart Lock) trusted devices, places and on-body detection, which can keep a stolen phone unlocked, and set safer options."
sources:
  - "https://support.google.com/android/answer/9075927"
  - "https://source.android.com/docs/security/features/trusty"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Android Extend Unlock risks

**Goal:** convenience features don't leave a grabbed phone unlocked.

## What it does
Settings > Security & privacy > More security settings > **Extend Unlock** (formerly Smart Lock). Keeps the phone
unlocked under conditions:
| Option | Risk |
|---|---|
| On-body detection | Phone stays unlocked while moving after being unlocked once, including in a thief's pocket |
| Trusted places | Home location keeps it unlocked for anyone in your home (or a spoofed location) |
| Trusted devices (Bluetooth) | Car or watch connection keeps it unlocked; a phone stolen from the car stays open |

Modern versions limit extended unlock to a maximum period (about 4 hours) before requiring credentials again.

## Safer settings
- Turn off on-body detection.
- Trusted places off if you share your home with people who shouldn't access the phone.
- Trusted devices: only a watch you wear, not the car or headphones.
- Pair with Theft Detection Lock (locks when snatched) in Google's theft protection.

## Check other unlock paths
- Face unlock on Android phones without secure 3D sensors is classed as less secure (convenience tier); can't
  unlock apps like banking.
- Fingerprint is fine; use Lockdown in high-risk moments.

## Gotchas
- Work profiles may disable Extend Unlock via policy.
- Extend Unlock isn't the same as Smart Lock for Passwords (old Google password saving name).
