---
id: computing-software.database-administration.replication-high-availability.consensus-based-leader-election
name: consensus-based-leader-election
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, replication-high-availability, failover, raft, leader-election, etcd, patroni, distributed-consensus-store]
level: advanced
status: draft
description: "Run database failover through a consensus store (etcd, Consul, ZooKeeper) as Patroni and similar tools do: leader keys with TTL, quorum sizing, fencing and DCS outages."
sources:
  - https://raft.github.io/raft.pdf
  - https://etcd.io/docs/latest/faq/
  - https://patroni.readthedocs.io/en/latest/dynamic_configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Consensus-based leader election for databases

Deciding "who is primary" by having nodes ping each other leads to split brain under network
partitions. HA managers (Patroni for PostgreSQL, Orchestrator with Raft, Vitess, Stolon,
Kubernetes operators) delegate the decision to a **distributed consensus store** (DCS) such as
etcd (Raft), Consul (Raft) or ZooKeeper (ZAB).

## How it works
1. The primary holds a **leader key** in the DCS with a TTL (Patroni: `ttl: 30`) and renews it
   every `loop_wait` (10 s).
2. If the primary cannot renew (crashed, partitioned from the DCS majority), the key expires.
3. Replicas race to acquire the key via an atomic compare-and-set; only one can win because the
   DCS itself requires a majority for writes. The winner (best candidate by replication position)
   promotes.
4. A former primary that cannot reach the DCS **demotes itself** (stops accepting writes) before
   its key expires. That self-fencing is what prevents two primaries.

## Sizing the DCS
- 3 members tolerate 1 failure, 5 tolerate 2. Even numbers add no tolerance.
- Place members in **three** failure domains (e.g. AZs, or two DCs + a tie-breaker site); with two
  sites, the side holding the majority keeps working, the other cannot elect.
- Dedicated, low-latency disks for etcd (fsync latency matters), separate from database I/O.
- Back up etcd (`etcdctl snapshot save`) and monitor leader changes and fsync latency.

## Timing parameters (Patroni)
`ttl` > `loop_wait` + 2 x `retry_timeout`. Shorter TTL = faster failover but more risk of false
failovers on DCS hiccups. Typical: ttl 30, loop_wait 10, retry_timeout 10 -> failover in ~30-40 s.

## DCS outage behaviour
If the DCS loses quorum, Patroni demotes the primary to read-only by default (it cannot prove it
is still leader). Patroni 2.0+ `failsafe_mode: true` lets the primary keep running if it can reach
all cluster members directly. Know which behaviour you have.

## Fencing and routing
- Self-demotion plus a watchdog (`/dev/watchdog`, Patroni `watchdog: mode: required`) reboots a
  node that is too stuck to demote itself.
- Clients must follow the leader: HAProxy health checks against Patroni's REST API
  (`/primary` returns 200 only on the leader), DNS/VIP managed by callbacks, or libpq
  `target_session_attrs=read-write` with multiple hosts.

## Verify
Partition the primary from the DCS in a test (firewall etcd ports): it demotes within TTL, a
replica takes the leader key and promotes, HAProxy routes to it, and only one node accepts
writes throughout.
