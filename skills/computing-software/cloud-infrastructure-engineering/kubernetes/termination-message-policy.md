---
id: computing-software.cloud-infrastructure-engineering.kubernetes.termination-message-policy
name: termination-message-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, pod-lifecycle, terminationmessagepolicy, exit-code-137, crashloopbackoff]
level: practitioner
status: docs-checked
description: "Surface why a container died with terminationMessagePath and FallbackToLogsOnError, read it from pod status, and respect the size limits."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/determine-reason-pod-failure/", "https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Termination messages

## Mechanism
When a container exits (success or failure), the kubelet reads `terminationMessagePath` (default
`/dev/termination-log`) and stores it in
`status.containerStatuses[].state.terminated.message` (or `lastState` after a restart).

```yaml
containers:
- name: app
  image: app:1.2
  terminationMessagePath: /dev/termination-log
  terminationMessagePolicy: FallbackToLogsOnError
```
- `File` (default): only the file content.
- `FallbackToLogsOnError`: if the file is empty AND the container exited with an error, use the
  last 2048 bytes or 80 lines of logs, whichever is smaller.

`FallbackToLogsOnError` is the cheap win: every crash reason shows in `kubectl describe` without
app changes.

## App side
Write a one-line cause before exiting non-zero:
```go
os.WriteFile("/dev/termination-log", []byte("config: missing DATABASE_URL"), 0644)
os.Exit(1)
```

## Read it
```bash
kubectl describe pod <p> | grep -A4 'Last State'
kubectl get pod <p> -o jsonpath='{range .status.containerStatuses[*]}{.name}: {.lastState.terminated.exitCode} {.lastState.terminated.reason} {.lastState.terminated.message}{"\n"}{end}'
```
Custom columns across pods make crash triage fast:
```bash
kubectl get pods -o custom-columns=POD:.metadata.name,REASON:.status.containerStatuses[0].lastState.terminated.reason,MSG:.status.containerStatuses[0].lastState.terminated.message
```

## Limits and gotchas
- The kubelet truncates messages longer than 4096 bytes; the total across all containers (init containers included) is limited to 12 KiB, divided equally (12 containers get 1024 bytes each).
- `terminationMessagePath` and `terminationMessagePolicy` cannot be updated on an existing pod.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the determine-reason-pod-failure page and core/v1 types: default path `/dev/termination-log`; policy `File` (default) or `FallbackToLogsOnError`; fallback uses the log tail only when the file is empty and the container exited with an error, limited to 2048 bytes or 80 lines, whichever is smaller; 4096-byte truncation and 12 KiB total shared equally; fields cannot be updated.
Removed: remarks on readOnlyRootFilesystem and OOMKilled messages that no documentation covers.

Method: documentation only; no commands were run.
