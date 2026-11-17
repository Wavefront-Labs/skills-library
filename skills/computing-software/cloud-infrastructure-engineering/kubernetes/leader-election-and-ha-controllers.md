---
id: computing-software.cloud-infrastructure-engineering.kubernetes.leader-election-and-ha-controllers
name: leader-election-and-ha-controllers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, leader-election, coordination-v1-lease, controller-runtime, failover, split-brain, leaseduration, renewdeadline, retryperiod, high-availability, poddisruptionbudget, rolling-update-operator, sharding]
level: advanced
status: docs-checked
description: "Run an operator with several replicas: controller-runtime Lease leader election, failover timing, split-brain exposure, and when to shard instead of adding replicas."
sources: ["https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/manager/manager.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/manager/internal.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/leaderelection/leader_election.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/config/controller.go", "https://github.com/kubernetes-sigs/kubebuilder/blob/master/docs/book/src/cronjob-tutorial/testdata/project/cmd/main.go", "https://kubernetes.io/docs/concepts/architecture/leases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leader election and HA controllers — one active brain, N replicas for failover only

**Goal:** run an operator at 2+ replicas for availability during pod eviction/node
drain/rolling update, with exactly one replica reconciling at any moment — and
understand how long a failover takes and what can go wrong during it.

## 1. Why operators need this at all
Unlike a stateless web service, running the *same* reconciler active on multiple
replicas simultaneously is dangerous: both would react to the same
events, race on the same `Update` calls (producing conflicts, but also duplicate
side effects on anything not perfectly idempotent — see
`computing-software.cloud-infrastructure-engineering.kubernetes.reconciliation-loop-design`).
In controller-runtime, `LeaderElection` is a manager option that is off unless you set it.
The kubebuilder scaffold exposes a `--leader-elect` flag in `cmd/main.go` (default `false`) and the
scaffolded manager Deployment passes `--leader-elect`, so extra replicas are pure standby,
not added throughput.

## 2. Mechanics: coordination.v1 Lease
controller-runtime supports only the `leases` resource lock (`coordination.v1` Lease); any other
`LeaderElectionResourceLock` value fails. The lock is one Lease named by `LeaderElectionID`, which is
**required**: the manager returns an error if it is empty. Choose an ID unique per operator —
two different operators using the same ID in the same namespace would contend for one lock.
`LeaderElectionNamespace` defaults to the pod's namespace when running in-cluster and must be set
explicitly when running outside a cluster.
```go
mgr, _ := ctrl.NewManager(cfg, ctrl.Options{
    LeaderElection:   true,
    LeaderElectionID: "widget-operator-lock",
    LeaseDuration:    &leaseDuration,  // default 15s
    RenewDeadline:    &renewDeadline,  // default 10s
    RetryPeriod:      &retryPeriod,    // default 2s
})
```
Controllers need leader election by default (`NeedLeaderElection` defaults to true), so only the
leader runs them; non-leader replicas wait. An opt-in, beta `EnableWarmup` controller option starts a
controller's sources (cache sync) before it becomes leader to shorten failover.

## 3. Failover timing — know your own number
The godoc defines `LeaseDuration` as how long non-leader candidates wait to force-acquire
leadership, measured from the last observed renewal, `RenewDeadline` as how long the acting leader
retries refreshing before giving up, and `RetryPeriod` as the wait between tries. From those
definitions, worst-case takeover after an abrupt leader loss (crash, node failure) is roughly
`LeaseDuration` plus up to one `RetryPeriod`: about 15-17 s with the defaults (derived from the
documented defaults, not a guarantee), during which no reconciliation happens. Work that arrives in
that window is handled after a new leader acquires, not lost.
- Tightening `LeaseDuration`/`RenewDeadline` shortens failover but raises the chance of a false
  failover under API server slowness or a long pause.
- `LeaderElectionReleaseOnCancel` (default `false`) makes the leader step down voluntarily when the
  manager stops, which speeds up voluntary transitions because the next leader does not wait out the
  lease. Its godoc warns it is unsafe unless the binary exits immediately after the manager stops.
  Set `terminationGracePeriodSeconds` long enough for an in-flight reconcile to finish, but not so
  long that rollouts stall.

## 4. Split-brain exposure — the case leader election doesn't fully close
Leader election lowers the chance of two reconcilers acting at once but cannot prove that a process
which lost its lease has stopped by the instant a new leader starts. When a manager loses
leadership it skips graceful shutdown and returns a "leader election lost" error from `Start`; the
standard `main` then exits. A process that is frozen (for example a long pause) can in rare timing
windows resume and issue one more write after a new leader is active. Idempotent,
conflict-tolerant reconciliation (optimistic concurrency, see `reconciliation-loop-design`) is the
real safety net.

## 5. Scaling throughput: shard, don't just add replicas
Extra replicas beyond 2 (one active, one standby) add nothing to reconcile
throughput — they are idle until a failover. If one operator genuinely needs more parallelism than
`MaxConcurrentReconciles` (default 1 per controller) gives, the pattern is **sharding**: partition
objects (by label, namespace, or a hash) across multiple independently leader-elected
deployments, each watching only its shard. This is real complexity; reach for it only after
confirming `MaxConcurrentReconciles` and vertical scaling are insufficient.

## Gotchas
- `LeaderElectionID` must be unique per *logical* operator: if staging and prod share a namespace and
  someone copy-pastes the manifest without changing the ID, they contend for one Lease.
- Replica count 1 "because leader election handles it" defeats the purpose — a crash means downtime
  until the pod restarts. HA needs 2+ replicas and a PodDisruptionBudget so voluntary disruptions
  (node drain) do not take down both at once.
- Wire probes correctly so a rolling update does not needlessly cycle a healthy standby.

## Verify
- [ ] `kubectl get lease -n <ns> widget-operator-lock -o yaml` shows
      `holderIdentity` matching the currently-active pod.
- [ ] Killing the leader pod (`kubectl delete pod`, not graceful) results in a new
      leader within roughly `LeaseDuration + RetryPeriod`, confirmed by a changed
      `holderIdentity` and resumed reconcile activity in logs/metrics.
- [ ] A rolling update of the operator Deployment causes no gap in
      `controller_runtime_reconcile_total` beyond the expected handoff window.
- [ ] A PodDisruptionBudget exists and `kubectl drain` on the leader's node does
      not take the operator fully offline.

## Checked

Checked 2026-10-27. Documentation checked: controller-runtime main branch source (latest release v0.25.2): `pkg/manager/manager.go`, `pkg/manager/internal.go`, `pkg/leaderelection/leader_election.go`, `pkg/config/controller.go`; kubebuilder cronjob tutorial `cmd/main.go` and `config/manager/manager.yaml` (master). Confirmed: defaults of 15 s / 10 s / 2 s, Lease-only lock, required `LeaderElectionID`, in-cluster namespace default, `LeaderElectionReleaseOnCancel` semantics and warning, "leader election lost" error path, `NeedLeaderElection` default true, `EnableWarmup` beta, `--leader-elect` flag default false in scaffold. Fixed: the claim that scaffolds default leader election on, that a default ID is shared, that ConfigMap/Endpoints locks remain supported, that release-on-cancel is the default, and that `os.Exit` is called on lost leadership. Removed as unconfirmed: standby replicas serving health endpoints.

Method: documentation only; no commands were run.
