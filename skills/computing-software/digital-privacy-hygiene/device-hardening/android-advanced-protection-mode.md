---
id: computing-software.digital-privacy-hygiene.device-hardening.android-advanced-protection-mode
name: android-advanced-protection-mode
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, android-advanced-protection, android, advanced-protection, high-risk-users, sideloading, 2g, memory-tagging]
level: practitioner
status: draft
description: "Enable Android 16 Advanced Protection to lock down a phone for high-risk users: blocks sideloading and 2G, forces Play Protect, USB protection and safer Chrome."
sources:
  - "https://developer.android.com/about/versions/16/features"
  - "https://security.googleblog.com/"
  - "https://landing.google.com/advancedprotection/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Android Advanced Protection mode

**Goal:** one switch that applies Google's strictest device protections for journalists, officials,
activists and anyone targeted by spyware.

## Turn it on
Android 16+: Settings > Security & privacy > **Advanced Protection** > Device protection on. It is distinct
from (but complements) the Google account **Advanced Protection Program**, which hardens the account with
security keys or passkeys.

## What it enforces
- **Install unknown apps** blocked; existing sideload permissions revoked.
- **Google Play Protect** forced on, cannot be disabled.
- **2G network** disabled (blocks downgrade attacks by fake base stations).
- **USB protection**: new USB data connections blocked while locked (charging only).
- **Inactivity reboot** when locked for a long period.
- **Memory Tagging Extension** on supported hardware (Pixel 8 and later) to catch memory corruption exploits.
- **Chrome**: always use HTTPS, site isolation, and the JavaScript optimizer turned off for unknown sites.
- **Google Messages**: scam detection on; links from unknown senders treated cautiously.
- Theft detection and offline device lock features on.

## Trade-offs
- No sideloaded apps at all (F-Droid users must choose).
- Some sites run slower in Chrome; some USB accessories need unlocking first.
- Settings it controls show as managed and greyed out; you turn the whole mode off to change one.

## Pair with
- Strong alphanumeric passcode and a supported, fully patched device.
- Google account Advanced Protection Program enrollment.

## Verify
- [ ] Settings shows Advanced Protection on; Install unknown apps greyed out; 2G toggle greyed out.
