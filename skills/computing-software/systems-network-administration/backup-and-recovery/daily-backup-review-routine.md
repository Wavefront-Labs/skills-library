---
id: computing-software.systems-network-administration.backup-and-recovery.daily-backup-review-routine
name: daily-backup-review-routine
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [daily-backup-check, backup-monitoring, operations-routine, backup-report, checklist]
level: practitioner
status: draft
description: "Run a 15-minute daily backup check: failed and warning jobs, missed RPO, unprotected new systems, capacity, immutability and copy status, logged with tickets."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://helpcenter.veeam.com/docs/one/reporter/about.html
  - https://www.cisecurity.org/controls/data-recovery
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Daily backup review routine

**Goal:** no backup failure survives more than one business day unnoticed. Owner: named person per day (rota), with a backup.

## Checklist (same order every day)
1. **Failures**: list jobs/objects failed in the last 24 hours. For each: retry or ticket; note cause.
2. **Warnings**: read them. "Guest processing failed" on a database means the DB backup is crash-consistent only; treat as failure.
3. **RPO misses**: systems with no good restore point inside their tier RPO (report, not job status). Catches disabled jobs and VMs that silently left a job.
4. **New unprotected systems**: inventory vs protected list (Veeam ONE Unprotected VMs, cloud resource without backup policy).
5. **Copies**: off-site / immutable copy jobs current; tape out-of-library status.
6. **Capacity**: repositories over 80%, days-left figure.
7. **Security signals**: unexpected deletions, retention changes, malware detection events, failed logins to backup consoles.
8. **Long-running or stuck**: jobs still running from last night; stale snapshots on VMs.

## Record
One line per day in the ops log or ticket: "Backups checked, 2 failures (INC123, INC124), RPO OK, capacity OK." Auditors (ISO 27001 A.8.13, SOC 2) ask for this evidence.

## Escalation
- Same object failing 2 days running: escalate to the backup lead.
- Any RPO miss on Gold tier: notify the service owner the same day.

## Gotchas
- Email reports land in folders nobody reads; use a dashboard or ticket automation instead.
- Weekend failures: Monday's check must cover 72 hours.

## Verify
Monthly, sample five daily entries and trace their tickets to closure.
