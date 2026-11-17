---
id: computing-software.cloud-infrastructure-engineering.kubernetes.startup-probe-for-slow-starting-apps
name: startup-probe-for-slow-starting-apps
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, slow-start-application, startup-probe, liveness-probe]
level: practitioner
status: docs-checked
description: "Protect slow-starting applications (JVM, warmup, migrations) with a startupProbe sized from real startup times instead of large initialDelaySeconds."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/#startup-probe", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-startup-probes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# startupProbe for slow-starting apps

## Problem
An app that takes 2-5 minutes to start (JVM warmup, cache load) gets killed by liveness unless
`initialDelaySeconds` is huge, and a huge delay then slows detection of real deadlocks for
the pod's whole life.

## Pattern
```yaml
startupProbe:
  httpGet: {path: /healthz, port: http}
  periodSeconds: 10
  failureThreshold: 30          # up to 300 s to start
livenessProbe:
  httpGet: {path: /healthz, port: http}
  periodSeconds: 10
  failureThreshold: 3           # 30 s to detect a hang after start
readinessProbe:
  httpGet: {path: /ready, port: http}
  periodSeconds: 5
```
Liveness and readiness are disabled until the startup probe succeeds once. After that the
startup probe never runs again for that container.

## Sizing
Measure real startup at p99 under worst conditions (cold node, image pull already done): time
from the container's `startedAt` (in `status.containerStatuses`) to its first successful health
response. Set
`failureThreshold x periodSeconds` to about 1.5-2x the p99.

## Gotchas
- If the app runs migrations at boot, move them to an init container or Job so restarts do not
  re-run them.
- A startupProbe that always succeeds (for example tcpSocket on a port opened early) gives no
  protection; probe the same endpoint as liveness.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed: liveness and readiness probes are not run until the startup probe succeeds, and the startup probe runs only at startup; if it never succeeds the container is killed and follows restartPolicy; the 30 x 10 = 300 s sizing example is the one in the task page; the docs advise a startup probe on the same endpoint as liveness; periodSeconds defaults to 10.
Removed: a CPU-limit startup-time example, an in-place resize remark and a jq sizing command that no documentation covers.

Method: documentation only; no commands were run.
