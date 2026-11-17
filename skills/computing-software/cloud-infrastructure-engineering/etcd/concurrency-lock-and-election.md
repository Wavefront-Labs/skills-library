---
id: computing-software.cloud-infrastructure-engineering.etcd.concurrency-lock-and-election
name: concurrency-lock-and-election
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [lock, election, concurrency, distributed-lock, leader-election, campaign, lease, mutex]
level: advanced
status: docs-checked
description: "Distributed locks and leader election: the Lock and Election services, lease binding, leader keys and revision-based guards."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/api_concurrency_reference_v3/"
  - "https://etcd.io/docs/v3.5/learning/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd exposes client-side locking and election facilities as gRPC services.

Lock service:

- `Lock(name, lease)` acquires a distributed shared lock with the given name. On success it returns a unique key that exists for as long as the caller holds the lock. Use it with transactions so updates happen only while holding the lock.
- The lock is held until `Unlock` is called on the key or the lease attached to the owner expires or is revoked. Locking twice with the same lease is treated as a single acquisition (a no-op).
- `Unlock(key)` takes the key returned by `Lock` and releases the lock; the next waiting caller is woken and given ownership.
- Do not modify the returned key or the lock may exhibit undefined behavior.

Election service:

- `Campaign(name, lease, value)` waits to acquire leadership and returns a `LeaderKey` with `name`, `key`, `rev` and `lease`. If the lease expires or is revoked before resigning, leadership passes to the next campaigner, if any.
- The `LeaderKey` can be used to post new values, to guard API requests transactionally on leadership still being held, and to resign.
- `Proclaim` overwrites the leader's value; `Leader` returns the current proclamation, if any; `Observe` streams proclamations in order; `Resign` releases leadership so others can campaign.
- `rev` is the creation revision of the leader key: a transaction can test ownership by comparing the key's creation revision with `rev`. If the key is deleted, leadership is lost.

How it works: the client library's lock waits for ownership using the key's creation revision, and its leader election waits on modification-revision updates. Because both bind to a lease, a crashed holder loses ownership when the lease expires.

## Checked

2026-11-08. Read the v3.5 concurrency reference and the API overview in full. Confirmed: Lock, Unlock, Campaign, Proclaim, Leader, Observe, Resign semantics, LeaderKey fields, lease behaviour and creation-revision use. Removed: etcdctl lock and elect commands and the Go session remark, which the pages do not describe.

Method: documentation only; no commands were run.
