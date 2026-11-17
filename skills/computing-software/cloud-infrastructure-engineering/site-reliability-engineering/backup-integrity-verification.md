---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.backup-integrity-verification
name: backup-integrity-verification
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, data-integrity, backup-checksum-verification, restore-testing, data-validation]
level: advanced
status: docs-checked
description: "Verify backups are complete and restorable: tool-level integrity checks, automated end-to-end restore tests with a heartbeat alert, content validation and stale-backup alerting."
sources: ["https://sre.google/sre-book/data-integrity/", "https://restic.readthedocs.io/en/stable/045_working_with_repos.html#checking-integrity-and-consistency", "https://www.postgresql.org/docs/current/app-pgverifybackup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup integrity verification

**Goal:** know, not hope, that backups can restore correct data. SRE Book: "No one really wants to make backups; what people really want are restores."

## Why test (SRE Book, "Knowing That Data Recovery Will Work")
Recovery dependencies, mostly the backup, may be in a latent broken state you only find when you try to
recover. To detect that: continuously test the recovery process as part of normal operations, and alert when
the recovery process fails to provide a heartbeat indication of success. The book says the only test that
should let you sleep at night is a full end-to-end test, that manual staged tests are not performed deeply or
often enough, and that you should automate them and run them continuously.

## What a recovery test should confirm (from the book)
- Backups are valid and complete, not empty.
- You have enough machine resources for setup, restore and post-processing.
- The recovery completes in reasonable wall time.
- You can monitor recovery progress.
- You are free of critical dependencies outside your control (for example an offsite media vault not available 24/7).

## Layers of verification
| Layer | Check | Example |
|---|---|---|
| Existence and freshness | A backup for every dataset within your recovery-point objective | Alert if the newest backup is older than the objective |
| Format integrity | The backup is readable by its tool | `restic check` verifies repository structure; `--read-data` also verifies pack files and `--read-data-subset` checks part of them (the restic docs warn `--read-data` downloads all pack files, costing time and bandwidth); PostgreSQL provides `pg_verifybackup` for base backups |
| Restore | Actually restore to a scratch environment | Automated, continuous restore job with a success heartbeat |
| Content validation | Restored data is correct | Compare counts or checksums with values recorded at backup time, plus an application smoke test |

## Practices
- Out-of-band data validation (SRE Book) catches corruption that is faithfully backed up: compare invariants continuously.
- Measure restore time, not just success, and compare it with your objective.
- Rotate which dataset gets a full restore test so every dataset is tested regularly; choose the interval from
  your own risk, as the book gives no figure.

## Verify
- [ ] Dashboard shows last successful restore test per dataset and restore duration; alerts fire on missing backups or a missing heartbeat.

## Checked
2026-11-01. Confirmed against the SRE Book "Data Integrity" chapter (latent broken backups, continuous
automated end-to-end tests, heartbeat alert, what to confirm) and the restic documentation (`check`,
`--read-data`, `--read-data-subset`, bandwidth caveat). `pg_verifybackup` is named by the PostgreSQL page cited
in sources; check its page for options. Removed: the shell restore script (AWS CLI, pg_restore, Pushgateway),
`mysqlbackup validate`, `xtrabackup --prepare`, the 5% subset example and the quarterly interval.
Method: documentation only; no commands were run.
