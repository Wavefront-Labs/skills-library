---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kubectl-describe-pod-triage
name: kubectl-describe-pod-triage
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, troubleshooting, describe-pod-triage, kubectl-describe, events, crashloopbackoff]
level: practitioner
status: docs-checked
description: "A systematic kubectl describe pod triage: read status, conditions, container states, last state, events and volumes in order to locate any pod failure fast."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/", "https://kubernetes.io/docs/tasks/debug/debug-application/determine-reason-pod-failure/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kubectl describe pod triage

```bash
kubectl describe pod <p> -n <ns>
```
Read top to bottom, asking one question per section.

1. **Status / Reason**: Pending, Running, Failed, or Terminating (`deletionTimestamp`).
2. **Node**: empty means never scheduled: jump to Events for `FailedScheduling`, which says
   which resource or constraint no node satisfied.
3. **Init Containers**: any not `Completed`? Init containers must finish before app
   containers start.
4. **Containers, per container**:
   - `State: Waiting` and its `Reason` (for example `ContainerCreating`, `ImagePullBackOff`,
     `CrashLoopBackOff`).
   - `Last State: Terminated` with `Reason` and `Exit Code`, and the termination message if
     one was written.
   - `Ready` and `Restart Count`.
   - Image and Image ID (is it the tag you expect?).
5. **Conditions**: `PodScheduled`, `Initialized`, `ContainersReady`, `Ready`,
   `PodReadyToStartContainers` (the Pod sandbox was created and networking configured).
   The first False is where it stopped.
6. **Volumes**: Secret/ConfigMap names, PVC claimName: compare with what exists.
7. **Events**: scheduling, image pull, volume, probe and sandbox failures show up here.

## Follow-ups by finding
| Finding | Next command |
|---|---|
| CrashLoopBackOff | `kubectl logs <p> -c <c> --previous` |
| Volume or mount events | `kubectl describe pvc <claim>` |
| Pending | `kubectl get events --field-selector involvedObject.name=<p>` and node capacity |
| No events (aged out) | `kubectl get pod <p> -o yaml` and read the status fields |

Events are kept for a limited time: the kube-apiserver `--event-ttl` defaults to 1 hour. For
older failures use pod status, logs in your log store, or an event exporter.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Pod Lifecycle" and "Debug Pods" plus the
kube-apiserver options source (latest release v1.37.1). Confirmed: pod condition names
including `PodReadyToStartContainers` and its meaning, container Waiting/Terminated states with
reason and exit code, `CrashLoopBackOff`, `FailedScheduling` in debug-pods, `--event-ttl`
default of 1 hour. Removed unconfirmed event reason lists and the exit-code number table.
Method: documentation only; no commands were run.
