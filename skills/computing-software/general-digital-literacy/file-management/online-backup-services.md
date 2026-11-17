---
id: computing-software.general-digital-literacy.file-management.online-backup-services
name: online-backup-services
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, cloud-backup-service, backblaze, offsite-backup]
level: intro
status: draft
description: "Choose and set up an online backup service (Backblaze, iDrive, Carbonite, Acronis) for offsite protection, and understand how it differs from cloud sync like OneDrive."
sources:
  - https://www.backblaze.com/cloud-backup
  - https://www.cisa.gov/stopransomware
  - https://www.ncsc.gov.uk/collection/top-tips-for-staying-secure-online
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Online backup services

## Backup vs sync
- **Sync** (OneDrive, Google Drive, Dropbox, iCloud): one copy mirrored everywhere. Deletion or ransomware encryption syncs too (with limited version history/recycle bin).
- **Backup**: separate, versioned copies kept for a set period, independent of your working files. The 3-2-1 rule: 3 copies, 2 media, 1 offsite. An online backup is the offsite copy.

## Choosing a service
- **Backblaze Personal**: unlimited data for one computer, continuous; keeps versions 30 days (1 year or forever as paid options). Restore by download or a shipped drive.
- **iDrive**: several devices on one plan including phones and external drives; snapshot history.
- **Carbonite, Acronis Cyber Protect Home Office**: similar; Acronis adds full-image and anti-ransomware.
- Compare: device limits, external drive support, version retention, restore options, private encryption key option, and price per year.

## Setup
1. Install, sign in, let it scan. Initial upload of hundreds of GB can take days; leave the computer on and plugged in.
2. Check the **exclusions** (some skip system folders, video, or external drives by default) and add folders that matter.
3. Optional **private encryption key**: the provider cannot read your files, but losing the key means losing the backup.
4. Turn on email alerts if a computer hasn't backed up for days.

## Gotchas
- External drives must be connected at least every 30 days or Backblaze deletes their backup.
- Metered/slow connections: set bandwidth throttling.
- Test a restore of a few files soon after setup.

## Verify
- [ ] Dashboard shows "backed up" with today's date and a test file restored correctly.
