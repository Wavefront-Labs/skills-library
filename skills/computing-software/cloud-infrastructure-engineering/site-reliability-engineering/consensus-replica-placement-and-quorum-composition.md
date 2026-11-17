---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.consensus-replica-placement-and-quorum-composition
name: consensus-replica-placement-and-quorum-composition
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [replica-placement, quorum-composition, distributed-consensus, failure-domains, etcd-learner, raft-membership]
level: sme
status: docs-checked
description: "Decide how many consensus replicas to run and where: 2f+1 quorums, failure domains, latency versus survivability, load, and safe etcd membership changes."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://etcd.io/docs/v3.5/op-guide/runtime-configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replica placement and quorum composition

From the SRE Book chapter Managing Critical State: decisions are how many replicas, where, and the trade-off
between latency and failure tolerance.

## Number of replicas
- Majority quorums: 2f + 1 replicas tolerate f failures (3f + 1 if Byzantine tolerance is needed). The
  minimum is three: with two there is no tolerance for any failure.
- Three replicas run normally with one down for maintenance. An unplanned failure during maintenance then makes
  the system unavailable, so the book says run five, tolerating two failures. With four of five left no action
  is needed; with three left, add a replica or two.
- If quorum is lost the system is in theory unrecoverable; forcing a membership change may work but data loss
  is possible. Avoid it.
- Slow minority replicas can lag without slowing the quorum, but if performance varies a lot every failure may
  pull a slow outlier into the quorum.
- The decision trades off reliability need, maintenance frequency, risk, performance and cost.
- Adding a replica can slightly lower availability: five replicas tolerate two down (40 percent), six
  tolerate two (33 percent). A sixth replica colocated in one datacenter leaves no spare when that
  datacenter fails.

## Location
- Failure domains: machine, rack on one power supply, racks on one network device, a datacenter (fibre cut),
  datacenters in one region (natural disaster).
- Greater distance between replicas widens the failure you survive but raises round-trip time and usually
  operation latency. How much that matters is system dependent: a leader-election service whose transaction
  time is a fraction of the lease time is not performance critical.
- Do not widen the failure domain beyond where your clients live; it buys nothing if clients are down too.
- Keep regular snapshot backups elsewhere: software bugs and human error are failure domains you cannot escape.
- Minimise client round trip to replicas; with a stable leader, distant clients pay latency to the leader.
  Leaderless protocols (Mencius, Egalitarian Paxos) may have an edge over wide areas.

## Capacity
Read-heavy load can be eased by adding replicas that serve reads; a strong leader takes extra load per added
replica. Sharded systems scale by shard count.

## Membership changes (etcd)
Per the etcd runtime reconfiguration guide:
- Changes need a quorum of members available. Keep cluster size above two; removing a member from a two-member
  cluster is unsafe.
- A failed machine that is not removed hurts quorum and reduces tolerance for another failure; replace it
  promptly: remove the member, then add a new one. Replacing a healthy member is also remove then add.
- Prefer adding a new member as a **learner** (`etcdctl member add NAME --peer-urls=URL --learner`, v3.4
  onward), start it, then `etcdctl member promote ID`. Promotion fails until its log has caught up with the
  leader. v3.4 allows one learner at a time.
- Going from 3 to 5 is two add operations; from 5 to 3, two removes.
- Removing the leader is safe but causes a brief period without a leader during election.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Managing Critical State (Number of Replicas, Location of
Replicas, Capacity sections) and the etcd v3.5 runtime reconfiguration page. Removed: the topology table,
Spanner and `move-leader` advice, `endpoint status` check, witness replicas, example addresses and
add-before-remove claim, which those pages do not support.
Method: documentation only; no commands were run.
