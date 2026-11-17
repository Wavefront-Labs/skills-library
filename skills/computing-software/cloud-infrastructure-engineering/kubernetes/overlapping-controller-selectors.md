---
id: computing-software.cloud-infrastructure-engineering.kubernetes.overlapping-controller-selectors
name: overlapping-controller-selectors
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, overlapping-controller-selectors, label-selectors, replicaset, deployments, ownerreferences]
level: practitioner
status: docs-checked
description: "Find and fix controllers whose label selectors overlap, which makes them adopt, fight over or delete each other's pods, and Services that select both."
sources: ["https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#selector", "https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/#non-template-pod-acquisitions", "https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overlapping controller selectors

A ReplicaSet acquires any pod that matches its selector and has no controller owner reference.
Kubernetes does not stop you from overlapping selectors, and the Deployment docs warn that
controllers with overlapping selectors fight each other and behave unexpectedly. Typical symptoms
are replica counts that flap, rollouts that stall, and one workload scaling down pods created by
the other.

## Detect
```bash
kubectl get deploy,sts,ds,rs -A -o json | jq -r '.items[] |
  [.metadata.namespace, .kind, .metadata.name, (.spec.selector.matchLabels|tostring)] | @tsv' | sort -k1,1 -k4
kubectl get pods -l app=web -o custom-columns=NAME:.metadata.name,OWNER:.metadata.ownerReferences[0].name
```
Look for the same selector in one namespace, or one selector that is a subset of another
(`app: web` vs `app: web, tier: frontend`).

Services have no owner, so overlap shows as traffic going to the wrong pods:
```bash
kubectl get endpointslices -l kubernetes.io/service-name=web -o wide
```

## Fix
- Give every workload a unique label in its selector, for example
  `app.kubernetes.io/instance: <release>` plus `app.kubernetes.io/name`.
- A Deployment's selector is immutable after creation in `apps/v1`; create a new workload with the
  new selector, move traffic, delete the old one (`kubectl delete deploy old --cascade=orphan`
  only if you want the pods to keep running unmanaged or be adopted, otherwise cascade normally).
- Helm charts: two releases of a chart that hardcodes `app: name` overlap; patch the chart to
  include the release label.

## Gotchas
Bare pods created by hand with labels matching a ReplicaSet selector (and no controller owner) are
acquired by it and can then be deleted when it scales down; the ReplicaSet docs warn about this.

## Verify
Each pod's `ownerReferences` points at the expected ReplicaSet, and replica counts stay stable for 10 minutes.

## Checked

Checked 2026-10-27. Documentation checked: Kubernetes website main tree (v1.38 dev; v1.37 is the latest release): Deployment (selector section), ReplicaSet (non-template pod acquisitions), EndpointSlice and recommended labels pages. Confirmed: ReplicaSet acquires matching pods without a controller owner, Kubernetes does not prevent overlapping selectors and overlapping controllers conflict, Deployment selector immutable in apps/v1, `--cascade=orphan` behaviour, `kubernetes.io/service-name` label on EndpointSlices, `app.kubernetes.io/name` and `app.kubernetes.io/instance` recommended labels. Removed as unconfirmed: the claim that StatefulSet selectors are immutable (not stated in the StatefulSet page).

Method: documentation only; no commands were run.
