---
id: computing-software.digital-privacy-hygiene.device-hardening.detecting-unwanted-bluetooth-trackers
name: detecting-unwanted-bluetooth-trackers
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, unwanted-tracker-alerts, airtag, tile, samsung-smarttag, bluetooth-tracker, stalking, find-my, tracker-detect, physical-security]
level: intro
status: draft
description: "Find AirTags, Tiles or SmartTags being used to follow you: enable iOS and Android unknown-tracker alerts, scan manually, locate the tag, and disable it safely."
sources:
  - "https://ssd.eff.org/module/how-to-detect-bluetooth-trackers"
  - "https://support.apple.com/en-us/119874"
  - "https://support.google.com/android/answer/13658562"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detecting unwanted Bluetooth trackers

**Goal:** cheap item trackers are used for stalking (dropped in bags, hidden in cars).
Modern phones can detect most of them.

## Turn on alerts
- **iPhone**: Settings > Privacy & Security > Location Services on; System Services >
  Find My iPhone on; Bluetooth on; notifications for Find My (Tracking Notifications) on.
  iOS alerts for AirTags, Find My network accessories and (since iOS 17.5) other brands
  supporting the cross-platform standard.
- **Android 6+**: Settings > Safety & emergency > **Unknown tracker alerts** > Allow
  alerts. Same cross-platform standard (Apple and Google jointly specified it).

## Manual scan
- Android: Unknown tracker alerts > **Scan now** (about 10 seconds; move around).
- iPhone: no general scan; Find My app > Items > "Items That Can Track Me" lists detected.
- Older/non-compliant tags: Tile app's "Scan and Secure" detects Tiles; AirGuard (open
  source, Android/iOS) detects several types.

## When alerted
1. Play sound from the alert to locate it (bags, coat pockets, car wheel wells, under seats).
2. Tap the tag with NFC on your phone to see its serial and partial owner phone number
   (keep a screenshot as evidence).
3. Disable: AirTag twist the back and remove the battery; others per manufacturer.
4. If you fear for your safety, consider contacting police/an advocate **before** disabling;
   disabling may alert the stalker that you found it. Apple/Google cooperate with law
   enforcement on owner identity.

## Verify
- [ ] Alerts enabled on every family phone; scan done after suspicious situations.
