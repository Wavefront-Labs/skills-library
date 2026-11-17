---
id: computing-software.database-administration.database-backup-recovery.restore-drills-and-disaster-recovery-runbooks
name: restore-drills-and-disaster-recovery-runbooks
category: computing-software
field: database-administration
product: database-backup-recovery
tags: [database-administration, disaster-recovery, restore-drill, runbook, game-day, chaos-engineering, backup-verification, tabletop-exercise, recovery-testing, bus-factor]
level: advanced
status: draft
description: "Run scheduled restore drills that actually prove a backup works, and write a DR runbook specific enough that someone other than its author can execute it under pressure."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restore drills and disaster-recovery runbooks that survive contact with reality

**Goal:** make "we have backups" into a tested, timed, documented fact — not a
belief that collapses the first time someone other than the person who set it up
has to use it during an actual incident.

## 1. A backup that was never restored is a hope
Backup jobs can report "success" while producing a file that doesn't restore —
corrupted mid-write, missing a required extension/plugin, taken against a replica
that was itself already broken, or simply too old because a silent failure a week
ago never retried. The only thing that proves a backup works is actually restoring
it and verifying the data. Schedule this — monthly for critical systems at
minimum, more often for anything with a tight RPO/RTO — not "whenever someone
remembers."

## 2. What a drill actually needs to prove
- **Restorability**: the backup restores without manual intervention beyond the
  documented steps.
- **Completeness**: row counts, checksums, or application-level smoke tests
  confirm the restored data matches expectations — a restore that "completes" but
  is missing a table or has truncated data due to a bad flag is a false pass if
  you only check the exit code.
- **Timing against RTO**: time the whole thing, including the parts people forget
  to budget — locating the right backup, provisioning a target, DNS/connection
  string cutover, cache warmup. A restore that technically finishes in 20 minutes
  but needs 2 hours of manual DNS changes afterward has a 2-hour RTO, not 20
  minutes.
- **Point-in-time accuracy**: if the RPO depends on log replay (WAL/binlog/redo),
  confirm the drill actually replays to a specific target timestamp, not just
  "restores the last full backup."

## 3. Runbooks: write for the person who isn't you, at 3am
A runbook that says "restore the database from backup" is not a runbook — it's a
reminder that one exists. A usable one has:
- Exact commands/console steps with no implied prior knowledge (full paths,
  exact flag names, which credentials/vault entry to use).
- Named decision points ("if lag > X, do Y instead of Z") rather than requiring
  judgment calls under stress that the author made easily because they'd done it
  ten times.
- The **current** topology — a runbook describing last year's architecture after
  a migration is actively dangerous, more so than no runbook, because it's
  trusted. Tie runbook review to any infrastructure change, not a fixed calendar
  alone.
- Rollback/abort criteria: what does "this isn't working, stop and escalate"
  look like, and to whom.

## 4. Bus-factor: the drill tests the runbook, not the expert
Run the drill with someone who did **not** write the backup/restore tooling,
following only the runbook, with the author silent unless asked. Every point
where they get stuck or guess is a runbook gap, found in a drill instead of a
real incident. If only one person can execute recovery, that person leaving or
being unreachable during an incident is itself the next disaster waiting to
happen — treat it as a finding, not a staffing inconvenience to route around
later.

## 5. Game days / tabletop exercises for scenarios too costly to drill live
Full production failover can't always be rehearsed live (cost, risk). A tabletop
walkthrough — stepping through the runbook verbally/on a whiteboard against a
specific injected scenario ("primary region is gone, RPO clock started 90 seconds
ago, go") — still surfaces missing steps, unclear ownership, and wrong assumptions
without the blast radius of a live drill, and is better than skipping verification
entirely for systems too critical to practice failover on live traffic.

## Verify
- [ ] A restore drill for each critical system ran within the last quarter and is scheduled to recur.
- [ ] The drill checked data completeness (checksums/row counts/smoke tests), not just restore completion status.
- [ ] Total time including cutover steps was measured against the documented RTO.
- [ ] The runbook was executed by someone other than its author, and gaps found were fixed, not just noted.
- [ ] The runbook's topology/commands were reviewed after the most recent infrastructure change.
