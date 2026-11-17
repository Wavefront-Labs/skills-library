---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.data-integrity-backups-and-restore-testing
name: data-integrity-backups-and-restore-testing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, data-integrity, backups, backup-restore-testing, restore-drill, soft-deletion, trash, lazy-deletion, defense-in-depth, out-of-band-validation, rpo, rto]
level: advanced
status: docs-checked
description: "Guarantee data can be recovered, not just backed up: the SRE Book's failure modes, three layers of defense in depth (soft deletion, backups, early detection) and restore drills."
sources: ["https://sre.google/sre-book/data-integrity/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data integrity, backups and restore testing

**Goal:** "the data is still there" survives human error, software bugs, hardware failure and malice,
proven by restoring, not by a green backup job.

## 1. The SRE Book's frame
- The point of backups is recovery: nobody wants backups, people want restores. Recovery
  factors should drive backup decisions, not the other way round.
- Failure modes are classified by root cause, scope and rate, and the restore plan must cope with
  any combination (the chapter counts 24). A strategy that guards against a creeping application
  bug may do nothing when a datacenter burns.
- Rate matters: a "big bang" loss (a million rows replaced by ten in one minute) is noticed fast; a
  creeping loss (ten rows deleted every minute for weeks) can take days to be noticed, needs
  snapshots from further back, and the restored data must be merged with current state.

## 2. Defense in depth (three layers)
1. **Soft deletion**: deleted data stays recoverable for a period (the chapter's example is a
   trash bin holding items deleted fewer than 30 days ago). It is the primary defense against
   developer error and secondary against user error, and also covers account hijackers who delete
   a user's data. For developer-facing offerings, **lazy deletion** is the primary defense against
   internal developer error.
2. **Backups and recovery**: the second line of defense. Decide how often you take restore
   points (full or incremental) with recovery speed in mind: restoring a long chain of
   interdependent incrementals (the chapter's example is over 1,000 after a three-year-old full)
   adds risk of failure at every link.
3. **Early detection**: out-of-band checks and balances within and between datastores, so
   degrading data is found before users see it. Shorter detection time shrinks the recovery window.

## 3. Practice
- Write the data-loss tolerance (RPO) and time-to-recover (RTO) per data store and let those
  numbers pick the backup mechanism.
- Run restore drills on a schedule you choose: restore into an isolated environment, check
  integrity and run a smoke test, record achieved recovery time and data loss, then tear it down.
- Rehearse narrow restores too (one tenant, one object, one table), not only full restores.
- Keep backups outside the failure domain of production, and alert on the absence of a successful
  backup, not only on failures.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Data Integrity: What You Read Is What You Wrote"
(sre.google/sre-book/data-integrity/): restore focus, failure-mode dimensions and the 24 combinations, big-bang
versus creeping loss, the three layers, soft and lazy deletion roles, 30-day trash example, over-1,000-backup chain example,
out-of-band checks. Removed as unconfirmed: all pgBackRest, Velero, restic and PostgreSQL commands, retention
baselines, restore throughput arithmetic, the backup-type comparison table, 3-2-1 and Object Lock detail, monitoring metric
names and drill cadence figures. Practice section is judgement, not sourced figures.
Method: documentation only; no commands were run.
