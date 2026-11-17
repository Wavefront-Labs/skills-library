---
id: computing-software.cloud-infrastructure-engineering.kubernetes.workload-garbage-collection-and-finalizers
name: workload-garbage-collection-and-finalizers
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, garbage-collection, cascade-foreground, cascade-background, cascade-orphan, finalizers, deletiontimestamp, deletiongraceperiodseconds, blockownerdeletion, pvc-protection, stuck-deleting, namespace-stuck-terminating, gc-controller]
level: advanced
status: docs-checked
description: "Cascading delete propagation (foreground/background/orphan), how finalizers block deletion, and the specific debugging steps for a workload object stuck Terminating."
sources: ["https://kubernetes.io/docs/concepts/architecture/garbage-collection/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/", "https://kubernetes.io/docs/tasks/administer-cluster/use-cascading-deletion/", "https://kubernetes.io/docs/concepts/storage/persistent-volumes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Workload garbage collection and finalizers — why deletion sometimes just doesn't

**Goal:** know what `kubectl delete` actually triggers under the hood so a stuck-deleting
Deployment, Job, namespace, or PVC is a five-minute diagnosis instead of a guess.
`replicaset-and-controller-reconciliation` covers how pods get *adopted*; this is the
reverse direction — how deletion propagates and what can block it.

## 1. Three cascade/propagation policies
`kubectl delete <obj> --cascade=<policy>` (Kubernetes uses background cascading deletion by
default, even without `--cascade` or `propagationPolicy`):
- **Background** (default): the object is deleted immediately; the garbage collector
  deletes dependents (owned objects) **asynchronously**, in no guaranteed order. Deleting a
  Deployment this way removes the Deployment object right away while its ReplicaSets/pods
  disappear moments later.
- **Foreground**: the owner object itself is **not actually removed** until all dependents
  with `blockOwnerDeletion: true` in their `ownerReferences` are gone. The owner instead
  gets a `metadata.deletionTimestamp` and the finalizer
  `foregroundDeletion` added automatically, and sits visible-but-terminating until its
  children are cleaned up. Use this when you need certainty that nothing is left running
  before considering the parent gone (e.g. scripted teardown that checks for the object's
  absence as its success signal).
- **Orphan** (`--cascade=orphan`): the owner gets an `orphan` finalizer and the dependents are
  left in place rather than deleted. Use it deliberately, for example to replace an owner object
  while keeping the objects it created.

## 2. Finalizers: a string that blocks the actual delete
A finalizer is just a string in `metadata.finalizers`. Deleting an object with any
finalizers present does **not** remove it from etcd — it sets `deletionTimestamp` and
leaves the object visible (`kubectl get` still shows it, `STATUS` column may show
`Terminating`) until every finalizer string is removed by whatever controller owns that
finalizer's contract. Only once the list is empty does the API server actually delete it.
- `kubernetes.io/pvc-protection`: on a PVC, protects it while a pod uses it; a PVC being
  deleted shows `Terminating` with this finalizer until no pod uses it.
- `kubernetes.io/pv-protection`: the equivalent for PVs bound to a PVC.
- Custom controllers (operators, CRDs related to workloads — e.g. a database operator
  managing a StatefulSet) commonly add their own finalizer to run cleanup (deprovision a
  cloud resource, drain data) before the object is actually gone — if that controller is
  down, crashing, or its webhook is unreachable, the object is stuck in `Terminating`
  **forever**, not just slowly, since nothing will ever remove the finalizer.

## 3. Diagnosing a stuck-Terminating workload object
1. `kubectl get <kind> <name> -o jsonpath='{.metadata.finalizers}'` — if non-empty, that's
   the blocker; identify which controller owns each finalizer string (usually a recognizable
   domain prefix, e.g. `kubernetes.io/...`, `yourco.io/...`).
2. Check that controller is actually running and not crash-looping or stuck on a webhook
   call (`kubectl get pods -n <controller-namespace>`, its logs for errors referencing this
   object's name/UID).
3. If the controller is gone for good (uninstalled operator, broken CRD) and cleanup is
   confirmed already done or unnecessary, remove the finalizer by hand:
   `kubectl patch <kind> <name> -p '{"metadata":{"finalizers":[]}}' --type=merge` — this
   is a deliberate bypass of whatever cleanup that finalizer was supposed to guarantee;
   the Kubernetes docs say to do it only when the finalizer's purpose is understood and
   accomplished some other way.
4. A namespace stuck `Terminating` is the namespaced version of the same problem at scale:
   `kubectl get namespace <ns> -o yaml` shows `status.conditions` (condition types include
   `NamespaceContentRemaining` and `NamespaceDeletionDiscoveryFailure`) naming what remains or
   failed; fix or remove finalizers on those specific resources, not the namespace object itself.

## Gotchas
- `blockOwnerDeletion` only matters for foreground cascading deletion: during foreground
  deletion only dependents with `ownerReference.blockOwnerDeletion=true` block owner deletion.
- Removing a finalizer by hand does not run whatever cleanup logic it represented — if it
  was guarding real external state (a cloud load balancer, a DNS record, a cloud disk),
  that state is now orphaned outside Kubernetes' knowledge.
- A ReplicaSet orphaned by `--cascade=orphan` on its Deployment is picked back up by label
  selector if a new ReplicaSet with the same selector is created — see
  `computing-software.cloud-infrastructure-engineering.kubernetes.replicaset-and-controller-reconciliation`
  for the adoption mechanics this enables deliberately.

## Verify
- [ ] `kubectl delete deploy <name> --cascade=foreground` visibly leaves the Deployment in
      `Terminating` until `kubectl get rs,po -l <selector>` returns empty, then it's gone.
- [ ] A PVC used by a running pod stays `Terminating` with the `pvc-protection` finalizer
      until the pod is removed.
- [ ] For any custom finalizer in use, confirm its owning controller is healthy before
      relying on deletion ever completing.
- [ ] A namespace stuck `Terminating` is resolved by fixing/removing finalizers on the
      specific resources the status conditions name, not by force-deleting the namespace.

## Checked
Checked 2026-10-24 against the kubernetes/website Garbage Collection, Finalizers, "Use cascading
deletion" and PersistentVolumes pages (default background deletion, foreground and orphan finalizers,
`blockOwnerDeletion`, protection finalizers, caution on manual removal) and the `core/v1` Namespace
condition types in kubernetes/api.
Method: documentation only; no commands were run.
