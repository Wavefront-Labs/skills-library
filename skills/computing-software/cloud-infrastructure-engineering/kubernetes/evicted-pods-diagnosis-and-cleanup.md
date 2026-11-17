---
id: computing-software.cloud-infrastructure-engineering.kubernetes.evicted-pods-diagnosis-and-cleanup
name: evicted-pods-diagnosis-and-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting, evicted-pods, kubelet-eviction, disk-pressure, crashloopbackoff]
level: practitioner
status: docs-checked
description: "Diagnose why pods were Evicted (node pressure, ephemeral-storage limits, API-initiated), find the culprit, and clean up the Failed pod objects left behind."
sources: ["https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection", "https://github.com/kubernetes/kube-state-metrics/blob/main/docs/metrics/workload/pod-metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evicted pods

## Find them and the reason
```bash
kubectl get pods -A --field-selector=status.phase=Failed -o custom-columns=NS:.metadata.namespace,POD:.metadata.name,REASON:.status.reason,NODE:.spec.nodeName,MSG:.status.message | grep -i evict
```
Messages tell the story:
| Message | Cause |
|---|---|
| `The node was low on resource: memory. Container x was using 1.8Gi, request is 256Mi, has larger consumption of memory.` | node MemoryPressure; pods using more than their request are evicted first |
| `The node was low on resource: ephemeral-storage` | DiskPressure (logs, images, emptyDir) |
| `Pod ephemeral local storage usage exceeds the total limit of containers` | the pod's own limit |
| `Usage of EmptyDir volume "cache" exceeds the limit "1Gi"` | emptyDir sizeLimit |
| `The node had condition: [DiskPressure]` | message built from the node's pressure condition |
| `Container x exceeded its local ephemeral storage limit "1Gi".` | the container's own ephemeral-storage limit |

## Find the node-level culprit
```bash
kubectl describe node <n> | grep -A8 Conditions
kubectl get events -A --field-selector involvedObject.kind=Node,involvedObject.name=<n> | grep -iE 'evict|pressure'
kubectl top pods -A --sort-by=memory | head
```
Memory evictions repeatedly hitting the same workloads means requests are too low compared to
real usage; set requests near actual working set.

## Cleanup
Evicted pods stay as Failed objects (for inspection) until the pod GC threshold
(`--terminated-pod-gc-threshold`, default 12500) is exceeded.
```bash
kubectl delete pods -A --field-selector=status.phase=Failed
```
Controllers already replaced them; deleting the Failed objects only removes records.

## Prevent
- Requests equal to typical usage (memory especially), limits for ephemeral-storage, `sizeLimit` on emptyDir volumes.
- Larger node disks or a separate image filesystem.
- Alert on `kube_pod_status_reason{reason="Evicted"}` rate and node pressure conditions.

## Checked

Date: 2026-10-27. Documentation release: Kubernetes v1.37.1 (latest release; website main is the v1.38 development tree).

- Eviction message texts (`The node was low on resource: %v.`, `The node had condition: %v.`, `Container %s was using %s,
  request is %s, has larger consumption of %v.`, ephemeral-storage and emptyDir messages): kubelet eviction source v1.37.1.
- Evicted pods are marked Failed and replaced by the controller; pods exceeding requests are evicted first: node-pressure
  eviction page.
- PodGC cleans up terminated pods above `terminated-pod-gc-threshold` (default 12500): pod-lifecycle page and
  kube-controller-manager PodGC defaults source.
- `kube_pod_status_reason` includes `Evicted`: kube-state-metrics pod metrics page.
- Removed: image-GC-threshold advice and the `freed` event grep, which none of the checked sources covers.

Method: documentation only; no commands were run.
