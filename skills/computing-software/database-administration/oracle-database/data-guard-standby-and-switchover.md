---
id: computing-software.database-administration.oracle-database.data-guard-standby-and-switchover
name: data-guard-standby-and-switchover
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle, data-guard, physical-standby, switchover, failover, redo-apply, dgmgrl, protection-mode, broker, fast-start-failover, rpo]
level: advanced
status: docs-checked
description: "Build an Oracle Data Guard physical standby, manage redo-apply lag, and run a clean planned switchover versus a lossy failover."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Oracle Data Guard — standby setup, lag, and switchover vs. failover

**Goal:** keep a physical standby genuinely ready to take over, know the real
difference between a switchover (planned, zero data loss) and a failover
(unplanned, possibly lossy), and manage it through the broker instead of raw SQL*Plus.

## 1. Protection modes set your RPO before any incident happens
- **Maximum Protection**: synchronous redo transport (`SYNC`), zero data loss, but
  the **primary stalls** if it cannot confirm the standby received the redo — a
  single-standby config with no second protected destination means a standby
  outage halts the primary. Needs at least two synchronized standbys for
  availability in practice.
- **Maximum Availability**: synchronous when possible, but degrades to
  asynchronous automatically if the standby is unreachable rather than stalling
  the primary — the common choice for "want zero loss, can't afford to stall".
- **Maximum Performance**: asynchronous (`ASYNC`) always; primary never waits.
  Normal choice for a WAN/DR standby. Data loss window = however much redo hadn't
  shipped.
Set and confirm with `dgmgrl`, not just `log_archive_dest_n` strings — the broker
keeps modes consistent across role changes, which hand-managed configs tend to
drift on.

## 2. Use the broker (dgmgrl), not manual SQL*Plus role transitions
```
dgmgrl sys/password@primary
DGMGRL> show configuration;
DGMGRL> show database verbose standby1;
DGMGRL> validate database standby1;
```
`validate database` before any transition — it reports whether the
standby is ready for the role change.

## 3. Switchover (planned, no data loss)
```
DGMGRL> switchover to standby1;
```
Requires the primary to be healthy and reachable — it waits for all redo to be
shipped and applied, then cleanly flips roles. The old primary becomes a standby
automatically; no resync needed afterward. If `switchover` fails partway (e.g.
network blip mid-transition), the configuration can be left in an ambiguous
state — `show configuration` and resolve before retrying, don't just re-run blindly.

## 4. Failover (unplanned, potentially lossy)
```
DGMGRL> failover to standby1;
```
Used when the primary is actually gone. Any redo not yet received by the chosen
standby is lost — in Maximum Performance mode this can be seconds to minutes of
transactions. After failover, the old primary (once it comes back) **cannot
simply rejoin as a standby** — it has transactions the new primary never saw.
Either flash it back (if Flashback Database was enabled and the flashback window
covers the failover point — `FLASHBACK DATABASE ... TO SCN <failover_scn>`) to
reinstate it as a standby, or rebuild it from scratch. Enabling Flashback Database
on every standby/primary ahead of time is what makes reinstatement fast instead of
a full re-clone.

## 5. Fast-Start Failover (FSFO)
Automates failover decision-making via an Observer process that monitors both
primary and standby and triggers failover without a human, within a configured
failover threshold. Gets the RPO/RTO benefit of automatic failover but
means a network partition between primary and observer (not an actual primary
failure) can trigger an unwanted failover — place the observer carefully (ideally
a third site) and test partition scenarios, not just primary-down scenarios.

## 6. Apply lag monitoring
```sql
SELECT name, value FROM v$dataguard_stats WHERE name IN ('apply lag','transport lag');
```
Apply lag growing while transport lag stays flat means the standby's apply (redo
apply via MRP) is falling behind — often undersized standby hardware relative to
primary write rate, or a nologging operation on the primary that the standby can't
apply from redo alone (requires a re-sync of that object).

## Verify
- [ ] Protection mode matches the intended RPO and was confirmed via `dgmgrl`, not just init parameters.
- [ ] `validate database` passes clean before any planned switchover.
- [ ] Flashback Database is enabled on standbys so a failed-over former primary can reinstate without a full rebuild.
- [ ] If FSFO is used, the observer's placement was tested against a network-partition scenario, not just primary-down.
- [ ] Apply lag and transport lag are both monitored, not just "standby is in sync" at a glance.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: protection modes Maximum Protection / Maximum Availability / Maximum Performance, switchover and failover through the broker, reinstating the former primary, the Observer for fast-start failover (Data Guard Broker and Concepts guides).

Removed or corrected: the FastStartFailoverThreshold property name and the list of what VALIDATE DATABASE checks (not found in the cited pages).

Method: documentation only; no commands were run.
