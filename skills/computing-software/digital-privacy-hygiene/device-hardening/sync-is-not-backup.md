---
id: computing-software.digital-privacy-hygiene.device-hardening.sync-is-not-backup
name: sync-is-not-backup
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, sync-vs-backup, backups, version-history, ransomware]
level: practitioner
status: draft
description: "Explain why Dropbox, OneDrive, iCloud and Google Drive sync spreads deletions and ransomware, use their version history, and add a real backup."
sources:
  - "https://help.dropbox.com/delete-restore/version-history-overview"
  - "https://support.microsoft.com/onedrive"
  - "https://www.cisa.gov/stopransomware"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Sync is not backup

**Goal:** understand what a sync service protects against, and close the gap.

## What sync does
It makes every device match. Delete, overwrite or encrypt a file on one device, and within seconds that change is on
all devices and in the cloud. Good against a lost laptop; bad against mistakes, ransomware, or a hijacked account.

## Built-in safety nets
| Service | Deleted files | Version history |
|---|---|---|
| Dropbox | Restore deleted files for 30 days (longer on higher plans) | Per-file versions, same window; Rewind whole folders on paid plans |
| OneDrive | Recycle bin about 30 days | Version history; **Restore your OneDrive** to a past date with Microsoft 365 |
| Google Drive | Trash 30 days | Versions for non-Google files kept 30 days or 100 versions |
| iCloud Drive | Recently Deleted 30 days | Data recovery at icloud.com (restore files) |

Know your windows; ransomware noticed after 31 days is not covered.

## Add a real backup (3-2-1)
- Three copies, two different media, one off-site, with **versioning** and at least one copy that the synced
  computer cannot overwrite (offline disk, immutable/append-only cloud backup).
- Tools: Time Machine, Windows File History, restic/Borg to a separate cloud bucket, a NAS with snapshots.
- Back up the sync folder like any other folder.

## Gotchas
- Selective sync and "files on demand" mean the files may not exist locally to back up; force local copies for
  critical folders or back up from the cloud side.
- A compromised account can delete version history too; protect the account with strong 2FA.
