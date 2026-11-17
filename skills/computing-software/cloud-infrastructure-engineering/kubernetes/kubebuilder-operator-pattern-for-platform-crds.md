---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubebuilder-operator-pattern-for-platform-crds
name: kubebuilder-operator-pattern-for-platform-crds
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubebuilder, operator-sdk, controller-runtime, crd, custom-resource, reconcile-loop, operator-pattern, finalizers, status-conditions, controller-gen, platform-api, go]
level: sme
status: docs-checked
description: "Writing a Kubebuilder/controller-runtime operator for a platform CRD: reconcile-loop structure, status conditions, finalizers, and the failure modes that make operators flaky."
sources: ["https://book.kubebuilder.io/reference/good-practices", "https://book.kubebuilder.io/reference/using-finalizers", "https://book.kubebuilder.io/reference/envtest", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/cache", "https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/controller/controllerutil", "https://pkg.go.dev/k8s.io/apimachinery/pkg/apis/meta/v1#Condition"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubebuilder/controller-runtime operator pattern for platform CRDs

**Goal:** write the controller behind a custom platform API when Crossplane's
composition model doesn't fit (the resource isn't "provision and converge
external state," it's genuinely custom control logic — e.g. a
`PreviewEnvironment` CRD that spins a namespace, deploys a chart, and tears it
down on PR close with its own lifecycle rules). Platform API *design* is
`computing-software.cloud-infrastructure-engineering.kubernetes.platform-api-design-abstracting-kubernetes-complexity`;
this skill is the Go-level implementation once the API shape is decided.

## 1. Scaffold and the reconcile contract
`kubebuilder init` + `kubebuilder create api --group platform --version v1alpha1
--kind PreviewEnvironment` scaffolds the CRD type, a controller stub, and
RBAC markers. The entire controller is one function:
`Reconcile(ctx, req) (Result, error)` called whenever the watched resource
(or anything it owns, via `OwnerReference`) changes. Three return shapes
matter: `Result{}, nil` (done, wait for next event), `Result{RequeueAfter: d},
nil` (poll again after `d` — use for "wait for external thing to become
ready," not raw sleeps; the older `Requeue: true` field is deprecated), and
`Result{}, err` (controller-runtime requeues with exponential backoff
automatically unless the error is a `reconcile.TerminalError` — never hand-roll
your own retry loop on top of this, it double-backs off and makes timing
debugging miserable).

## 2. Reconcile must be idempotent and level-triggered
The single most common operator bug: writing reconcile as if it only runs
once per change ("edge-triggered" thinking). It runs on every cache resync
(SyncPeriod, default 10 hours, with 10 percent jitter), but also on every
watched-object change, on controller restart, and after any error, with the
same object state — so
every reconcile must compute "what should exist" and converge toward it,
never "do the next step" from memory. Store any cross-reconcile progress
in `status`, not in controller memory. A reconcile that creates a resource
without first checking if it already exists will either error on
AlreadyExists (annoying but recoverable) or, worse, silently duplicate
work if the check uses the wrong key.

```go
func (r *PreviewEnvReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    var pe platformv1alpha1.PreviewEnvironment
    if err := r.Get(ctx, req.NamespacedName, &pe); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }
    if !pe.DeletionTimestamp.IsZero() {
        return r.finalize(ctx, &pe)
    }
    // ... desired-state convergence, update pe.Status, r.Status().Update(ctx, &pe)
}
```

## 3. Status conditions are the user-facing API, treat them as one
`status.conditions` (the standard `metav1.Condition` slice — `Type`,
`Status`, `Reason`, `Message`, `ObservedGeneration`) is what `kubectl
describe`, Backstage cards, and other controllers watching your CRD actually
read. Set `ObservedGeneration` to the spec's `generation` on every status
update so consumers can tell "status reflects the latest spec" from "status
is stale from a previous spec version." A controller that never sets a
`Ready` condition, or sets it `True` optimistically before the real work
finishes, breaks every downstream automation built on "wait until Ready."

## 4. Finalizers — the only safe way to clean up external state
If reconcile provisions anything outside Kubernetes (a DNS record, a cloud
resource, a Slack channel), add a finalizer string in `Reconcile` (when the
object is not being deleted and lacks it; `controllerutil.AddFinalizer`) and
remove it (`controllerutil.RemoveFinalizer`) only after confirmed, idempotent
cleanup in the delete path — without this,
deleting the CR deletes the Kubernetes object immediately and your external
resource leaks forever with no record it ever existed. Gotcha: a finalizer
left on a resource whose controller is uninstalled or crashing permanently
blocks `kubectl delete` (object sits in `Terminating` forever) — give every
finalizer a clear removal path and document for on-call how to remove it
manually as a last resort.

## 5. Common flakiness sources
- **Stale cache reads**: controller-runtime's client reads from a local
  informer cache by default; a `Get` immediately after your own `Create`/
  `Update` can return stale data because the cache hasn't synced yet. Don't
  loop-retry a `Get` expecting it to see your own just-written change within
  the same reconcile — rely on the next reconcile triggered by the watch
  event instead.
- **Owned-object GC races**: `SetControllerReference` + owner-based GC
  deletes children when the parent is deleted, but if a child is deleted out
  of band (manual `kubectl delete` on a child), the controller only notices
  on its next watch event — don't assume synchronous consistency.
- **envtest vs. real cluster drift**: `envtest` (used by
  `make test`) runs a real apiserver+etcd but no kubelet, controller-manager
  or other built-in controllers, so Pod status transitions and owner-based
  garbage collection never happen in tests — integration-test anything that depends on actual Pod
  lifecycle against a real (even if small, e.g. kind) cluster, not envtest
  alone.

## Verify
- Deleting the CR triggers the finalizer path and the external resource is
  confirmed gone (not just the k8s object) before the finalizer is removed.
- Restarting the controller mid-reconcile (kill the pod) does not duplicate
  or corrupt the managed resource — reconcile from a cold cache converges to
  the same end state.
- `status.conditions[].observedGeneration` matches `metadata.generation`
  after every successful reconcile, confirmed by editing spec and checking
  status updates to the new generation, not a cached old one.

## Checked
2026-10-26. Checked against the Kubebuilder book source (repository kubernetes-sigs/kubebuilder, last commit 2026-10-25) and the controller-runtime and apimachinery source (repositories kubernetes-sigs/controller-runtime, last commit 2026-10-19, and kubernetes/apimachinery). Confirmed: errors returned from Reconcile are requeued with exponential backoff except `TerminalError`; `RequeueAfter` requeues after the duration and `Result.Requeue` is deprecated; cache SyncPeriod defaults to 10 hours (with 10 percent jitter between controllers); `metav1.Condition` fields Type, Status, ObservedGeneration, LastTransitionTime, Reason, Message; the book's finalizer pattern (add in Reconcile when absent and not deleting; run idempotent pre-delete logic then remove when deleting); `controllerutil.AddFinalizer`, `RemoveFinalizer` and `SetControllerReference`; the default client may read from a cache (`GetAPIReader` is the direct reader); envtest runs without kubelet or controller-manager. Corrected: the finalizer is added in Reconcile, not in `CreateOrUpdate`; envtest does not mention a scheduler. Removed the kubectl finalizer-patch command as not in the fetched docs.
Method: documentation only; no commands were run.
