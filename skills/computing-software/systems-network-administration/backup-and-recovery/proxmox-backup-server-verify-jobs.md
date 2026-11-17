---
id: computing-software.systems-network-administration.backup-and-recovery.proxmox-backup-server-verify-jobs
name: proxmox-backup-server-verify-jobs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [pbs-verify, proxmox-backup-server, verify-job, chunk-integrity, backup-verification, proxmox-backup]
level: practitioner
status: docs-checked
description: "Verify Proxmox Backup Server snapshots with scheduled verify jobs and verify-new, re-verification intervals, handling of corrupt chunks, and reading verification state."
sources:
  - https://pbs.proxmox.com/docs/maintenance.html
  - https://pbs.proxmox.com/docs/proxmox-backup-manager/synopsis.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PBS verify jobs

**Goal:** detect bit rot or damaged chunks in deduplicated backups, where one bad chunk can affect many snapshots.

## Why verify
Physical drives degrade over time (bit rot), so an old backup that verified once can later be corrupt. The PBS manual recommends re-verifying all backups at least monthly. A good pattern is an hourly or daily job that checks new and expired backups, plus a weekly or monthly job that reverifies everything, so restores hold no surprises.

## Verify jobs
```bash
proxmox-backup-manager verify-job create weekly-verify --store store1 --schedule 'sat 03:00' \
  --ignore-verified true --outdated-after 30
proxmox-backup-manager verify-job list
```
- `--ignore-verified` (default true): do not re-verify snapshots that are already verified and not outdated.
- `--outdated-after N`: days after which a verification counts as outdated (0 is deprecated).
- The schedule uses calendar event syntax; verify jobs are created in the datastore's Verify Jobs tab or with the CLI above.
- Read and verify threads can be set with `--read-threads` and `--verify-threads` (1 to 32; defaults 1 and 4).
- A manual run over a datastore: `proxmox-backup-manager verify <datastore> --ignore-verified false`, or Verify All in the datastore's Content tab.

## Verify new backups
Datastore option `verify-new` (`proxmox-backup-manager datastore update <datastore> --verify-new true`): all new backups are verified right after completion. This adds read load at backup time.

## Gotchas
- Verification reads backup data: schedule it outside backup windows and size disks for the I/O.
- Failed verifies on many snapshots usually point to a storage problem; check the disks and, on ZFS, scrub results.
- PBS can send notifications about scheduled verification, garbage collection and sync results.

## Verify
The datastore Content view shows recent verification on snapshots within the outdated-after window, and verify task logs show no errors.

## Checked
2026-10-28. Confirmed against the PBS Maintenance page (Verification section) and the proxmox-backup-manager synopsis (`verify-job create`, `--ignore-verified` default true, `--outdated-after` in days, `--verify-new`, `--read-threads` and `--verify-threads`). Removed because the pages do not state them: the SHA-256 comparison detail, the `.bad` chunk renaming, how clients heal after a failed verify, and the claim that verify-new doubles read I/O. See the PBS docs for the corrupt-chunk handling procedure before relying on it.
Method: documentation only; no commands were run.
