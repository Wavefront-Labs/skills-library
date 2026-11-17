---
id: computing-software.cloud-infrastructure-engineering.kubernetes.reconciliation-loop-design
name: reconciliation-loop-design
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, controller-runtime, reconcile, reconciler, idempotency, level-triggered, requeue, requeueafter, exponential-backoff, optimistic-concurrency, resourceversion, conflict-409, predicates, event-filtering, client-go, informer-cache]
level: advanced
status: docs-checked
description: "Design a controller-runtime Reconcile loop that's idempotent and level-triggered: requeue strategy, conflict handling, and the mistakes that cause hot-loops or drift."
sources: ["https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/reconcile/reconcile.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/predicate/predicate.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/config/controller.go", "https://book.kubebuilder.io/reference/good-practices"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reconciliation loop design — the one function an operator actually is

**Goal:** write `Reconcile(ctx, req) (Result, error)` so it converges a cluster
toward desired state no matter how many times, in what order, or how far apart in
time it's called — because controller-runtime WILL call it that way, by design.
This is the single most important piece of operator-writing craft; getting it wrong
produces operators that work in the demo and hot-loop or drift in production.

## 1. Level-triggered, not edge-triggered
The request you get (`req.NamespacedName`) tells you *what* object to look at, never
*what changed*. Never reason from "the event said X happened" — there is no event in
`Reconcile`'s signature, only a name. Each call must:
1. **Re-fetch** the object fresh (`r.Get(ctx, req.NamespacedName, &obj)`) — never
   reuse a cached copy from a previous call or an informer event payload.
2. Handle `NotFound` by returning `(Result{}, nil)` — the object is gone, nothing to do
   (don't treat it as an error; finalizers handle actual cleanup, see
   `computing-software.cloud-infrastructure-engineering.kubernetes.finalizers-and-garbage-collection`).
3. Compute desired state from `obj.Spec` **as it is right now**, diff against observed
   state (live child resources, not what you think you created last time), and issue
   the delta. Treat every call as if it might be the first one ever, or the
   fortieth in a row with nothing changed (periodic resync).

## 2. Idempotency is non-negotiable
Reconcile runs on: object create, every update, periodic resync (default 10h,
configurable), controller restart replaying the whole watch cache, and leader
failover. It must produce the same end state whether called once or fifty times
with no changes in between.
- Prefer `CreateOrUpdate` / `CreateOrPatch` (`controllerutil` package or hand-rolled
  get-then-create-or-update) over bare `Create` — a bare `Create` on a resync where
  the child already exists returns `AlreadyExists`, which a sloppy reconciler then
  mishandles.
- Never use `+1` / append-only logic in Reconcile (e.g. "append to a list each time
  we see this"); it must read-compute-set, not read-mutate-accumulate.
- Side effects outside Kubernetes (sending a webhook notification, provisioning a
  cloud resource with no idempotency key) need their own dedup — a resync replaying
  the same reconcile must not re-trigger them. Track "already done" in `status`, or
  use the cloud provider's idempotency token if offered.

## 3. Requeue strategy
`Reconcile` returns `(ctrl.Result, error)`:
- `error != nil` → the `Result` is ignored and the request is requeued with **exponential backoff**
  (the default per-item rate limiter starts at 5ms and caps at 1000s). Wrap an error with
  `reconcile.TerminalError` to log it without requeueing. Use plain errors for transient
  failures (API conflict, dependency not ready) — don't swallow the error into a
  manual `Result{RequeueAfter: ...}` just to avoid "noisy" logs; the backoff exists
  precisely to avoid hot-looping on persistent errors while still recovering fast
  from blips.
- `Result{Requeue: true}` → a rate-limited requeue using the workqueue's backoff (not an
  immediate requeue). The field is deprecated in favour of `RequeueAfter`: the godoc says
  there is no good reason to use it, because a retry-on-error limiter is the wrong clock for
  waiting on an external event.
- `Result{RequeueAfter: d}` (greater than zero; no need to also set `Requeue`) → correct for
  "come back and check again at a known future time" (cert about to expire, backoff window for
  an external API, polling a non-watchable resource). Not a substitute for fixing missing
  watches.
- `Result{}` with `nil` error → done until the next real event. If you find yourself
  needing a short `RequeueAfter` to "catch" something, you're usually missing a
  watch (see below), not missing a timer.

## 4. Watch what you need, not what's convenient
`SetupWithManager`'s `Owns()`/`Watches()` determine what re-triggers Reconcile.
Missing a watch on a child resource means edits to that child (manual
`kubectl edit`, another operator's side effect) never self-heal until the next
periodic resync — hours later. Over-watching (e.g. watching every ConfigMap
cluster-wide for an operator that only cares about one) floods the workqueue and
the informer cache with unrelated objects. Use `builder.WithPredicates` to filter events before they enqueue a reconcile:
`predicate.GenerationChangedPredicate` skips updates that do not change `metadata.generation`
(for a custom resource with a status subresource, status-only writes; check which writes bump
generation for built-in types), and `predicate.ResourceVersionChangedPredicate` only drops
updates whose resourceVersion is unchanged (such as resync events). A common source of
needless reconcile storms is watching objects whose `status` churns constantly for reasons you
don't care about (e.g. another controller's heartbeat field).

## 5. Optimistic concurrency and conflicts
Every write carries the `resourceVersion` you read; a concurrent writer racing you
causes your `Update` to fail with a 409 Conflict. This is correct behavior, not a
bug to work around with retries-forever:
- controller-runtime's client surfaces this as an error; let it flow into the
  default backoff-requeue (section 3) rather than hand-rolling a retry loop inside
  Reconcile — a tight in-process retry loop racing the same conflict burns CPU and
  can starve the workqueue of other work.
- Patch (`client.MergeFrom` / `client.Apply` server-side apply) instead of
  read-modify-write `Update` where you only need to change a subset of fields —
  it avoids the conflict entirely for non-overlapping writers.
- Writing to `status` should use the `/status` subresource client
  (`r.Status().Update(...)`) so spec and status writes don't race each other's
  resourceVersion.

## Gotchas
- Logging "reconciling" at the top of every call without a change-detection guard
  produces log spam on every resync that looks like a bug to the next engineer —
  log at a level that reflects whether anything actually changed.
- controller-runtime recovers panics in Reconcile by default (`RecoverPanic` defaults to true),
  turning them into errors that are requeued and counted in
  `controller_runtime_reconcile_panics_total`; watch that metric rather than relying on a crash.
- A Reconcile that takes too long blocks that worker slot; `MaxConcurrentReconciles`
  (default 1) bounds parallelism but a single stuck reconcile (hung external API call with no
  context timeout) still eats one slot — always pass `ctx` through to outbound calls and set
  a timeout; the controller option `ReconciliationTimeout` sets one per Reconcile call (there is
  no timeout by default).
- Returning early on `err != nil` from a sub-step without updating `status` first
  leaves the object looking "stuck" with no breadcrumb — set a status Condition
  before returning the error, not after.

## Verify
- [ ] Deleting a child resource by hand causes it to reappear within one reconcile
      (watch is wired), not only after the resync period.
- [ ] Running the operator with two replicas and leader election, killing the
      leader mid-reconcile, the object converges correctly after failover with no
      duplicate side effects.
- [ ] Forcing a 409 conflict (concurrent edit during a long reconcile) resolves on
      the next backoff retry without manual intervention.
- [ ] `kubectl get <cr> -o jsonpath='{.status.conditions}'` reflects the true state
      after an injected failure, not a stale success from before the failure.

## Checked

Checked 2026-10-27. Documentation checked: controller-runtime main branch source (latest release v0.25.2): `pkg/reconcile/reconcile.go`, `pkg/predicate/predicate.go`, `pkg/controller/controllerutil`, `pkg/config/controller.go`, `pkg/internal/controller`, `pkg/internal/controller/metrics`, `pkg/cache/cache.go`; kubebuilder good-practices page (master). Confirmed: error returns are requeued with backoff and `TerminalError` stops requeueing, `RequeueAfter` semantics, 5ms to 1000s default per-item limiter, 10h default resync, `CreateOrUpdate`/`CreateOrPatch` in `controllerutil`, `RecoverPanic` default true, `ReconciliationTimeout` (no default timeout), metric `controller_runtime_reconcile_panics_total`. Fixed: `Result{Requeue: true}` was described as an immediate requeue without backoff (it is rate-limited and deprecated), `ResourceVersionChangedPredicate` was described as filtering status-only updates (it does not), panics were described as crashing the process, and the helper package name (`controllerutil`).

Method: documentation only; no commands were run.
