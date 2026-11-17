---
id: computing-software.cloud-infrastructure-engineering.kubernetes.probe-timing-tuning
name: probe-timing-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, probe-tuning, initialdelayseconds, failurethreshold, startup-probe, periodseconds, ckad]
level: practitioner
status: docs-checked
description: "Tune probe timing fields (initialDelaySeconds, periodSeconds, timeoutSeconds, failureThreshold, successThreshold) and use startupProbe so slow starts don't trigger restart loops."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/#configure-probes", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-startup-probes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probe timing tuning

## Fields and defaults
| Field | Default | Notes |
|---|---|---|
| `initialDelaySeconds` | 0 | wait before first probe |
| `periodSeconds` | 10 | min 1; while a container is not Ready the readiness probe may also run at other times |
| `timeoutSeconds` | 1 | min 1 |
| `failureThreshold` | 3 | consecutive failures before action |
| `successThreshold` | 1 | must be 1 for liveness and startup; min 1 |
| `terminationGracePeriodSeconds` (probe-level) | pod's (30 s if unset) | min 1; not allowed on readiness probes |

**Time to act** ≈ `initialDelaySeconds + periodSeconds * failureThreshold` (+ timeouts).
With defaults a failing liveness probe restarts the container after about 30 s.

## Use startupProbe for slow starts
Instead of a huge `initialDelaySeconds` on liveness (which also delays detection of a real
startup hang and wastes time when the app starts fast):
```yaml
startupProbe:
  httpGet: {path: /healthz, port: 8080}
  periodSeconds: 5
  failureThreshold: 60          # allows up to 300s to start
livenessProbe:
  httpGet: {path: /healthz, port: 8080}
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
readinessProbe:
  httpGet: {path: /ready, port: 8080}
  periodSeconds: 5
  failureThreshold: 2
```
Liveness and readiness don't run until startup succeeds. Readiness can be aggressive (fast
removal from endpoints is cheap); liveness must be conservative (restart is expensive).

## Measure, then set
- Startup: p99 startup time from logs (`kubectl logs --timestamps`) × 1.5 for `failureThreshold*period`.
- Timeout: p99 latency of the health endpoint under load, with headroom.
- Watch `kubectl get events --field-selector reason=Unhealthy` and container restart counts.

## Gotchas
- A busy or CPU-starved container can miss the 1 s default timeout; raise `timeoutSeconds` for liveness.
- `successThreshold > 1` on readiness delays recovery; keep 1 unless flapping.
- Probe fields on a container cannot be updated in place; change them in the pod template (new pods).

## Verify
- [ ] Zero liveness-triggered restarts during a load test and during cold starts on a fresh node.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed in the probe concept page: defaults and minimums for initialDelaySeconds (0), periodSeconds (10, min 1), timeoutSeconds (1, min 1), successThreshold (1, must be 1 for liveness and startup), failureThreshold (3, min 1); probe-level terminationGracePeriodSeconds inherits the pod value (30 s default) with minimum 1; liveness and readiness do not start until the startup probe succeeds; failureThreshold x periodSeconds sizing of the startup probe (the 30 x 10 = 300 s example); the core/v1 types mark probes as `Cannot be updated`.
Removed: JVM GC and CPU-throttling advice that no documentation covers.

Method: documentation only; no commands were run.
