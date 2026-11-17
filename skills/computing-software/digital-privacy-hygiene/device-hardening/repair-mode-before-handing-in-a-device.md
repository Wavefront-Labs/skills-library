---
id: computing-software.digital-privacy-hygiene.device-hardening.repair-mode-before-handing-in-a-device
name: repair-mode-before-handing-in-a-device
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, repair-mode, lost-device-response, secure-erase]
level: practitioner
status: draft
description: "Protect your data when a phone or laptop goes in for repair: Pixel repair mode, Samsung maintenance mode, Apple's requirements, and a Windows technician account."
sources:
  - "https://support.google.com/pixelphone/answer/13531954"
  - "https://www.samsung.com/us/support/answer/ANS00091340/"
  - "https://support.apple.com/en-us/108044"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Repair mode before handing in a device

**Goal:** the technician can test the device without browsing your photos, messages and logged-in apps.

## Android
- **Pixel (Android 14+): Settings > System > Repair mode.** Creates an isolated environment; your data stays
  encrypted and inaccessible; exit with your screen lock afterwards.
- **Samsung: Settings > Battery and device care > Maintenance mode.** Creates a separate user; optional log
  creation; restart to exit with your credentials.

## iPhone/iPad
Apple and authorised providers usually require Find My turned off (or the device erased) for many repairs. Before
handing in:
1. Back up (iCloud or computer).
2. Follow Apple's current repair-prep instructions; if asked to erase, do so after backup.
3. Don't share your passcode unless required for a specific test; ask what it's for.
4. Turn Find My back on after you get it back.

## Windows laptop
- Create a temporary **standard local account** for the technician; give them that password only.
- Ensure BitLocker is on (data on other accounts stays protected).
- Sign out of password managers and browsers.

## Mac
Create a temporary standard user account; keep FileVault on. Apple's repair prep may also ask for Find My off.

## Always
- Remove SIM and memory cards where possible.
- Note serial numbers and the condition; check for profiles/apps added when you get it back.

## Gotchas
- Some independent shops ask for your passcode by default; repair mode removes the need.
- Expect the phone to be erased in some board-level repairs; backup first.
