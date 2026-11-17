---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.distributed-locks
name: distributed-locks
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, distributed-systems-design, distributed-locks, fencing-tokens, leases, redlock, etcd-lease, mutual-exclusion]
level: advanced
status: docs-checked
description: "Use distributed locks only when needed and safely: leases with expiry, fencing tokens, consensus-backed lock services, and why Redlock alone is not enough for correctness."
sources: ["https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html", "https://etcd.io/docs/v3.5/dev-guide/api_concurrency_reference_v3/", "https://learn.microsoft.com/rest/api/storageservices/lease-blob"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Distributed locking and fencing tokens

## First ask
Can you avoid the lock? Options: partition work by key so only one consumer owns it, use conditional
writes/optimistic concurrency (ETags, version checks), or a single-writer queue.

## Two purposes
Ask what happens if the lock fails.
- **Efficiency** (avoid duplicate work; a failure costs a little money or a duplicate email): a single Redis instance
  with a conditional set-if-not-exists to take the lock and an atomic delete-if-value-matches to release it is enough.
  Document in the code that the lock is approximate. Do not run a five-node Redlock for this.
- **Correctness** (two holders corrupt data): use a proper consensus system (Kleppmann names ZooKeeper, for example
  via Curator lock recipes; at the very least a database with reasonable transactional guarantees) and enforce
  **fencing tokens** on every access to the resource.

## Lease + fencing pattern
1. Give every lock a timeout (a lease), so a crashed holder cannot hold it forever.
2. The lock service hands out a number that strictly increases each time the lock is acquired: the fencing token. With
   ZooKeeper, Kleppmann says the zxid or znode version can serve.
3. Every write to the protected resource carries the token; the resource remembers the highest token seen and rejects
   lower ones. This needs the resource itself to check tokens.
4. A check of lease expiry just before the write is not a fix: a pause can land between the check and the write.

Why: a holder can be paused (stop-the-world GC, page fault, CPU contention, SIGSTOP) or its write delayed in the
network (Kleppmann cites a GitHub incident with packets delayed about 90 seconds) past lease expiry, then write after
another holder took over. Fencing makes that stale write fail.

## Lock-service notes
- etcd Lock: takes a name and a lease ID; the lock is released when Unlock is called or the lease expires or is
  revoked. It returns a key that exists while the lock is held, and the API reference says this key can be used with
  transactions so updates happen only while holding the lock. Do not modify that key.
- Azure blob lease: exclusive write and delete lock on a blob, 15 to 60 seconds or infinite (`-1`); writes to a leased
  blob must include the lease ID. A duration cannot be changed by renew or change.

## Gotchas
- Redlock lacks a way to generate fencing tokens, and its safety depends on bounded network delay, process pauses and
  clock error (Redis expires keys using gettimeofday, which can jump). Kleppmann concludes it is unsafe where
  correctness depends on the lock.
- Locks without an owner check on release can be released by the wrong process.

## Verify
- [ ] Test with a paused holder (SIGSTOP) shows the stale write rejected.

## Checked
2026-11-08. Confirmed against Martin Kleppmann, How to do distributed locking (efficiency versus correctness, single
Redis for efficiency locks, leases, pause and delay examples, fencing token mechanics, ZooKeeper zxid or version,
Redlock lacking tokens and relying on timing); etcd v3 concurrency API reference (Lock, lease, returned key used with
transactions); Azure Lease Blob reference (15 to 60 seconds or infinite, lease ID on writes). Removed as not stated
in readable sources: exact `SET ... NX PX` command, DynamoDB conditional-put locks, ZooKeeper ephemeral sequential
nodes, etcd revision as fencing token, "renew well before expiry" advice; dropped the Redis docs page from sources
(it returned no readable content).
Method: documentation only; no commands were run.
