---
id: computing-software.general-digital-literacy.file-management.pausing-cloud-sync-and-metered-connections
name: pausing-cloud-sync-and-metered-connections
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-cloud-storage, pause-sync, metered-connection, onedrive, google-drive]
level: intro
status: draft
description: "Pause OneDrive, Google Drive, Dropbox and iCloud sync on a slow or metered connection, set Windows metered networks, and resume without creating conflicts."
sources:
  - https://support.microsoft.com/en-us/office/how-to-pause-and-resume-sync-in-onedrive-2152bfa4-a2a5-4d3a-ace8-92912fb4421e
  - https://support.google.com/drive/answer/10838124
  - https://help.dropbox.com/sync/pause-resume
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Pause sync and metered connections

## Pause
- **OneDrive:** click the cloud icon in the taskbar › gear › **Pause syncing** › 2, 8 or 24 hours. Resume from the same menu.
- **Google Drive for desktop:** Drive icon › gear › **Pause syncing**.
- **Dropbox:** Dropbox icon › your avatar › **Pause syncing**.
- **iCloud Drive (Mac):** Finder sidebar › iCloud Drive › the pause control next to the progress, or temporarily turn off on mobile data on iPhone (Settings › Mobile Data › iCloud Drive).

## Metered networks (hotspot, capped broadband)
- Windows: Settings › Network › Wi-Fi › your network › **Metered connection** On. OneDrive pauses automatically on metered networks (setting in OneDrive › Settings › Sync and back up › Advanced).
- Also stops Windows Update downloads and Store updates over that network.
- Limit bandwidth instead of pausing: OneDrive › Settings › Sync and back up › Advanced › **Upload/Download rate**; Google Drive › Preferences › Bandwidth.

## When to pause
- Tethering to a phone, video calls on weak Wi-Fi, replacing many files at once, or before reorganising a big folder (resume when done so it syncs once).

## Gotchas
- While paused, edits on two devices to the same file cause **conflict copies** on resume (`Report-DESKTOP-ABC.docx`). Avoid editing shared files while paused.
- Pausing does not stop online-only files downloading when you open them.
- OneDrive auto-resumes after the chosen time; don't forget a 24-hour pause before travel.

## Verify
- [ ] Icon shows paused; after resuming, it returns to *Up to date* with no conflict copies.
