---
id: computing-software.digital-privacy-hygiene.device-hardening.phone-backups-icloud-google-and-computer
name: phone-backups-icloud-google-and-computer
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, phone-backup, backups, icloud-backup, google-one-backup, encrypted-local-backup, finder-backup, android-backup, photos-backup]
level: intro
status: draft
description: "Back up iPhone and Android phones properly: iCloud or Google backup settings, encrypted local backups to a computer, and what each backup actually includes."
sources:
  - "https://support.apple.com/en-us/108366"
  - "https://support.google.com/android/answer/2819582"
  - "https://support.apple.com/en-us/108353"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Phone backups

**Goal:** a lost or broken phone costs a few hundred dollars, not years of photos and
chats.

## iPhone
- **iCloud Backup**: Settings > [name] > iCloud > iCloud Backup > on (runs when charging,
  locked, on Wi-Fi). Needs enough iCloud storage. With Advanced Data Protection on, it's
  end-to-end encrypted.
- **Encrypted local backup**: connect to a Mac (Finder) or Windows (Apple Devices app) >
  Back up all data to this computer > **Encrypt local backup** (includes saved passwords,
  Health, Wi-Fi). Store the password.
- Photos with iCloud Photos sync aren't duplicated inside iCloud Backup.

## Android
- Settings > System/Google > **Backup** > Backup by Google One on: app data, call history,
  contacts, device settings, SMS/MMS; photos via Google Photos backup separately.
- Backups are encrypted with your screen lock for certain data (end-to-end for some
  categories); details vary by version.
- Samsung: Samsung Cloud/Smart Switch to a PC for local backups.

## Separately backed up apps
WhatsApp, Signal, authenticator apps, games: each has its own backup/transfer mechanism;
check them (see the Signal, WhatsApp and authenticator skills).

## Verify
- [ ] Last backup date within a week on every family phone.
- [ ] Authenticator and messenger backups confirmed separately.
