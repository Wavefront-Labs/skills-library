---
id: computing-software.cloud-infrastructure-engineering.kubernetes.replicaset-and-controller-reconciliation
name: replicaset-and-controller-reconciliation
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, replicaset, controller-manager, reconcile-loop, ownerreferences, label-selector, informer, watch-cache, adoption, orphaning, resourceversion, generation, observedgeneration, level-triggered, edge-triggered, pod-template-hash, kube-controller-manager]
level: advanced
status: docs-checked
description: "How workload controllers drive ReplicaSets and pods via watch and reconcile, label selectors and ownerReferences, and when adoption or orphaning surprises you."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/", "https://kubernetes.io/docs/concepts/workloads/controllers/deployment/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-controller-manager/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ReplicaSet and controller reconciliation — the loop under every workload object

**Goal:** read `kubectl get rs` / stuck reconciles correctly by knowing what the controller
is actually doing: watching, diffing desired vs observed, and acting through labels and
owner references — not by magic that "just makes pods appear."

## 1. The shape of every controller
Every built-in workload controller (Deployment, ReplicaSet, DaemonSet, Job, StatefulSet)
runs the same loop against an informer's local cache, not a live API call per tick:
1. **Watch** objects of its kind (and the pods/children it owns) via the API server's
   watch stream; keep a local cache (`client-go` informer) in sync.
2. **Enqueue** a work item (namespace/name) on any relevant change.
3. **Reconcile**: compare desired state (`spec`) to observed state (cache), issue the
   delta of create/update/delete calls, requeue on error with backoff.
This is **level-triggered, not edge-triggered**: the loop doesn't care *what* changed,
only the current diff. A missed event is self-healed on the next resync (in
kube-controller-manager the reflector resync period is random between `--min-resync-period` and
twice that value, with a default of 12h, so between 12h and 24h) — and a manually deleted pod
reappears without anyone "noticing" the delete event specifically, because the ReplicaSet controller
sees the pod count fall below `spec.replicas`.

## 2. ReplicaSet is the thing that actually owns pods
A Deployment never owns pods directly. It creates/manages ReplicaSets; each ReplicaSet's
own controller owns the pods, selecting them by `spec.selector` (immutable after creation)
and stamping `pod-template-hash` into both the ReplicaSet's selector/labels and the pod
template labels so that two ReplicaSets from the same Deployment never fight over the same
pods. `kubectl get rs -l app=api` during a rollout shows old and new ReplicaSets side by
side, each converging its own replica count toward the Deployment's current proportional
split (see `computing-software.cloud-infrastructure-engineering.kubernetes.deployment-rollout-internals`
for the surge math).

## 3. ownerReferences and adoption/orphaning
A pod is "owned" by a `metadata.ownerReferences` entry (`controller: true` marks the
managing owner; `blockOwnerDeletion` affects foreground GC). Owner references are set at
*creation*, not continuously enforced — but **selector matching is continuously enforced**:
- If a pod with no matching owner carries labels that satisfy a ReplicaSet's selector, the
  ReplicaSet **adopts** it (patches in an ownerReference) on the next reconcile. This is how
  `kubectl delete rs --cascade=orphan` followed by re-creating a ReplicaSet with the same
  selector re-adopts the orphaned pods instead of creating new ones.
  - The ReplicaSet docs state that a pod matching the selector is acquired only if it has no
    controller owner reference.
- If you edit a running pod's labels so they **no longer match** its owning ReplicaSet's
  selector, the ReplicaSet treats it as missing and creates a replacement — the edited pod
  is **orphaned**, not deleted, and now runs unmanaged until something else claims or
  deletes it. This is a classic "why do I have 4 pods for 3 replicas" bug.
- Two controllers whose selectors overlap (e.g. a hand-written ReplicaSet with a selector
  broad enough to catch a Deployment's pods) will fight: both reconcile toward their own
  replica count against a shared pod set. `kubectl apply` validation won't catch this —
  only distinct, narrow selectors (unique `pod-template-hash` or a dedicated label) do.

## 4. Reading the signals
- `generation` (spec changed) vs `status.observedGeneration` (controller has seen it): if
  they differ for more than a reconcile interval, the controller is stuck or crashing —
  check `kube-controller-manager` leader election and logs, not the workload.
- `resourceVersion` changes on every write (optimistic concurrency); a controller that
  reconciles against a stale cached version gets a 409 conflict and retries — frequent
  conflicts under heavy write load are a sign of too many actors mutating the same object.
- `kubectl get events --field-selector involvedObject.kind=ReplicaSet` shows `SuccessfulCreate`
  / `FailedCreate` (often a quota or webhook rejection) before pods ever reach the node.

## Gotchas
- Deleting a ReplicaSet with `--cascade=orphan` leaves pods running but unmanaged — easy to
  forget and lose the safety net of self-healing.
- A broad `matchLabels` selector shared accidentally across two Deployments causes silent
  pod adoption/thrashing; always make selectors as specific as the Deployment name.

## Verify
- [ ] `kubectl get rs -o jsonpath='{.items[*].metadata.ownerReferences}'` ties each
      ReplicaSet back to exactly one Deployment.
- [ ] After deliberately relabeling one pod off its ReplicaSet's selector, confirm a
      replacement pod is created and the relabeled one is orphaned (`ownerReferences` empty).
- [ ] `status.observedGeneration == metadata.generation` after any spec change settles.
- [ ] No two controllers in the namespace have overlapping `selector.matchLabels`.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; v1.37 is the latest release): ReplicaSet, Deployment (selector, pod-template-hash) and Owners and Dependents pages, and the kube-controller-manager reference. Confirmed: ReplicaSet acquires matching pods without a controller owner, relabelling a pod removes it from the ReplicaSet and a replacement is created, `--cascade=orphan` then re-creating a ReplicaSet with the same selector adopts the old pods, Deployment adds `pod-template-hash` to the ReplicaSet selector and pod template labels so child ReplicaSets do not overlap, Deployment selector immutable in apps/v1, Kubernetes does not stop overlapping selectors, `controller: true` ownerReferences on pods. Fixed: the resync period (client-go has no 10h default; kube-controller-manager uses a random value between 12h and 24h by default). Removed as unconfirmed: the adoption edge-case paragraph and the resync-storm gotcha.

Method: documentation only; no commands were run.
