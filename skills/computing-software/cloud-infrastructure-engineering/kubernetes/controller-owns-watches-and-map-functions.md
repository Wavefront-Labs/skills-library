---
id: computing-software.cloud-infrastructure-engineering.kubernetes.controller-owns-watches-and-map-functions
name: controller-owns-watches-and-map-functions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, owns-watches, enqueuerequestsfrommapfunc, controller-runtime, kubebuilder, field-indexer, predicates, operators]
level: advanced
status: docs-checked
description: "Wire controller-runtime watches correctly: For/Owns for owned children, Watches with EnqueueRequestsFromMapFunc and field indexes for referenced objects, and safe predicates."
sources: ["https://book.kubebuilder.io/reference/watching-resources", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/builder/controller.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/handler/enqueue_mapped.go", "https://github.com/kubernetes-sigs/controller-runtime/blob/main/pkg/predicate/predicate.go", "https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Owns, Watches and EnqueueRequestsFromMapFunc

The question each watch answers: "when *this* object changes, which of my primary objects
must be reconciled?"

## Builder
```go
func (r *AppReconciler) SetupWithManager(mgr ctrl.Manager) error {
  // index Apps by the Secret they reference, so the map func is a cache lookup
  if err := mgr.GetFieldIndexer().IndexField(context.Background(), &appv1.App{}, ".spec.secretRef",
    func(o client.Object) []string {
      a := o.(*appv1.App)
      if a.Spec.SecretRef == "" { return nil }
      return []string{a.Spec.SecretRef}
    }); err != nil { return err }

  return ctrl.NewControllerManagedBy(mgr).
    For(&appv1.App{}, builder.WithPredicates(predicate.GenerationChangedPredicate{})).
    Owns(&appsv1.Deployment{}).
    Owns(&corev1.Service{}).
    Watches(&corev1.Secret{}, handler.EnqueueRequestsFromMapFunc(r.appsForSecret)).
    Complete(r)
}

func (r *AppReconciler) appsForSecret(ctx context.Context, obj client.Object) []reconcile.Request {
  var apps appv1.AppList
  if err := r.List(ctx, &apps, client.InNamespace(obj.GetNamespace()),
    client.MatchingFields{".spec.secretRef": obj.GetName()}); err != nil { return nil }
  reqs := make([]reconcile.Request, 0, len(apps.Items))
  for _, a := range apps.Items {
    reqs = append(reqs, reconcile.Request{NamespacedName: types.NamespacedName{Namespace: a.Namespace, Name: a.Name}})
  }
  return reqs
}
```
(Signatures are controller-runtime v0.15+: map funcs take `ctx`; `Watches` takes the object
directly, not `source.Kind`.)

## Owns requires a controller ownerReference
`Owns(&appsv1.Deployment{})` is equivalent to a `Watches` with `handler.EnqueueRequestForOwner(...,
OnlyControllerOwner())`: it enqueues only the first controller-type ownerReference of the given
type (use `builder.MatchEveryOwner` to reconcile all owners). Set the reference on create:
```go
if err := ctrl.SetControllerReference(app, dep, r.Scheme); err != nil { return ctrl.Result{}, err }
```
Cross-namespace ownerReferences are invalid (the GC deletes the child); a cluster-scoped
owner can own namespaced children, not the reverse. For cross-namespace relationships use
labels + `Watches` with a map func.

## Predicates
- `GenerationChangedPredicate` on `For` skips updates that do not change `metadata.generation`
  (for a custom resource with a status subresource, status-only writes). Caveats from its godoc:
  for built-in types generation may also change on other writes (a Deployment's generation also
  changes on annotation writes), and a status that someone else overwrites or wipes will not be
  corrected because status-only updates are not reconciled.
- Do **not** put it on `Owns`: Deployment status changes (readiness) are what you want.
- `predicate.ResourceVersionChangedPredicate` only drops updates whose resourceVersion did not
  change (such as resync events); it does not filter status-only writes. Label/annotation predicates
  and `predicate.NewPredicateFuncs` cover other filters.

## Cache and memory
Every watched type is cached cluster-wide by default. Watching all Secrets/ConfigMaps in a
big cluster costs a lot of memory: use `builder.OnlyMetadata` (`WatchesMetadata`) when you
need only names/labels, and restrict the cache with `cache.Options{ByObject: ...}` label
selectors or namespaces.

## Verify
- [ ] Changing the referenced Secret triggers a reconcile (log line or
  `controller_runtime_reconcile_total` increments); deleting an owned Deployment gets it recreated.
- [ ] envtest covers both paths.

## Checked

Checked 2026-10-27. Documentation checked: controller-runtime main branch source (latest release v0.25.2) for `builder`, `handler`, `predicate`, `controllerutil` and `cache` packages; v0.15.0 release notes; Kubernetes website main tree (v1.38 dev; v1.37 latest release) owners and dependents page. Confirmed: `Watches(object, handler)` signature and `WatchesMetadata`/`OnlyMetadata`, `handler.EnqueueRequestsFromMapFunc` taking `ctx` (changed in v0.15), `Owns` using `OnlyControllerOwner` by default, `SetControllerReference`, `GenerationChangedPredicate` behaviour and caveats, `cache.Options` `ByObject`/`DefaultNamespaces`, cross-namespace ownerReferences disallowed and a cluster-scoped owner allowed for namespaced dependents. Fixed: `ResourceVersionChangedPredicate` was described as reducing status-only noise; it does not.

Method: documentation only; no commands were run.
