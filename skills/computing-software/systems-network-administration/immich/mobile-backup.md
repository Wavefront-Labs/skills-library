---
id: computing-software.systems-network-administration.immich.mobile-backup
name: mobile-backup
category: computing-software
field: systems-network-administration
product: immich
tags: [mobile-app, background-backup, album-sync, android, ios]
level: intro
status: docs-checked
description: "Configure Immich mobile backup: album selection, checksum deduplication, Wi-Fi only, album sync, Android battery and iOS background refresh."
sources:
  - https://docs.immich.app/features/mobile-backup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have phone photos and videos upload automatically to your server.

When backup is enabled, Immich uploads new items from the selected albums when you open or resume the app and periodically in the background.

General settings:

- Backup albums: choose which device albums to back up. Double-tap an album to exclude it; useful on iOS where an asset can belong to several albums.
- Deduplication: on first selection Immich computes a checksum of each file's content. Files matching assets already on the server, whether uploaded by CLI, web or another device, are skipped, saving bandwidth.
- Networking: by default uploads happen only on Wi-Fi; change this on the backup settings page.
- Album synchronisation: when enabled, Immich creates server albums mirroring your device albums. It is one-way, from device to server. Use "Reorganize into album" to backfill existing uploads.

Android:

- Aggressive battery optimisation on some models can stop the background worker; see dontkillmyapp.com for how to disable it on your phone.
- You can restrict the background task to run only while charging.
- You can set a minimum delay between taking a photo and the background upload.

iOS:

- Enable Background App Refresh in Settings, General, Background App Refresh.
- iOS controls when the background task runs; opening the app more often makes background tasks run more often.
- iCloud assets in backed-up albums are pulled into the app cache temporarily during hashing and upload, using extra data and storage.

## Checked

2026-11-09. Confirmed against the Immich docs (https://docs.immich.app/) by reading features/mobile-backup in full.
Removed: nothing.
Method: documentation only; no commands were run.
