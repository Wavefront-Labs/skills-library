---
id: computing-software.digital-privacy-hygiene.device-hardening.sideloading-risks-and-safe-practice
name: sideloading-risks-and-safe-practice
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, sideloading, install-unknown-apps, apk, play-protect, apksigner, alternative-app-marketplaces]
level: practitioner
status: draft
description: "Decide when sideloading apps is acceptable on Android and iOS (EU marketplaces), verify APK signatures, and close the install-unknown-apps permission afterwards."
sources:
  - "https://developer.android.com/tools/apksigner"
  - "https://www.privacyguides.org/en/android/obtaining-apps/"
  - "https://support.google.com/googleplay"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sideloading risks and safe practice

**Goal:** installing apps from outside the main store is the top Android malware route and a common scam
tactic; do it only deliberately and verifiably.

## Why scammers push it
- "Install our app to receive your refund / track your parcel / get the job" links lead to APKs with
  Accessibility abuse, SMS reading (2FA theft) and remote control.
- Investment scams send iPhone users TestFlight links or ask them to install a configuration/MDM profile.
- Rule: any stranger asking you to install an app from a link, or a profile, is attempting fraud.

## Android
- Each source needs **Install unknown apps** (Settings > Apps > Special app access). Grant it to one app
  (e.g. F-Droid or Obtainium), install, then **turn it back off** for browsers and messengers.
- Keep **Google Play Protect** on (Play Store > profile > Play Protect); it scans sideloaded apps.
- Prefer reputable sources: F-Droid (reproducible builds for many apps), the developer's GitHub releases via
  Obtainium, not mirror sites.
- Verify the signing certificate against the developer's published fingerprint:
  ```bash
  apksigner verify --print-certs app.apk   # compare SHA-256 digest
  ```
  On-device, AppVerifier does the same. Updates must be signed by the same key or Android refuses them.
- Google is rolling out developer verification for sideloaded apps in some countries from 2026; unverified
  apps may need an advanced flow.

## iOS
- In the EU (iOS 17.4+), alternative marketplaces and web distribution exist; apps are still notarized by Apple
  but reviewed less. Use only well-known marketplaces.
- Elsewhere, "sideloading" means enterprise certificates, TestFlight or MDM profiles: refuse unless it is your
  employer's IT. Check Settings > General > VPN & Device Management for unknown profiles.

## Verify
- [ ] No browser/messenger holds Install unknown apps.
- [ ] Every sideloaded app has a known source and checked signature.
- [ ] No unexpected configuration profile on iPhones.
