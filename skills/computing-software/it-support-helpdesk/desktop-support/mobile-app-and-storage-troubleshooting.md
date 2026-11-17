---
id: computing-software.it-support-helpdesk.desktop-support.mobile-app-and-storage-troubleshooting
name: mobile-app-and-storage-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, mobile-device-support, mobile-app-troubleshooting, ios, android, app-crash, clear-cache, offload-app, storage-full, managed-apps, comptia-a-plus]
level: intro
status: draft
description: "Resolve mobile app crashes, failed updates and storage-full errors on iOS and Android: force stop, clear cache vs data, offload/reinstall, OS updates, and managed-app caveats."
sources:
  - "https://support.apple.com/guide/iphone/welcome/ios"
  - "https://support.google.com/android/"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mobile-app-and-storage-troubleshooting

Goal: fix "the app keeps closing / won't update" on a phone in the order
that loses the least data (A+ 220-1202 mobile OS troubleshooting).

## Ladder (stop when fixed)
1. **Force close** and reopen (iOS: swipe up from app switcher; Android:
   Settings → Apps → app → Force stop).
2. **Restart the phone.**
3. **Update the app and the OS** — many crashes are fixed versions;
   managed apps may be held at a version by MDM.
4. **Clear cache** (Android: Settings → Apps → app → Storage → Clear cache;
   keeps logins/data). iOS has no per-app cache clear — use the app's own
   setting or step 5.
5. **Offload** (iOS: Settings → General → iPhone Storage → app → Offload App
   — keeps documents and data, reinstalls binary) / Android **Clear storage**
   (removes app data and sign-in — check what's unsynced first).
6. **Delete and reinstall** — managed apps reinstall via Company Portal;
   app protection data is re-provisioned on sign-in.

## Storage full
- iOS: Settings → General → iPhone Storage — recommendations, "Review large
  attachments", Photos optimise storage (iCloud), message retention 1 year.
  "System Data"/"Other" balloons from caches; a restart or backup/restore
  shrinks it.
- Android: Settings → Storage → Free up space; Files by Google for
  duplicates and large files.
- Below ~1–2 GB free, OS updates fail and apps crash — free space before
  updating.

## Network-dependent failures
App works on Wi-Fi but not mobile data → Settings → Mobile data → per-app
toggle off. Corporate Wi-Fi with TLS inspection breaks certificate-pinned
apps — test on mobile data.

## Managed device caveats
- App removed/blocked by MDM compliance → Company Portal shows why.
- Work profile (Android): work apps have a briefcase badge; the personal
  copy of the same app is a different install.
- Don't factory reset an enrolled corporate device without checking
  Activation Lock / FRP and MDM re-enrolment steps.

## Verify
App opens and performs the user's failing action twice in a row; free
storage above 10 % of capacity.
