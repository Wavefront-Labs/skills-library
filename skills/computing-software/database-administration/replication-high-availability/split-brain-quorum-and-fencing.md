---
id: computing-software.database-administration.replication-high-availability.split-brain-quorum-and-fencing
name: split-brain-quorum-and-fencing
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, high-availability, split-brain, quorum, fencing, stonith, network-partition, cap-theorem, witness-node, automatic-failover, dual-primary]
level: advanced
status: draft
description: "Size quorum to survive a real network partition, and use fencing (STONITH) so a demoted primary can never keep accepting writes after failover."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Split-brain, quorum, and fencing — making failover actually safe

**Goal:** understand exactly how a database HA cluster can end up with two nodes
both believing they're primary, size quorum so a partition doesn't trigger a bad
decision, and use fencing so the old primary is physically prevented from
accepting writes after a failover, not just asked nicely to stop.

## 1. Split-brain is a partition problem, not a crash problem
Split-brain happens when a network partition (not necessarily a node crash)
separates a cluster into two groups that can each internally communicate but not
with each other. Without a correct quorum mechanism, each side can conclude "the
other side is down" and promote its own primary — now two nodes accept writes
independently, and reconciling the divergent data afterward may be lossy or
impossible for conflicting writes to the same row. This is the core reason
automatic failover is harder to get right than it sounds: the failure mode that
breaks it is exactly the condition (network trouble) that makes failover seem
most urgently needed.

## 2. Quorum: why it must be a strict majority, sized correctly
A cluster of N voting members needs **more than half** to agree before taking
action (promoting a primary, declaring another node dead) — this guarantees at
most one side of any partition can ever reach quorum, because two disjoint groups
can't both have a majority of the same N. Common sizing mistakes:
- **Even node counts** (e.g. 2 or 4 voters) can split exactly in half with
  neither side reaching majority — add a witness/arbiter (a lightweight
  quorum-only participant, no data) to break ties, or always deploy an odd number
  of full voting members.
- **Counting a DR-site replica as a full voter** can let a single WAN link
  failure cost the primary site its majority even though the primary site itself
  is perfectly healthy — site-aware/weighted quorum schemes exist specifically to
  avoid this (give the DR site's vote less weight, or exclude it from the failover
  quorum entirely and keep it manual-only).

## 3. Fencing: assume the old primary might still be alive and trying to write
Quorum tells the surviving majority it's safe to promote a new primary — it does
**not** guarantee the old primary has actually stopped. A node that's merely
unreachable from the cluster's monitoring path may still be up and reachable by
clients on a different network segment, still accepting writes. Fencing (STONITH
— "Shoot The Other Node In The Head") forcibly cuts the old primary off: power
fencing (remote power-cycle via IPMI/BMC), network fencing (disable its switch
port/revoke its storage access), or storage fencing (revoke a SAN/shared-disk
lease so it physically can't write even if it thinks it's primary). Skipping
fencing and relying on "the old primary will notice and step down" is the single
most common way a theoretically-safe quorum design still produces a real
split-brain incident.

## 4. The CAP trade-off made concrete
Under a partition, a system must choose: refuse writes on the minority side (favor
consistency, lower availability) or keep serving on both sides and reconcile later
(favor availability, risk inconsistency/conflicts). Most relational HA setups
(Postgres/MySQL/SQL Server style primary-replica with quorum-based failover)
choose consistency — the minority side becomes read-only or fully unavailable.
Multi-region active-active designs that choose availability need an explicit
conflict-resolution strategy (see the multi-region topology skill) because they've
accepted that both sides may diverge.

## 5. Testing it for real
Quorum/fencing logic is exactly the kind of thing that looks correct on paper and
fails under the specific partition shape nobody tested. Inject actual network
partitions (not just node shutdowns — a shutdown is cleanly detected, a partition
is ambiguous) between every pairing of sites/AZs in a staging environment and
confirm: exactly one side promotes, the other side's primary is fenced and
verifiably unable to accept writes, and the partition healing afterward doesn't
reintroduce the old primary without a safe rejoin procedure.

## Verify
- [ ] Voting membership is an odd number of true voters, or includes a witness/arbiter to avoid exact-tie partitions.
- [ ] DR-site or cross-WAN replicas are weighted or excluded from automatic-failover quorum, reviewed explicitly, not defaulted.
- [ ] Fencing is configured and was tested to confirm it actually blocks writes (not just alerts) on the demoted node.
- [ ] A real network-partition injection test (not just a node-kill test) has been run between each site pairing.
- [ ] The rejoin procedure for a fenced/former-primary node is documented and doesn't allow it back in without resync verification.
