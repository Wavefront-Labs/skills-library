---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.distributed-locking-and-fencing
name: distributed-locking-and-fencing
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [distributed-locking, lock-fencing, fencing-token, etcd-mutex, zookeeper, distributed-consensus]
level: advanced
status: docs-checked
description: "Use distributed locks safely: consensus-backed locks (etcd, ZooKeeper), lease expiry hazards, fencing tokens checked by the resource, and when not to use a lock at all."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html", "https://pkg.go.dev/go.etcd.io/etcd/client/v3/concurrency#Mutex"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed locking and fencing

SRE Book: for leader election, critical shared state or distributed locking, use distributed consensus systems
that have been formally proven and tested thoroughly; informal approaches cause outages and subtle consistency
problems. Leases create a classic hazard (Kleppmann): a holder pauses past its lease, another client acquires the
lock, and both act.

## The hazard
```
client A acquires lock with a lease -> long GC pause -> lease expires
client B acquires lock -> writes to storage
client A wakes, still believes it holds the lock -> writes to storage  => corruption
```
Checking the lock expiry just before writing does not fix it; the pause can happen between the
check and the write.

## Fencing tokens
The lock service increments a number each time a client acquires the lock; every write to the protected
resource carries it; the storage server checks tokens and rejects writes whose token has gone backwards. This
only works if the lock service generates strictly monotonically increasing tokens.
- ZooKeeper: the `zxid` or the znode version number can serve as the token (Kleppmann).
- etcd (Go client `concurrency` package): `NewSession` (option `WithTTL`), `NewMutex`, `Mutex.Lock`,
  `Mutex.Unlock`, `Mutex.Key`, and `Mutex.IsOwner`, which returns a comparison for use in a transaction. Check
  the etcd docs before choosing a revision as a fencing token.
- Storage side (SQL example):
```sql
UPDATE reports SET body = $1, fence = $2 WHERE id = $3 AND fence < $2;  -- 0 rows => stale holder
```
- Better still, make the storage operation conditional within the consensus store itself, so the lock check
  and the write are atomic.

## Choosing
| Need | Use |
|---|---|
| Efficiency (avoid duplicate work; occasional double run is OK) | a single Redis instance is enough (Kleppmann) |
| Correctness (double run corrupts data) | consensus lock + fencing, or a transactional DB constraint |

## Gotchas
- Kleppmann: Redlock has no facility for generating fencing tokens, so it is not safe where correctness matters.
- Lock holders must renew the lease (session keepalive) and abort work on session loss.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Managing Critical State (use proven consensus systems for
locking), Kleppmann's How to do distributed locking (lease-expiry hazard, expiry check does not help, fencing tokens,
zxid or znode version, Redlock lacks tokens, efficiency versus correctness) and the pkg.go.dev etcd concurrency
page (function names listed). Removed: the CreateRevision token claim and Go snippet, the Txn compare line, the
Chubby claim, Redis SET NX PX and the coarse-lock recommendation.
Method: documentation only; no commands were run.

## Verify
- [ ] Test: pause the holder past the lease, let another acquire, resume: stale write rejected.
- [ ] Session-loss handler aborts in-progress work.
