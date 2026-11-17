---
id: computing-software.general-digital-literacy.file-management.backup-schedules-and-versioning
name: backup-schedules-and-versioning
category: computing-software
field: general-digital-literacy
product: file-management
tags: [file-management, file-backup, backup-schedule, file-history, time-machine]
level: intro
status: docs-checked
description: "How Time Machine schedules backups and local snapshots, how Google Drive keeps and pins file versions, and how to pick a schedule that matches how much work you can lose."
sources:
  - https://support.apple.com/en-au/guide/mac-help/mh35860/mac
  - https://support.google.com/drive/answer/2409045
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backup schedules and versioning

## Mac Time Machine
- With Time Machine on, the Mac backs up automatically and keeps hourly, daily and weekly backups of your files.
- It also saves local snapshots hourly on the same disk, kept for up to 24 hours or until space is needed. Local snapshots are only created on APFS disks.
- Setup and restore steps: see the Mac User Guide page on Time Machine.

## Google Drive file versions
- Drive: select the file > More > File information > **Manage versions**.
- A version might be permanently deleted after 30 days or when 100 newer versions exist. **Keep forever** on a version stops that.
- Docs, Sheets and Slides use a separate version history from other files.

## Picking a schedule
- Decide how much work you can afford to lose, and keep versions long enough to notice a problem.

## Verify
- [ ] Restore an earlier version of a test file and confirm it opens.

## Checked
2026-11-01. Confirmed: Apple Mac User Guide "Back up your Mac with Time Machine" (hourly/daily/weekly, local snapshots, 24 hours, APFS); Google Drive Help "Check activity & file versions" (Manage versions, 30 days / 100 versions, Keep forever). Removed: File History intervals, OneDrive and Dropbox retention figures, Time Machine menu paths and retention schedule (no page read).
Method: documentation only; no commands were run.
