---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.leader-election
name: leader-election
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, leader-election, distributed-lock, lease, fencing-token, kubernetes-lease, etcd, zookeeper, dynamodb-lock, blob-lease, singleton-job]
level: advanced
status: docs-checked
description: "Run exactly one active coordinator among replicas: lease-based election on k8s/etcd/DynamoDB/blob leases, fencing tokens against split brain, and lease timing."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/leader-election", "https://kubernetes.io/docs/concepts/architecture/leases/", "https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leader election

**First ask:** can the job be made safe to run concurrently (idempotent, partitioned work)?
That beats election. If not — scheduled singletons, a coordinator assigning shards — elect.

## Mechanisms
- **Kubernetes**: Lease objects in the `coordination.k8s.io` API group (see the Kubernetes Leases page for how leader election uses them).
- **Azure Storage blob lease**: the Azure pattern's sample; the first instance to acquire the lease is leader until it releases it or fails to renew, and a lease lifetime stops a faulted leader holding it forever.
- **Other coordination stores** (for example ZooKeeper) are an option; check the product docs for session and TTL behaviour.

## Fencing (the part people skip)
A paused leader (GC pause, VM stall) can wake up after its lease expired and keep writing.
Issue a monotonically increasing **fencing token** with each lease (Kleppmann's article, ZooKeeper-based example) and have the protected resource reject writes with an older token.
Without fencing, leases give no hard guarantee of a single writer.

## Timing
- Renew well before the lease expires and give the leader several attempts per lease.
- Leader stops work if it can't renew in time; don't wait for expiry.
- Failover time is bounded below by the lease lifetime; that's the availability cost.

## Gotchas
- A single Redis instance is acceptable for locks used only for efficiency, not for correctness (Kleppmann).
- Clock errors and pauses matter for lease schemes (Kleppmann's timing discussion); fence rather than trust timing.
- Observability: export a leader gauge per instance; alert if the sum stays other than 1.

## Checked
2026-10-28. Confirmed against the Azure Leader Election pattern page (mutex via blob lease, lease lifetime and renewal), Kleppmann's distributed-locking article (leases, fencing tokens, single Redis instance acceptable for efficiency locks, clock and pause problems) and the Kubernetes Leases page. Removed: client-go timing defaults, etcd/Consul/DynamoDB/Postgres advisory lock mechanisms, Azure lease 15-60 s range, the 3x renew ratio and the `SET NX PX` form (not in the fetched pages).
Method: documentation only; no commands were run.

## Verify
- [ ] SIGSTOP the leader for longer than the lease: another takes over; old leader's writes rejected on resume.
- [ ] Rolling restart: leadership moves within the gap you accepted.
