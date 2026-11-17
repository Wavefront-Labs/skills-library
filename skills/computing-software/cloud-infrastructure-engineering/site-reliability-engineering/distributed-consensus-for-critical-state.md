---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.distributed-consensus-for-critical-state
name: distributed-consensus-for-critical-state
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [site-reliability-engineering, sre, distributed-consensus, paxos, raft, leader-election, quorum, split-brain, etcd, fencing-token, distributed-lock]
level: advanced
status: docs-checked
description: "Decide when critical state needs a consensus system, what an operator must know about quorum, leaders and logs, and how to size, place and monitor it."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://etcd.io/docs/v3.5/faq/", "https://etcd.io/docs/v3.5/metrics/", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed consensus for critical state

**Goal:** state that must never be wrong (who is leader, who holds a lock, membership, configuration) lives in a
consensus system you understand well enough to size, place and monitor.

## 1. Do you need consensus? (SRE Book, Managing Critical State)
- The book's rule: whenever you see leader election, critical shared state or distributed locking, use a distributed
  consensus system that is formally proven and thoroughly tested. Informal approaches cause outages and subtle,
  hard-to-fix data consistency problems.
- Its failure examples: file-server pairs using heartbeats plus STONITH (leader election by timeouts, which
  heartbeats cannot solve correctly), and a gossip-joined search cluster where both sides of a partition elect a
  master and accept writes (split brain, data corruption).
- Leader election is equivalent to distributed consensus. Consensus protocols named: Paxos, Raft, Zab, Mencius.
  Paxos runs as numbered proposals accepted by a majority; on its own it only agrees on one value, so real systems
  use it to build a replicated state machine (RSM), which executes the same operations in the same order on several
  processes. RSMs underlie data and configuration storage, locking and leader election.
- Other patterns the chapter builds on consensus: barriers (block a group until a condition is met; a single
  coordinator would be a single point of failure, so use an RSM such as ZooKeeper), and reliable consensus-backed
  queues (good throughput, latency matters less if tasks are long).

## 2. Performance and reads (SRE Book)
- Many systems use a stable leader; all writes go through it, so clients far from the leader see higher latency and
  the leader's outgoing bandwidth can be a bottleneck. Multi-Paxos with a stable leader needs one round trip to a
  quorum in the steady state.
- To read current data you can read from the leader, or use quorum leases (a lease on part of the data granted to
  some replicas, enabling local strongly consistent reads at the cost of write performance; useful for read-heavy
  workloads concentrated in one region).
- Disk writes matter: commit latency depends on a quorum performing synchronous writes. Consensus over a LAN can
  be comparable to asynchronous leader-follower replication, but fault-tolerance benefits need replicas in
  different failure domains, which costs latency.

## 3. Deployment sizing and placement
- Replica counts, majority quorums, failure-domain placement and the downside of a sixth replica or colocated
  leaders are covered in `computing-software.cloud-infrastructure-engineering.site-reliability-engineering.failure-domain-and-multi-region-design`.
- etcd FAQ: use an odd number of members. An odd-size cluster tolerates the same number of failures as the next
  even size with fewer nodes, and during a partition an odd number guarantees a majority partition that can keep
  operating. Adding a member to reach an even number buys no extra fault tolerance.
- etcd FAQ: higher latencies between members can cause frequent elections or heartbeat timeouts with default
  settings; tune timeouts for high-latency deployments.
- etcd keeps a history of the keyspace (MVCC); without periodic compaction (for example `--auto-compaction`) it
  eventually exhausts storage, raises a space quota alarm, and answers writes with `mvcc: database space exceeded`
  until the alarm is cleared.

## 4. Monitoring (etcd 3.5 metrics page)
- `wal_fsync_duration_seconds` is the latency of fsync when etcd persists log entries before applying them, and
  `backend_commit_duration_seconds` is the backend commit latency. The metrics page says high latencies on these
  often indicate disk issues and can cause high request latency or an unstable cluster. Alert on their high
  percentiles; pick the threshold from your own baseline.
- Other families to watch are listed on the metrics page (leader, proposals, network); read it for exact names.

## 5. Distributed locks need fencing (Kleppmann)
- A lock with a timeout is not safe on its own: a client can pause and write after its lock expired. The fix the
  article gives is a fencing token, a number that increases every time a lock is granted, sent with every write to
  the storage service, which rejects a write with an older token than one already processed. ZooKeeper's zxid or
  znode version can serve as the token.
- The article argues Redlock does not produce fencing tokens and so should not be used where correctness depends on
  the lock.

## Verify
- [ ] Every use of leader election, locking or shared critical state goes through a consensus system, not heartbeats or gossip.
- [ ] The cluster has an odd member count and its quorum survives the loss of any one failure domain.
- [ ] Lock consumers send a monotonically increasing fencing token and the protected resource rejects stale ones.
- [ ] Disk commit latency and compaction/quota state are monitored.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Managing Critical State chapter, the etcd v3.5 FAQ (odd member
count, latency tuning, compaction and space quota) and metrics page (fsync and backend commit descriptions), and
Kleppmann's distributed locking article (fencing tokens, Redlock). Removed: the Raft paper (raft.pdf not fetched), the
etcd op-guide source, the Kubernetes client-go example with timings, the PromQL alert thresholds, the 10 ms fsync figure,
etcd size limits and write rates, the 1 s election default and 10x heartbeat rule, etcd/ZooKeeper read-consistency flags,
and all claims about Consul or Spanner, none of which were confirmed on the pages read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
