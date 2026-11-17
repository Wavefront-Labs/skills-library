---
id: computing-software.cloud-infrastructure-engineering.kubernetes.ephemeral-storage-requests-and-limits
name: ephemeral-storage-requests-and-limits
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, ephemeral-volumes, ephemeral-storage-requests, ephemeral-storage-eviction, disk-pressure]
level: practitioner
status: docs-checked
description: "Set ephemeral-storage requests and limits so the scheduler accounts for disk, know what counts (logs, writable layer, emptyDir), and avoid surprise evictions."
sources: ["https://kubernetes.io/docs/concepts/storage/ephemeral-storage/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ephemeral-storage requests and limits

```yaml
resources:
  requests:
    ephemeral-storage: 2Gi
  limits:
    ephemeral-storage: 4Gi
```

## What counts
The kubelet measures, when it manages local ephemeral storage:
- writeable container layers (files written outside volumes),
- directories holding node-level container logs,
- `emptyDir` volumes, except tmpfs ones (memory-backed `emptyDir` counts against the container memory limit).

## Scheduling
Each node has a maximum amount of local ephemeral storage it can provide for pods (see Node
Allocatable). The scheduler ensures the sum of the requests of the scheduled containers stays below
the node's capacity, so pods with large scratch needs land where disk fits.

## Enforcement
The kubelet measures usage by periodic scanning (or, with project quotas, via the
`LocalStorageCapacityIsolationFSQuotaMonitoring` feature gate, monitoring only) and marks the pod for
**eviction** when:
- a container's writeable layer plus log usage exceeds its `limits.ephemeral-storage`, or
- the sum of all containers' usage plus the pod's `emptyDir` volumes exceeds the sum of the container limits, or
- an `emptyDir` exceeds its `sizeLimit`.
Event text in the kubelet source: `Pod ephemeral local storage usage exceeds the total limit of containers 4Gi.`
This is an eviction, not a container restart. If the kubelet is not measuring local ephemeral storage, a pod
over its limit is not evicted for it, but low filesystem space still taints the node and evicts pods that do not tolerate the taint.

## Sizing
Measure real usage on a representative node (the kubelet summary API reports per-pod ephemeral storage).
Add margin for log bursts; rotate logs (kubelet `containerLogMaxSize`) and write temp files to an emptyDir
with a `sizeLimit`.

## Policy
Setting requests and limits on every pod (for example through admission-time defaults) keeps unbounded
disk writers from filling nodes and causing DiskPressure evictions of other pods.

## Checked
2026-10-23, against the Kubernetes website local ephemeral storage page (what the kubelet measures, scheduling by requests, eviction rules at container and pod level, project quota monitoring, the low-space taint) and the kubelet eviction source (event message strings and the emptyDir sizeLimit message). The `/var/log/pods` path, the PVC and image-layer remarks and the LimitRange assertion were removed as unconfirmed.
Method: documentation only; no commands were run.
