---
id: computing-software.cloud-infrastructure-engineering.kubernetes.memory-limit-enforcement
name: memory-limit-enforcement
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, resource-limits, memory-limit-enforcement, oomkilled, kubelet-eviction, qos-class]
level: practitioner
status: docs-checked
description: "How memory limits are enforced (cgroup OOM kill of the container) versus kubelet eviction under node pressure, and how to tell which one hit a pod."
sources: ["https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/", "https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Memory limit enforcement vs eviction

## Two different mechanisms
| | Container OOM kill | Kubelet eviction |
|---|---|---|
| Trigger | container exceeds its own `limits.memory` (cgroup `memory.max`) | node `memory.available` below `evictionHard`/`evictionSoft` |
| Actor | Linux kernel OOM killer in that cgroup | kubelet |
| Result | container restarted (pod stays), reason `OOMKilled`, exit 137 | whole pod Failed, reason `Evicted`, rescheduled by its controller |
| Order | n/a | pods over their requests first (by priority, then by overage), Guaranteed and under-request pods last |

Node-level kernel OOM (if the kubelet cannot reclaim memory first) also happens: the `oom_killer` adds the
kubelet-set `oom_score_adj` (BestEffort 1000, Guaranteed -997, Burstable
`min(max(2, 1000 - 1000 * memoryRequestBytes / machineMemoryCapacityBytes), 999)`) to a score based on the
share of node memory used, and kills the highest. Containers in `system-node-critical` pods also get -997.

## Tell them apart
```bash
kubectl get pod <p> -o jsonpath='{.status.reason} {.status.containerStatuses[0].lastState.terminated.reason}{"\n"}'
# "Evicted" at pod level vs "OOMKilled" in container lastState
kubectl describe node <n>                  # MemoryPressure condition
kubectl get events -A --field-selector reason=Evicted
```
Kernel OOM kills are recorded in the node's kernel log.

## Details that matter
- Memory limits are enforced reactively by the kernel: a container that over-allocates is killed only when
  the kernel detects memory pressure, so it may exceed its limit for a while.
- tmpfs emptyDir (`medium: Memory`) files count against the memory limit of the container that wrote them.
- The `MemoryQoS` feature (cgroup v2) can set `memory.high` to throttle Burstable containers before the
  hard limit; it is off unless you set the kubelet `memoryThrottlingFactor` (default nil, no `memory.high`).
- Containers killed by the OOM killer can be restarted per `restartPolicy`; evicted pods are not restarted by the kubelet.

## Policy
Set memory requests equal to limits for important services (Guaranteed: they are not over their requests,
so they are evicted last, by priority) and alert before working set approaches the limit.

## Checked
2026-10-23, against the Kubernetes website resource-management page (cpu throttled vs memory OOM kill, reactive enforcement), the node-pressure eviction page (oom_score_adj table and oom_killer behaviour, eviction order, restart behaviour), the Pod QoS page (MemoryQoS, memoryThrottlingFactor default nil), the volumes page (tmpfs emptyDir counts against the memory limit), and the assign-memory task (OOMKilled, exit code 137). Runtime flag advice, the page-cache accounting statement and the 90 percent alert figure were removed as unconfirmed.
Method: documentation only; no commands were run.
