---
id: computing-software.cloud-infrastructure-engineering.kubernetes.matchlabelkeys-spread-and-affinity
name: matchlabelkeys-spread-and-affinity
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, scheduling, matchlabelkeys, topology-spread-constraints, pod-anti-affinity, rolling-update]
level: practitioner
status: docs-checked
description: "Use matchLabelKeys (with pod-template-hash) in topology spread and pod affinity so spreading counts only the current revision during rolling updates."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/#topology-spread-constraint-definition", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#matchlabelkeys"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# matchLabelKeys

## Problem
During a rolling update, old and new ReplicaSet pods share `app: web`. Spread constraints and
anti-affinity count both, so new pods are placed to balance the combined set; when old pods go
away the new revision ends up skewed (for example 4 pods in zone a, 2 in zone b).

## Fix
```yaml
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector:
    matchLabels: {app: web}
  matchLabelKeys:
  - pod-template-hash
```
At pod creation kube-apiserver looks up the incoming pod's value for each key in `matchLabelKeys`
and merges those key-value labels into `labelSelector`, so only pods of the same revision are
counted. `matchLabelKeys` cannot be set when `labelSelector` is not set. For spread constraints the
field is beta since v1.27.

Pod affinity / anti-affinity also accept `matchLabelKeys` and `mismatchLabelKeys` (keys whose label
values must not match the incoming pod's); both are beta and on by default, controlled by the
`MatchLabelKeysInPodAffinity` feature gate:
```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
    - labelSelector: {matchLabels: {app: web}}
      matchLabelKeys: [pod-template-hash]
      topologyKey: kubernetes.io/hostname
```

## Notes
- Keys absent on the pod are ignored.
- A key cannot appear in both `labelSelector` and `matchLabelKeys`.
- Don't use keys whose label may be edited directly on live pods: the merged selector is not updated.
- Spread is evaluated only at scheduling time (scaling down can leave skew); a tool such as the
  Descheduler can rebalance pods.

## Verify
```bash
kubectl get pods -l app=web -o custom-columns=POD:.metadata.name,HASH:.metadata.labels.pod-template-hash,NODE:.spec.nodeName
kubectl get nodes -L topology.kubernetes.io/zone
```
After a rollout, count new-hash pods per zone; the difference should be at most maxSkew.

## Checked
2026-10-23, against the Kubernetes website pages for topology spread constraints (matchLabelKeys merge at creation, same-key and labelSelector rules, beta since v1.27, Descheduler note, caution about directly edited labels) and assign-pod-node (matchLabelKeys and mismatchLabelKeys beta, MatchLabelKeysInPodAffinity gate). The StatefulSet controller-revision-hash and descheduler strategy-name claims were removed as unconfirmed.
Method: documentation only; no commands were run.
