---
id: computing-software.database-administration.replication-high-availability.multi-region-replication-topologies
name: multi-region-replication-topologies
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, multi-region, active-active, active-passive, conflict-resolution, last-write-wins, crdt, latency, cross-region-replication, geo-distribution, consistency-model]
level: advanced
status: draft
description: "Choose between active-passive and active-active multi-region database topologies, and pick a conflict-resolution strategy before, not after, concurrent writes collide."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multi-region replication topologies — active-passive vs. active-active, and conflict resolution

**Goal:** choose a multi-region topology based on actual latency and consistency
requirements, and have a conflict-resolution answer in place before two regions
write to the same row at the same time, not after.

## 1. Active-passive: simplest, has an RPO/RTO you must actually measure
One region is primary; others are async (or sync, if latency allows) read
replicas/standbys, promoted on failover. Simple to reason about (one write
authority, no conflict resolution needed), but has a real data-loss window on
unplanned failover equal to replication lag at the moment of failure, and a
failover delay (detection + promotion + traffic cutover). This is the right
default unless you have a specific reason (write latency for distant users,
regulatory data-residency for writes, or true multi-region write availability
requirements) to need more than one write region.

## 2. Active-active: lower write latency, but conflicts are now your problem
Multiple regions accept writes concurrently. Solves write-latency-for-distant-users
and gives write availability if one region goes down — at the cost of needing an
explicit answer for what happens when the same row is written in two regions
before replication catches up. There is no topology that makes this free; any
active-active design has chosen (whether deliberately or by accident) one of the
strategies below.

## 3. Conflict resolution strategies, concretely
- **Last-write-wins (LWW)**: compare timestamps, keep the later one, discard the
  earlier. Simple, but silently **loses data** — the "losing" write just vanishes,
  with no error to the client who thought it succeeded. Needs synchronized clocks
  (NTP drift matters) and is only acceptable where losing a conflicting write is
  truly fine (e.g. a "last viewed at" field, not a financial balance).
- **Application-level merge/CRDTs**: structure data so concurrent updates compose
  without loss (counters as increments not absolute values, sets as
  add/remove-wins CRDTs, sequences via version vectors). Correct, but requires
  designing the data model for it from the start — retrofitting CRDTs onto an
  existing arbitrary schema is a rewrite, not a config change.
- **Partition by owner/shard key** (the pragmatic default): route each entity to a
  single "home" region for writes (e.g. by customer/tenant), so no two regions
  ever write the *same* row concurrently even though the system is active-active
  overall. Converts a hard conflict-resolution problem into a routing problem —
  the usual real-world answer when true CRDT modeling isn't justified.
- **Reject and surface to the application**: detect the conflict (version/vector
  clock mismatch) and return an error instead of silently resolving — correct for
  data where silent loss is unacceptable and the user/application can meaningfully
  retry or merge (collaborative editing conflict dialogs are this pattern at the
  UI layer).

## 4. Latency is not just a UX number — it drives correctness decisions
Cross-region round-trip latency (often 50–150ms+ depending on distance) makes
synchronous cross-region commits (consensus across regions on every write)
expensive enough that most systems avoid it for the hot write path, pushing
toward async replication and therefore toward needing a conflict story. Measuring
actual inter-region RTT before committing to a topology avoids discovering the
latency problem after the architecture is load-bearing.

## 5. Read-your-writes consistency across regions
Even active-passive setups need a decision: does a user who just wrote to the
primary region, then immediately reads from their nearest (replica) region, see
their own write? If replication lag means no, either route that user's
subsequent reads to the primary for a short window ("sticky" session routing) or
make the application tolerant of eventual consistency for that read path —
deciding this per use case, rather than discovering it as a support ticket, is
part of the topology design, not an afterthought.

## Verify
- [ ] The decision between active-passive and active-active was driven by a measured latency/availability requirement, not assumed.
- [ ] If active-active, a specific conflict-resolution strategy (LWW/CRDT/sharded-ownership/reject) was chosen deliberately per data type, not left to whatever the replication tool defaults to.
- [ ] Clock synchronization (NTP) is monitored if any LWW logic depends on timestamp comparison.
- [ ] Read-your-writes behavior across regions was decided and tested for at least the critical user-facing flows.
- [ ] Actual inter-region RTT was measured before committing to a synchronous or near-synchronous cross-region design.
