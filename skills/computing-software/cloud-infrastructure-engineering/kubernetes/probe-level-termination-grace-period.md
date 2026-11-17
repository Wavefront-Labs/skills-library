---
id: computing-software.cloud-infrastructure-engineering.kubernetes.probe-level-termination-grace-period
name: probe-level-termination-grace-period
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, probe-terminationgraceperiodseconds, liveness-probe, graceful-termination]
level: practitioner
status: docs-checked
description: "Set terminationGracePeriodSeconds on liveness and startup probes so a hung container is killed quickly while normal shutdowns keep the long pod grace period."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/#probe-level-terminationgraceperiodseconds", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Probe-level terminationGracePeriodSeconds

A pod with `terminationGracePeriodSeconds: 3600` (long drains, queue consumers) also waits up to
an hour when a liveness probe kills a hung container. The probe-level field (beta from 1.22, on by default from 1.25, stable in 1.28)
overrides the pod value only for probe-triggered kills.

```yaml
spec:
  terminationGracePeriodSeconds: 3600
  containers:
  - name: worker
    image: acme/worker:5
    livenessProbe:
      httpGet: {path: /healthz, port: 8080}
      periodSeconds: 10
      failureThreshold: 3
      terminationGracePeriodSeconds: 30
```

## Rules
- Allowed on `livenessProbe` and `startupProbe`; rejected on `readinessProbe` (readiness never
  kills).
- When both are set, the kubelet uses the probe-level value for a probe-triggered kill. Pod deletion without a probe failure uses the pod-level value.
- Minimum value is 1 second.

## Picking a value
Long enough to flush logs or close connections (10-60 s), short enough that a deadlocked
process restarts fast. A container that is hung will not handle SIGTERM anyway.

## Verify
```bash
kubectl get events --field-selector reason=Killing,involvedObject.name=<pod>
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState.terminated}'  # finishedAt shows when it stopped
```
After a forced liveness failure, the container should stop within about the probe-level value rather than the pod-level one.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed: probe-level `terminationGracePeriodSeconds` is stable (v1.28) and the kubelet uses it over the pod-level value; it cannot be set on readiness probes (rejected by the API server); minimum value 1; feature gate ProbeTerminationGracePeriod was alpha 1.21, beta 1.22 (off by default until 1.25), stable and removed 1.28. The Killing event appears in the task page example.
Removed: the KEP number and the claim that evictions and drains never use the probe value.

Method: documentation only; no commands were run.
