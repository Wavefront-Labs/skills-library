---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.leader-election-implementation
name: leader-election-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [leader-election-implementation, kubernetes-lease, leader-election, etcd-election, client-go, distributed-consensus]
level: advanced
status: docs-checked
description: "Implement leader election on a consensus store (client-go leaderelection, etcd Election), choose lease timings, and stop work when leadership is lost."
sources: ["https://sre.google/sre-book/managing-critical-state/", "https://pkg.go.dev/k8s.io/client-go/tools/leaderelection", "https://pkg.go.dev/go.etcd.io/etcd/client/v3/concurrency", "https://kubernetes.io/docs/concepts/architecture/leases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing leader election

SRE Book "Managing Critical State": whenever you see leader election, critical shared state or distributed
locking, use a distributed consensus system that has been formally proven and tested thoroughly. Leader election
is a reformulation of the distributed asynchronous consensus problem, which cannot be solved correctly by
heartbeats and timeouts; informal approaches lead to outages and subtle data-consistency problems. For Kubernetes
controller specifics see `computing-software.cloud-infrastructure-engineering.kubernetes.leader-election-and-ha-controllers`.

## Kubernetes: client-go leaderelection
Kubernetes uses Lease objects for component-level leader election, and your own workload may define a Lease so
replicas can elect a leader through the Kubernetes API. Name it obviously after the product or component.
```go
leaderelection.RunOrDie(ctx, leaderelection.LeaderElectionConfig{
    Lock:            lock,                 // a resourcelock built for your Lease; see the resourcelock package
    LeaseDuration:   15 * time.Second,
    RenewDeadline:   10 * time.Second,
    RetryPeriod:     2 * time.Second,
    ReleaseOnCancel: true,
    Callbacks: leaderelection.LeaderCallbacks{
        OnStartedLeading: func(ctx context.Context) { run(ctx) },    // must stop when ctx is cancelled
        OnStoppedLeading: func() { log.Fatal("lost leadership; exiting") },
        OnNewLeader:      func(id string) { log.Printf("leader is %s", id) },
    },
})
```
- 15s, 10s and 2s are the values core Kubernetes clients default to for `LeaseDuration`, `RenewDeadline` and
  `RetryPeriod`.
- `LeaseDuration`: how long non-leader candidates wait, measured from the last observed change to the record,
  before forcing acquisition. Keep it as short as your clock-rate-skew tolerance allows.
- `RenewDeadline`: how long the acting leader retries refreshing before giving up.
- `ReleaseOnCancel`: releases the lock when the run context is cancelled. Only set it if all code guarded by the
  lease has completed before cancelling, otherwise two processes may act at once.
- `OnStoppedLeading` is always called when the elector exits, even if it never started leading, and callbacks
  run asynchronously.

## etcd election
```go
s, _ := concurrency.NewSession(cli, concurrency.WithTTL(10))   // TTL in seconds
e := concurrency.NewElection(s, "/election/billing-scheduler")  // key prefix
if err := e.Campaign(ctx, podName); err != nil { return err }  // blocks until leader or ctx ends
go func() { <-s.Done(); log.Fatal("session expired; lost leadership") }()
```
Several sessions can campaign for the same prefix but only one leads at a time. With a background context
Campaign keeps blocking until it can win, unless the server returns a non-recoverable error.

## Timing rules (client-go package documentation)
- The client acts only on locally captured timestamps and uses changes in the record to see renewals, so it
  tolerates arbitrary clock skew but not arbitrary clock skew rate. Tolerance for skew rate is roughly the ratio
  of `LeaseDuration` to `RenewDeadline` (60s and 30s tolerates nodes running twice as fast as others).
  Clock synchronisation between nodes is highly recommended.
- Monitor the rate of leader transitions and increase `RetryPeriod` and `LeaseDuration` until it is stable and
  acceptably low; tolerance to API latency varies inversely with leader availability.

## The hard part: stopping the old leader
The package states that it does not guarantee only one client is acting as leader (no fencing). So:
- Exit or cancel all guarded work immediately on lost leadership.
- Use fencing tokens for side effects (see `distributed-locking-and-fencing`).
- Make leader actions idempotent.

## Gotchas
- Keep leader-only work separable from serving traffic if leadership loss should not stop serving.

## Verify
- [ ] Kill the leader: a new leader takes over within roughly the lease duration plus retry period; measure it.
- [ ] Partition the leader from the store: it stops guarded work.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Managing Critical State page, the client-go leaderelection and etcd client concurrency package pages on pkg.go.dev, and the Kubernetes Leases concept page. Removed: RBAC verbs, the "failover is roughly LeaseDuration" and GC-pause rules, the leader_election_master_status metric, the list of ZooKeeper/Consul and the claim that Leases sit on etcd, and the LeaseLock construction code, none of which appeared on a page read.

Method: docs-checked 2026-11-09 against the pages above, read from downloaded copies; no commands were run.
