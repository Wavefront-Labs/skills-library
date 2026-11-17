---
id: computing-software.digital-privacy-hygiene.device-hardening.testing-backup-restores
name: testing-backup-restores
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, backup-restore-test, backups, disaster-recovery, sha256, restic, time-machine]
level: practitioner
status: draft
description: "Run regular restore drills: restore sample and full data to a spare location, compare hashes, and confirm the keys and passwords needed to decrypt backups are reachable."
sources:
  - "https://www.cisa.gov/stopransomware/ransomware-guide"
  - "https://restic.readthedocs.io/en/stable/045_working_with_repos.html"
  - "https://support.apple.com/guide/mac-help/welcome/mac"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing backup restores

**Goal:** a backup is only proven when you have restored from it. Find the broken job, the forgotten password
or the excluded folder before the disaster does.

## Quarterly sample restore (30 minutes)
1. Pick 5-10 random files of different types (photo, document, spreadsheet, a file changed this week).
2. Restore them to a **different location**, never over the originals.
3. Compare:
   ```powershell
   Get-FileHash .\original.jpg, .\restored\original.jpg -Algorithm SHA256
   ```
   ```bash
   sha256sum original.jpg restored/original.jpg
   ```
4. Open each file. Check the newest file is actually there (stale backups are the most common failure).

## Tool-specific integrity checks
- restic: `restic check --read-data-subset=10%` (reads and verifies a sample of pack data).
- Time Machine: `tmutil verifychecksums /Volumes/<backup>/...`; or browse with Enter Time Machine and restore a folder.
- Cloud photo/drive services: download a whole album or folder via the web, not just the app cache.
- Phone backups: restore onto a spare or reset device once a year, or at least confirm the backup date and size.

## Yearly full drill
- Restore a whole machine (or a VM) from backup to estimate how long it really takes.
- Do it from a device that does **not** already hold your password manager session: can you get the backup
  password, cloud login and 2FA from the emergency kit alone?

## Record
Keep a short log: date, what was restored, result, time taken. Fix failures the same week.

## Common findings
- Backup job stopped months ago after a password change or drive letter change.
- New folders (a second drive, a new photo app) never added to the backup set.
- Encryption key/password stored only inside the backup it protects.

## Verify
- [ ] Last sample restore within 3 months, hashes matched, newest file present.
- [ ] Decryption credentials available outside the backup.
