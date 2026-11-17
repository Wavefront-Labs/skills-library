---
id: computing-software.cloud-infrastructure-engineering.kubernetes.finalizers-and-garbage-collection
name: finalizers-and-garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, operator, finalizer, deletiontimestamp, garbage-collection, ownerreferences, cascading-deletion, stuck-terminating, foreground-deletion, background-deletion, controller-runtime, controllerutil-addfinalizer]
level: advanced
status: docs-checked
description: "Use finalizers to clean up external resources before deletion: deletionTimestamp handling, idempotent cleanup, removal ordering and unsticking a Terminating object."
sources: ["https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/", "https://kubernetes.io/docs/concepts/architecture/garbage-collection/", "https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/", "https://github.com/kubernetes-sigs/controller-runtime/tree/main/pkg/controller/controllerutil"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finalizers and garbage collection — cleaning up what Kubernetes itself can't see

**Goal:** when a custom resource is deleted, anything it created *outside*
Kubernetes' own object graph (a cloud load balancer, an IAM role, a row in an
external database, a DNS record) gets torn down reliably — without ever leaving a
cluster object permanently stuck in `Terminating`.

## 1. What native garbage collection already handles
If every child is a Kubernetes object with an `ownerReference` back to the parent,
the garbage collector handles cascading delete for free — no finalizer needed.
- **Foreground** (`propagationPolicy: Foreground`, `kubectl delete --cascade=foreground`):
  the *owner* gets a `foregroundDeletion` finalizer and stays visible (with
  `deletionTimestamp` set) until all dependents with `ownerReference.blockOwnerDeletion=true`
  are gone, then the owner itself is removed.
- **Background** (the default, even without `--cascade` or `propagationPolicy`): the API server
  deletes the owner immediately; the garbage collector deletes dependents asynchronously afterward.
  The owner can disappear from `kubectl get` while children are still being cleaned up.
- **Orphan** (`--cascade=orphan`, `propagationPolicy: Orphan`): the dependents are left in place
  and nothing is deleted. Useful deliberately (planned migration); dangerous by accident.
Write a finalizer **only** for things the GC graph cannot see: anything outside
the Kubernetes API (cloud provider resources, external SaaS state, data in a
different system) or ordering the GC can't express.

## 2. The finalizer protocol
1. On create (or first reconcile), add your finalizer string
   (`controllerutil.AddFinalizer(&obj, "widgets.apps.example.com/finalizer")`) if
   absent, then `Update`. Custom finalizer names must be qualified names such as
   `example.com/finalizer-name`; the API server rejects writes that use an unqualified custom finalizer.
2. On delete request, the API server does **not** remove the object; it sets
   `metadata.deletionTimestamp`, returns 202, and keeps the object until every entry is removed
   from `metadata.finalizers`. After that point you can remove finalizers but cannot add new
   ones, and cannot change `deletionTimestamp`.
3. Reconcile sees `!obj.DeletionTimestamp.IsZero()` → run cleanup logic instead of
   normal reconciliation.
4. Cleanup succeeds → `controllerutil.RemoveFinalizer(&obj, ...)` then `Update`.
   Once the finalizer list is empty (and no other finalizer from another
   controller remains), the API server actually deletes the object.
```go
if !widget.DeletionTimestamp.IsZero() {
    if controllerutil.ContainsFinalizer(&widget, finalizerName) {
        if err := r.cleanupExternalResources(ctx, &widget); err != nil {
            return ctrl.Result{}, err   // requeues with backoff; finalizer stays
        }
        controllerutil.RemoveFinalizer(&widget, finalizerName)
        if err := r.Update(ctx, &widget); err != nil {
            return ctrl.Result{}, err
        }
    }
    return ctrl.Result{}, nil
}
```

## 3. Cleanup must be idempotent and must tolerate partial completion
The cleanup function runs every reconcile while the object is terminating until it
returns success — including after a crash mid-cleanup. Design it as:
"check if the external thing still exists; if so, delete it; if not, treat as
success" — never "delete it" unconditionally (a second call then errors on
not-found, which, if treated as failure, means the object is stuck forever).
Record partial progress in `status` if cleanup has multiple external resources, so
a crash doesn't force re-discovering what's already gone from scratch each time.

## 4. Unsticking a stuck Terminating object
The most common operator support ticket: an object stuck in `Terminating` forever.
Causes, in order of likelihood:
1. **Cleanup is failing silently or looping** — check controller logs/events for
   the actual error from `cleanupExternalResources`; this is the correct fix,
   never remove the finalizer by hand first.
2. **The controller that owns the finalizer is down or was uninstalled** —
   nothing will ever call Reconcile to remove it. Confirm the owning controller
   pod exists and is healthy before assuming this.
3. **Only after confirming the controller is gone for good** (uninstalled
   deliberately, CRD being decommissioned): manually remove the finalizer entry
   (for example `kubectl edit` and delete the array entry). The Kubernetes docs say to avoid
   removing finalizers by hand unless the finalizer's purpose is understood and accomplished some
   other way (for example, cleaning up the dependent object manually). This bypasses cleanup
   entirely, so whatever the finalizer protected (external resources) must be cleaned up by hand.

## Gotchas
- Finalizers added by multiple controllers on the same object: the object stays
  Terminating until every one of them is removed — a hung second controller blocks
  deletion even if yours is fine. `kubectl get widget foo -o jsonpath='{.metadata.finalizers}'`
  shows exactly which ones remain.
- Finalizers can also block deletion of dependents, so an owner can stay `Terminating`
  longer than expected; the Kubernetes docs say to check finalizers and owner references on
  both the owner and its dependents.
- Add the finalizer in the reconciler (as in the protocol above) rather than a webhook, so the
  same controller that adds it also removes it.

## Verify
- [ ] Deleting the custom resource while its external dependency is intentionally
      unreachable (simulate an API outage) leaves it `Terminating`, not silently
      deleted with the external resource orphaned.
- [ ] Restoring reachability causes cleanup to complete and the object to
      disappear within one reconcile, with no manual intervention.
- [ ] `kubectl get <cr> -o jsonpath='{.metadata.finalizers}'` is empty immediately
      before the object vanishes — never force-removed during normal operation.
- [ ] Killing the controller mid-cleanup and restarting it resumes and completes
      cleanup rather than erroring on "already deleted" external state.

## Checked
Checked 2026-10-24 against the kubernetes/website Finalizers, Garbage Collection and "Use cascading
deletion" pages (background is the default, foreground and orphan semantics, `blockOwnerDeletion`,
qualified finalizer names, no adding finalizers after deletion is requested, 202 response, caution about
removing finalizers) and controller-runtime `controllerutil` (`AddFinalizer`, `RemoveFinalizer`,
`ContainsFinalizer`).
Method: documentation only; no commands were run.
