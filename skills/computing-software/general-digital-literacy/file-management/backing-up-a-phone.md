---
id: computing-software.general-digital-literacy.file-management.backing-up-a-phone
name: backing-up-a-phone
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, backup, phone-backup, icloud-backup, google-one-backup, android-backup, itunes-backup, finder-backup, photos-backup, whatsapp-backup]
level: intro
status: draft
description: "Back up an iPhone (iCloud or computer) or Android phone (Google One), check it ran, and know what each backup misses (WhatsApp, 2FA apps, local files)."
sources:
  - https://support.apple.com/guide/iphone/welcome/ios
  - https://support.google.com/android
  - https://support.apple.com/guide/icloud/welcome/icloud
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backing up a phone

**Goal:** if the phone is lost or broken, a new one can be restored with your photos, contacts and apps.

## iPhone
- **iCloud:** Settings › [your name] › iCloud › **iCloud Backup** › on. Backs up nightly when charging,
  locked and on Wi-Fi. Free 5 GB is rarely enough: iCloud+ 50 GB/200 GB.
- **Computer:** connect via USB › Mac Finder (sidebar device) or Windows **Apple Devices** app /
  iTunes › Back Up Now; tick **Encrypt local backup** to include saved passwords, Health and Wi-Fi data.
- Check: Settings › [name] › iCloud › iCloud Backup shows "Last successful backup".

## Android
- Settings › Google › **Backup** (or System › Backup) › *Backup by Google One* on › Back up now.
  Covers apps and data, call history, contacts, settings, SMS, and photos via Google Photos.
- Samsung also offers Samsung Cloud / Smart Switch to a PC.

## What's often missing
- **WhatsApp/Signal chats**: their own backup (see chat-backup skill).
- **Authenticator apps**: enable cloud backup in the app (Google Authenticator sync, Microsoft
  Authenticator backup) or keep recovery codes.
- Files in other apps' private storage; music not from a store.

## Gotchas
- Photos synced to iCloud/Google Photos are a sync, not a separate backup; deleting deletes everywhere.
  Keep a second copy on a computer or drive for irreplaceable photos.

## Verify
- [ ] "Last backup" is within the last day or two.
