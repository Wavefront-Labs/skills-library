---
id: computing-software.digital-privacy-hygiene.device-hardening.vetting-an-app-before-installing
name: vetting-an-app-before-installing
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, app-vetting, app-permissions, data-safety, privacy-nutrition-label, exodus-privacy, fake-apps]
level: intro
status: draft
description: "Check an app before installing: developer identity, Data safety / privacy label, permissions vs purpose, tracker reports from Exodus, update history and review patterns."
sources:
  - "https://reports.exodus-privacy.eu.org/"
  - "https://support.google.com/googleplay"
  - "https://www.apple.com/privacy/labels/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vetting an app before installing

**Goal:** a two-minute check that filters out data-harvesting, abandoned and impostor apps.

## Checklist
1. **Need**: could the website or a built-in feature do it? Fewer apps = less tracking and attack surface.
2. **Developer**: tap the developer name; is it the real company (bank, airline) with other known apps and a
   website that links back to this listing? Copycats use near-identical names and icons.
3. **Install count and age**: a "Chase Bank" with 5,000 installs, or a listing created last week, is wrong.
4. **Reviews**: read the 1-3 star ones and recent ones; bursts of short 5-star reviews indicate manipulation.
5. **Updated**: last update within a year; older apps miss OS privacy changes and fixes.
6. **Privacy disclosures**: Google Play **Data safety** section; App Store **App Privacy** label ("Data Used to
   Track You" is the important box). They are self-declared but a long tracking list is honest bad news.
7. **Permissions vs purpose**: flashlight, calculator, QR scanner, or wallpaper apps asking for contacts, SMS,
   location or accessibility are out.
8. **Trackers**: search the package name (from the Play URL `id=`) at Exodus Privacy for embedded tracker SDKs.
9. **Business model**: free with no ads or subscription usually means data sales; read the privacy policy's
   "sharing" section for "partners" and "affiliates".

## Category red flags
- Free VPNs, "cleaners", battery savers, antivirus from unknown vendors.
- Loan and crypto apps (extortion and fraud are common).
- Any app reached via an ad or a text message instead of searching the store.

## After installing
- Deny permissions at first launch; grant only when a feature needs it.
- Review it again in a month; delete if unused.

## Verify
- [ ] Developer, install count and Data safety checked for each new app.
