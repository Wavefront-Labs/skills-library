---
id: computing-software.database-administration.sql-server.always-on-availability-groups
name: always-on-availability-groups
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, always-on, availability-group, wsfc, windows-cluster, synchronous-commit, automatic-failover, listener, quorum, split-brain, readable-secondary]
level: advanced
status: docs-checked
description: "Design SQL Server Always On availability groups with the right sync mode and quorum, and diagnose failover, listener, and data-loss incidents."
sources:
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/overview-of-always-on-availability-groups-sql-server
  - https://learn.microsoft.com/en-us/sql/sql-server/failover-clusters/windows/wsfc-quorum-modes-and-voting-configuration-sql-server
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/active-secondaries-readable-secondary-replicas-always-on-availability-groups
  - https://learn.microsoft.com/en-us/sql/database-engine/availability-groups/windows/perform-a-forced-manual-failover-of-an-availability-group-sql-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL Server Always On availability groups — sync modes, quorum, and failover

**Goal:** know which availability mode to use where, why automatic failover
sometimes doesn't happen when you expect it, and how to avoid the specific way
these clusters lose data.

## 1. Sync commit vs. async commit
- **Synchronous commit**: primary waits for the secondary to harden the log
  (write to disk, not apply) before committing. Zero data loss on failover, at the
  cost of commit latency equal to the round-trip to the secondary. Use within a
  datacenter/low-latency link, and only for secondaries that participate in
  automatic failover.
- **Asynchronous commit**: primary commits without waiting. Used for DR replicas
  across regions where latency would be unacceptable. These secondaries can never
  be automatic-failover targets — only manual, forced failover, which **can lose
  the most recent transactions** (whatever hadn't shipped yet).
Mixing both in one AG (sync local secondary for HA, async remote for DR) is the
standard pattern — know which one each secondary is before assuming failover is
lossless.

## 2. Quorum and the thing that causes split-brain-like symptoms
AGs ride on Windows Server Failover Clustering (WSFC) quorum, not their own vote.
Losing quorum (e.g. a majority of cluster nodes/file-share-witness unreachable)
takes the **whole cluster offline**, not just one AG — all databases in all AGs on
that cluster become unavailable even if the actual SQL instances are healthy. This
surprises people who think AGs are per-database independent. Microsoft recommends an odd number of quorum votes: use a witness
(see the WSFC quorum article for witness types) with an even number of voting nodes, and size
voting membership deliberately (generally no vote for nodes at a DR site) — adding a DR-site replica as a full voting member
can let a WAN partition cost you quorum at the primary site.

## 3. Forced (manual) failover and data loss
When quorum is intact but you need to fail over to an async secondary anyway
(primary site genuinely down), `ALTER AVAILABILITY GROUP ... FORCE_FAILOVER_ALLOW_DATA_LOSS`
is the only path — explicit in the syntax because it is exactly that. Any
transaction committed on the old primary after the last log block shipped is gone.
Before forcing, if there's any way to reach the old primary's log, exhaust that
first; after forcing, every secondary database (including the old primary's, once it returns as a secondary) is SUSPENDED and must be resumed manually. Resuming rolls back log records never committed on the new primary, so create a database snapshot on a suspended database first if you may need to recover that data.

## 4. The listener and client redirection
The AG listener is a separate virtual network name/IP tied to a cluster resource;
clients connect to the listener (not an instance name) so failover is transparent.
Confirm `MultiSubnetFailover=True` in connection strings for multi-subnet AGs
(different IP per subnet for the listener) — without it, the driver does not try all listener IPs in parallel, so reconnecting after a cross-subnet failover is slower.

## 5. Readable secondaries and their gotchas
Secondaries can serve read-only workloads (`ApplicationIntent=ReadOnly` routing)
but run on redo delay — read queries on a secondary are mapped to snapshot isolation (locking hints are ignored),
so readers do not normally block redo. Costs: 14 bytes of row-version overhead per modified row
on disk-based tables (carried over from the primary, so page splits are possible), extra tempdb space
for row versions, and queries can be temporarily blocked until transactions that were open on the
primary when read access was enabled have finished.

## Verify
- [ ] Each secondary's commit mode (sync/async) matches its actual role (HA vs. DR).
- [ ] The witness/voting topology was reviewed for a WAN-partition quorum-loss scenario.
- [ ] Connection strings use the listener name with `MultiSubnetFailover=True` where applicable.
- [ ] A forced-failover runbook exists and names the expected data-loss window.
- [ ] Readable-secondary latency (redo lag) is monitored, not just primary health.

## Checked

2026-10-22. Documentation release checked: SQL Server 2025 (17.x) via learn.microsoft.com (ver17 pages; 2022 noted where relevant).
Confirmed: Learn availability-group overview and failover pages (synchronous commit waits for log hardening, asynchronous commit allows only forced manual failover, automatic failover needs synchronous commit and a synchronized target), WSFC quorum article (odd vote count, quorum loss sets the whole cluster offline, force-quorum split-brain risk, no votes for DR-site nodes), forced-failover page (all secondary databases suspended and resumed manually, snapshot first), listener connectivity page (MultiSubnetFailover opens sockets to all IPs in parallel), readable-secondary page (snapshot isolation mapping, 14-byte overhead, tempdb, temporary blocking). Wrong in the draft: the old primary does not need a rebuild after a forced failover (resume the suspended databases), and the 21 s timeout and the claim that read load competes with redo I/O were unsourced and removed.
Method: documentation only; no commands were run.
