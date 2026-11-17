---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.restore-drills-and-restore-slos
name: restore-drills-and-restore-slos
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [restore-drill-schedule, restore-slo, data-integrity, backup-testing, pitr, disaster-recovery]
level: practitioner
status: docs-checked
description: "Prove backups by restoring them: restore SLOs per failure mode, practised restores that demonstrate meeting them, point-in-time recovery, and correctness checks."
sources: ["https://sre.google/sre-book/data-integrity/", "https://www.postgresql.org/docs/current/continuous-archiving.html", "https://pgbackrest.org/user-guide.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Restore drills and restore SLOs

SRE Book (Data Integrity): "No one really wants to make backups; what people really want are restores."
Deliver a recovery system, not a backup system. Do not make teams "practice" backups; instead:
- teams define SLOs for data availability in a variety of failure modes, and
- a team practises and demonstrates its ability to meet those SLOs.

## Writing restore SLOs
When formulating a backup strategy, decide how quickly you need to recover from a problem and how much
recent data you can afford to lose. Write one target for each of the two per dataset and failure mode, and
record the measured result of each restore against them. The book notes that a plan must cover user action,
operator error, application bugs, infrastructure defects, faulty hardware and site catastrophes in any
combination; a strategy that guards against a creeping application bug may not help when a datacenter burns.

## What a restore drill covers
1. Restore from a real backup (not an archive) into an isolated environment.
2. Check the recovered data is correct, not merely present: the book warns that mixing transactional and
   non-transactional backup and restore solutions means recovered data is not necessarily correct.
3. Time the restore: restoring probably takes as long as backing up, so loading can take hours.
4. Exercise point-in-time recovery ("time-travel" inside Google) where the service needs each affected
   artifact recovered to its own point in time. The book's study of 19 recovery efforts found the hardest
   cases were low-grade corruption or deletion discovered weeks to months later.

PostgreSQL point-in-time recovery from continuous archiving is documented on the Postgres page above. The
pgBackRest user guide shows a time-targeted restore of this shape (placeholders):
```bash
pgbackrest --stanza=<STANZA> --delta --type=time "--target=<TIMESTAMP>" --target-action=promote restore
```
Then run your own application-level checks on the restored instance.

## Gotchas
- Do not rely on an infrequently used recovery scheme whose only tests are your own rare restore attempts;
  prefer schemes in common, continual use (SRE Book).
- Restore time grows with data size; compare each measured restore to the objective you wrote.
- Restores that need the primary's credentials or keys may fail in a real disaster; drill with the recovery
  credentials (a design choice, not stated by the book).

## Verify
- [ ] Each dataset has written recovery-time and data-loss objectives per failure mode.
- [ ] A recorded restore, with content checks, demonstrates meeting them.

## Checked
2026-11-01. Confirmed against the SRE Book Data Integrity chapter (restore quote, recovery system, SLOs for
data availability, mixed backup solutions, 19-recovery study, point-in-time recovery, restore time) and the
pgBackRest user guide (`--delta`, `--type=time`, `--target`, `--target-action=promote`, `restore`). Removed:
the example RTO/RPO figures, 14 and 28 day numbers, the drill cadence table, the alert rule and metric
names, and the 2 TB example, which no page states.
Method: documentation only; no commands were run.
