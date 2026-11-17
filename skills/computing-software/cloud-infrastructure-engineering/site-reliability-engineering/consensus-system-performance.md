---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.consensus-system-performance
name: consensus-system-performance
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [consensus-performance, quorum-leases, batching-proposals, raft, paxos, etcd-tuning, distributed-consensus]
level: sme
status: docs-checked
description: "Tune consensus performance: RTT-bound commits, batching and pipelining, read paths (quorum leases, linearizable vs serializable reads), disk writes, and etcd timing flags."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://etcd.io/docs/v3.5/tuning/", "https://etcd.io/docs/v3.5/learning/api_guarantees/", "https://www.cs.cmu.edu/~dga/papers/leases-socc2014.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consensus system performance

SRE Book chapter on managing critical state: the two physical constraints on committing a state change are
network round-trip time and the time to write to persistent storage. Throughput comes from batching and
pipelining (and sharding); read scaling for read-heavy loads from quorum leases.

## Write path costs
- With a strong leader, Multi-Paxos needs one round trip from the proposer to a quorum of acceptors, plus the
  log disk write. A quorum spread across distant regions makes every write pay that RTT.
- **Batching**: put multiple client operations into one proposal. **Pipelining**: keep several proposals
  in flight (sliding window). Both raise throughput; batching amortises the fixed disk and network costs over many operations.
- **Disk**: log writes must be flushed directly to disk and can be the bottleneck; if a small random write takes
  about 10 ms, the SRE Book puts the limit near 100 consensus operations per second. etcd is very sensitive to disk
  latency; other processes' disk activity can cause long fsync latencies and missed heartbeats.

## Read path options
| Read type | Cost | Consistency |
|---|---|---|
| Read via consensus (quorum read) | full round trip | linearizable |
| Quorum leases (Moraru et al.) | local at lease holders for a subset of keys | linearizable; writes must contact holders |
| Follower / stale reads | local anywhere | bounded or unbounded staleness |
etcd: reads are linearizable by default and go through Raft; a client can configure a request as serializable, which may return stale data but avoids the consensus cost.

## etcd tuning
```bash
# ms; heartbeat ~= RTT between members, election timeout at least 10x RTT
etcd --heartbeat-interval=100 --election-timeout=1000 --snapshot-count=10000
sudo ionice -c2 -n0 -p `pgrep etcd`                         # prioritise disk IO
```
The etcd defaults are a 100 ms heartbeat and a 1000 ms election timeout. Across data centres or high-latency networks set the heartbeat near the RTT and the election timeout at least 10x RTT, identical on all members.

## Capacity
- A distinguished leader handles all requests, so distant clients see longer latency; the SRE Book lists sharding,
  pipelining and batching as the scaling levers.
- Keep values small and the database under the configured space quota (`--quota-backend-bytes`).

## Gotchas
- Changing the proposer costs an extra round trip and can cause dueling proposers (livelock); keep a stable leader.

## Verify
- [ ] Measured disk write latency and member-to-member RTT on the production hardware support the heartbeat and election settings.

## Checked
2026-11-01. Confirmed against the SRE Book chapter (RTT and disk constraints, batching, pipelining, sharding, quorum leases, the 10 ms example), the etcd v3.5 tuning guide (defaults, 10x rule, ionice, snapshot-count) and API guarantees page (linearizable by default, serializable option). Removed: metric thresholds, leader-lease row, size and quota figures, `check perf`, region latency ranges.
Method: documentation only; no commands were run.
