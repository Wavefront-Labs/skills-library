---
id: computing-software.digital-privacy-hygiene.device-hardening.checking-android-security-patch-level
name: checking-android-security-patch-level
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, android-security-patch-level, android, security-bulletin, google-play-system-update, end-of-support]
level: intro
status: docs-checked
description: "Read an Android phone's security patch level and Play system update date, judge whether the device is still supported, and decide when to replace it."
sources:
  - "https://source.android.com/docs/security/bulletin"
  - "https://www.privacyguides.org/en/os/android-overview/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Checking the Android security patch level

**Goal:** know whether a phone is actually receiving fixes, because vendors stop patching on different schedules.

## Read the dates
- In Settings, find the phone's **Android security update** (patch level) and **Google Play system update** dates;
  the screens are under About phone or Security settings and the exact path varies by vendor, so search Settings.
- Google Play system updates: since Android 10 Google can push security fixes for some system components through
  Google Play, independent of the vendor.

## Interpret
- Google and device makers publish fixes through the Android Security Bulletins (Android platform, upstream Linux
  kernel and SoC manufacturer fixes are covered); Pixel devices have their own Pixel Update Bulletins at
  source.android.com/docs/security/bulletin.
- Firmware updates are critical: without them a device cannot be secure. Closed-source components are supported by
  the chip maker for a limited period, so a device past that end of life cannot get those fixes from the vendor.
- A vendor can promise a long support period while the SoC's own support ends sooner (Privacy Guides gives a
  Fairphone example), so check the chip's end of life as well as the phone maker's promise.

## Act
- Install pending updates and restart.
- Patch level stuck and the vendor has ended support: replace the phone, or use a maintained alternative OS where
  your model is supported (Privacy Guides covers GrapheneOS for supported Pixels).

## Gotchas
- A recent Google Play system update does not mean firmware and vendor patches are current.

## Verify
- [ ] Patch level date noted and compared with the current Android Security Bulletin.
- [ ] The model's support end date looked up on the vendor's site and noted for replacement planning.

## Checked
2026-11-01. Confirmed on the Android Security Bulletins index (bulletin types, Pixel bulletins) and Privacy Guides
"Android overview" (firmware updates critical, limited support periods, EOL devices stay unpatched, Play system
updates from Android 10, Fairphone/SoC example). Removed: exact menu paths, adb command, `-01`/`-05` patch level
meaning, "2-3 months behind" and "~60 days" thresholds, 7-year and 2-3-year support figures, carrier-lag claim,
antivirus claim (not stated on the pages read).
Method: documentation only; no commands were run.
