---
id: computing-software.systems-network-administration.backup-and-recovery.file-level-restore-sampling
name: file-level-restore-sampling
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [file-level-restore, restore-testing, restore-sampling, backup-verification, automation, recovery-testing]
level: practitioner
status: draft
description: "Prove backups are restorable with routine file-level restore sampling: random selection across systems, automated restore to a sandbox, hash comparison and trend reporting."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File-level restore sampling

**Goal:** frequent, cheap evidence that backups contain readable, correct data, not just successful job statuses.

## Design
- **Frequency**: weekly sample, e.g. 10-20 files across different systems and repositories.
- **Selection**: random systems weighted by tier, random restore point within retention (not just last night), random files that have not changed since that point.
- **Target**: restore to a sandbox location, never over production.

## Automate the check
1. Pick a file from the backup catalog or a file list exported at backup time.
2. Restore it:
   - restic: `restic -r <repo> restore <snapshot> --target /sandbox --include /srv/data/report.xlsx`
   - Veeam: file-level restore via PowerShell (`Start-VBRWindowsFileRestore` then copy) or Veeam Explorer.
   - Bacula: `bconsole` `restore` with `file=` selection.
3. Compare: if the production file's modification time predates the restore point, compare SHA-256; otherwise check the file opens/parses (`file`, `unzip -t`, application validator).
4. Log result: system, restore point age, file, size, hash match, duration.

```bash
sha256sum /sandbox/srv/data/report.xlsx /srv/data/report.xlsx
```

## Report
Monthly: success rate, failures with root cause (missing file = backup scope gap; hash mismatch = corruption), restore time. Any failure opens an incident.

## Gotchas
- Sampling only last night's backups misses chain corruption in older points.
- Exclusions (e.g. open files, filters) show up first in sampling; check them against the backup scope definition.

## Verify
The sampling log shows the expected number of tests each week with 100% success or tracked incidents.
