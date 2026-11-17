---
id: computing-software.digital-privacy-hygiene.device-hardening.restic-encrypted-backups
name: restic-encrypted-backups
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, restic, backups, encrypted-backups, backblaze-b2, s3, sftp, retention-policy]
level: advanced
status: docs-checked
description: "Back up with restic to local disks, SFTP, S3 or B2: init an encrypted repo, schedule backups, set forget/prune retention, check integrity and restore."
sources:
  - "https://restic.readthedocs.io/en/stable/"
  - "https://restic.readthedocs.io/en/stable/060_forget.html"
  - "https://github.com/restic/restic"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restic encrypted backups

**Goal:** fast, deduplicated, end-to-end encrypted backups to storage you do not have to trust.

## Initialise a repository
```bash
export RESTIC_REPOSITORY=b2:my-bucket:laptop      # or /mnt/usb/restic, sftp:user@host:/srv/restic, s3:s3.us-east-1.amazonaws.com/bucket
export RESTIC_PASSWORD_FILE=~/.config/restic/pass  # chmod 600
export B2_ACCOUNT_ID=... B2_ACCOUNT_KEY=...        # backend credentials
restic init
```
Data is encrypted client-side (AES-256 in counter mode, authenticated with Poly1305-AES). **Lose the password and the backup is gone**: store
it in your password manager and the emergency kit.

## Back up
```bash
restic backup ~/Documents ~/Pictures --exclude-file ~/.config/restic/excludes --exclude-caches
restic snapshots
```
Exclude caches, `node_modules`, VM images and cloud-sync placeholders.

## Retention
```bash
restic forget --keep-daily 7 --keep-weekly 5 --keep-monthly 12 --keep-yearly 3 --prune
```
`forget` alone only removes snapshot references; `--prune` frees the space.

## Verify and restore
```bash
restic check                              # structure
restic check --read-data-subset=5%        # also read actual data
restic restore latest --target /tmp/restore --include <HOME>/Documents/taxes
restic mount /mnt/restic                  # browse snapshots (Linux/macOS with FUSE)
```

## Schedule
- Run backups from your OS scheduler (systemd timer, cron, Task Scheduler) with the repository and
  password environment set, and alert on failure so silent breakage is noticed.

## Gotchas
- Use a separate repository per machine or understand shared-repo locking.
- For ransomware resistance, use an append-only repository so a compromised laptop cannot delete
  snapshots; read restic's append-only security considerations first, as policy-based removal changes the picture.

## Checked
2026-11-01. Confirmed against the restic stable docs (preparing a repo, backup, working with repos, references): environment variables, `--password-file`, S3 repository form, AES-256 CTR with Poly1305-AES, `--read-data-subset`, `restic mount`, append-only mode. Removed: Windows/Backrest/healthchecks advice, `restic unlock`, `restic prune`, rest-server flag.
Method: documentation only; no commands were run.

## Verify
- [ ] Snapshots appear daily; `check --read-data-subset` passes; a test restore matches.
