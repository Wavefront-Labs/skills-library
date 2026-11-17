---
id: computing-software.cloud-infrastructure-engineering.kubernetes.controller-workqueues-and-informer-caching
name: controller-workqueues-and-informer-caching
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, client-go, informer, shared-informer, workqueue, ratelimitingqueue, delta-fifo, reflector, cache-indexer, controller-runtime-client, maxconcurrentreconciles, resync-period, field-indexer, cached-client]
level: advanced
status: docs-checked
description: "The machinery behind every controller-runtime Reconcile call: informer caches, the rate-limited workqueue, resync periods, and what watching/indexing costs in memory and API load."
sources: ["https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/cache/cache.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/cache/internal/cache_reader.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/config/controller.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/internal/controller/controller.go", "https://github.com/kubernetes/client-go/blob/master/util/workqueue/default_rate_limiters.go", "https://github.com/kubernetes/client-go/blob/master/util/workqueue/doc.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/client/doc.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controller workqueues and informer caching — what happens between a watch event and your Reconcile call

**Goal:** know what's actually running underneath `Reconcile`, so you can diagnose
"why didn't it fire," "why is memory climbing," and "why is the API server under
load" instead of guessing. This is plumbing you rarely write by hand with
controller-runtime, but you tune and debug it constantly.

## 1. The pipeline: Reflector -> DeltaFIFO -> Informer cache -> event handler -> workqueue
1. A **Reflector** opens a `List` then a `Watch` against the API server for one
   GVK, feeding changes into a **DeltaFIFO**.
2. The **shared informer** processes deltas, updating a local in-memory **cache**
   (a thread-safe store, queryable by key/index without hitting the API server)
   and invoking registered event handlers (`AddFunc`/`UpdateFunc`/`DeleteFunc`).
3. controller-runtime's generated handlers translate the raw object event into a
   `reconcile.Request{NamespacedName}` and push it onto a **workqueue**.
4. Worker goroutines (bounded by `MaxConcurrentReconciles`) pop requests and call
   your `Reconcile`.
**Shared** means one informer per GVK is reused across every controller in the
same manager that watches that type — `Owns()`/`Watches()` on five different
controllers for Pods does not open five watches; it's one informer, five sets of
handlers. This is why controller-runtime strongly prefers one manager per binary.

## 2. The cache is what your `Get`/`List` calls actually read
controller-runtime's default client reads (`Get`, `List`) from the **informer
cache**, not a live API call, for any GVK with an informer started (which happens
lazily on first use: the cache starts an informer on demand unless
`ReaderFailOnMissingInformer` is set). This is why reads are fast and don't load the
API server, and why a `Get` right after your own `Create`/`Update` can return an older
value until the informer has processed the watch event.
The controller-runtime client docs describe the pattern as reading from a cache and
writing to the API server: writes (`Create`/`Update`/`Patch`/`Delete`) go straight to
the API server.

## 3. Workqueue semantics: dedup, rate limiting, retries
The queue is a client-go rate-limiting workqueue (on current controller-runtime, a
priority queue wrapping the same rate limiter, enabled by default via `UsePriorityQueue`):
- **Deduplication**: the workqueue is "stingy": a single item will not be processed
  multiple times concurrently, and an item added several times before it can be processed
  is processed once — a storm of rapid updates to one
  object produces one reconcile, not N. This is exactly why Reconcile must
  re-fetch fresh state (section 1 of `reconciliation-loop-design`) rather than
  trusting whatever triggered the enqueue.
- **Rate limiting on requeue after error**: per-key exponential backoff starting at
  5ms and capped at 1000s, reset (`Forget`) once a reconcile for that key succeeds. With
  the default priority queue the controller's default rate limiter is this per-item
  limiter alone; with `UsePriorityQueue` disabled the client-go default controller rate
  limiter also applies an overall bucket limit of 10 qps with burst 100. A persistently
  failing object backs off on its own; it does not need manual throttling logic in Reconcile.
- `MaxConcurrentReconciles` defaults to 1 per controller (`GroupKindConcurrency` can set it
  per kind in the manager's controller config).
- `AddAfter`/`RequeueAfter` schedules a delayed re-add outside the backoff path —
  used for the "come back later" case described in `reconciliation-loop-design`.

## 4. Resync — the safety net, and the cost of relying on it
Each informer has a configurable **resync period** (controller-runtime default `10h` with
about 10 percent jitter between controllers, overridable via `cache.Options.SyncPeriod`); on
resync, every object currently in the cache is re-delivered as an artificial Update event
even though nothing changed (it does not re-sync the cache with the server), re-enqueuing a
reconcile for everything watched. This is the
backstop against missed events (a network blip, a bug in event handling) but it
is **not** a substitute for correct watches — tightening the resync period to "fix"
a controller that doesn't notice changes promptly just hides a missing `Watches()`
call behind a shorter blast radius, and a cluster-wide resync storm every N
minutes at scale (many controllers, many objects) is real, measurable API/CPU load.

## 5. Field indexers — cheap lookups without extra API calls
`mgr.GetFieldIndexer().IndexField(ctx, &corev1.Pod{}, "spec.nodeName", func(o
client.Object) []string {...})` lets later `List` calls filter by that indexed
field against the local cache (`client.MatchingFields{"spec.nodeName": "node-1"}`)
instead of listing everything and filtering in Go. Index values are automatically prefixed
with the object's namespace. The cache serves field-selector lists from these indexes and
supports exact matches only (a non-exact field match returns an error), and it does not
support the `Continue` list option. Register indexers at manager setup, before the manager
starts.

## Gotchas
- Watching a high-cardinality type cluster-wide (every Pod, every Event) without
  a namespace/label restriction grows the cache to hold every such object in
  memory — on a large cluster this is a multi-GB informer cache for a controller
  that only cares about a handful of objects. Scope watches with
  `cache.ByObject`/namespace selectors wherever the controller-runtime version
  supports it.
- `MaxConcurrentReconciles` > 1 means your Reconcile function must be safe for
  concurrent execution against *different* objects — shared mutable state
  (package-level maps, non-thread-safe clients) across reconciles is a data race
  that won't show up until load.
- Prefer watches that go through the manager's cache over hand-rolled watches, so
  shutdown and leader election are handled by controller-runtime.
- A field-selector `List` through the cached client only works for fields you registered with
  `IndexField` and only for exact matches; register the indexer for every field you filter on.

## Verify
- [ ] `controller_runtime_reconcile_total` and workqueue depth metrics
      (`workqueue_depth`, `workqueue_adds_total`) are exported and show sane
      steady-state values (depth near zero outside of bursts).
- [ ] A rapid burst of updates to one object produces a bounded number of
      reconciles (dedup working), visible in reconcile-count metrics, not one per update.
- [ ] Memory profiling (`pprof`) under a watched type with many objects shows
      cache size proportional to what's actually needed, not every object cluster-wide
      when only a subset is relevant.
- [ ] Temporarily blocking the API server's watch endpoint and restoring it
      causes the controller to self-heal via relist/resync without a restart.

## Checked

Checked 2026-10-27. Documentation checked: controller-runtime main branch source (latest release v0.25.2): `pkg/cache`, `pkg/cache/internal/cache_reader.go`, `pkg/config/controller.go`, `pkg/controller`, `pkg/internal/controller`, `pkg/metrics/workqueue.go`, `pkg/client/doc.go`; client-go workqueue package (master). Confirmed: informer-on-demand reads from the cache, writes go to the API server, workqueue dedup ("stingy") semantics, default per-item backoff 5ms to 1000s with a 10 qps / 100 burst overall limiter when the priority queue is off, `UsePriorityQueue` default on, `MaxConcurrentReconciles` default 1, `SyncPeriod` default 10h with jitter, exact-match-only cached field selectors, metric names `workqueue_depth`, `workqueue_adds_total` and `controller_runtime_reconcile_total`. Fixed: the claim that the client cache is usually updated synchronously on own writes (not documented; reads can lag), the claim that unindexed field selectors silently fall back to client-side filtering, and the rate limiter description. Removed as unconfirmed: the claim that a late `IndexField` call is rejected or ignored by version.

Method: documentation only; no commands were run.
