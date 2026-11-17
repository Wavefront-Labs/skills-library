---
id: computing-software.cloud-infrastructure-engineering.kubernetes.probe-anti-patterns
name: probe-anti-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, probes, probe-anti-patterns, cascading-restarts, liveness, readiness, reliability]
level: advanced
status: docs-checked
description: "Recognise probe designs that turn a small outage into a big one: dependency checks in liveness, identical liveness and readiness, heavy probes, and readiness flapping under load."
sources: ["https://kubernetes.io/docs/concepts/workloads/pods/probes/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Probe anti-patterns

## 1. Liveness checks dependencies (the cascade)
`/healthz` pings the database. DB has a 30s blip → every pod fails liveness → kubelet
restarts all replicas at once → cold caches, connection storms on recovery, maybe
CrashLoopBackOff delays — a short DB blip becomes a much longer outage. The probe docs warn that a bad liveness probe causes cascading failures.
**Rule:** liveness answers only "is *this process* wedged?" (event loop responsive, no
deadlock). Never call downstream services from liveness.

## 2. Readiness checks shared dependencies
If all pods report not-ready when the DB is down, the Service has **zero endpoints**: clients
get connection refused / 503 from ingress instead of a graceful error page or cached data.
Readiness should reflect whether *this pod* can serve traffic better than its peers. Report
degraded dependencies via metrics/errors, not by pulling every pod.

## 3. Liveness == readiness
Same endpoint, same thresholds → when overloaded, a pod is pulled from rotation *and*
restarted, losing in-flight work. Keep liveness more tolerant than readiness. The probe docs describe using the same
low-cost HTTP endpoint for both, with a higher `failureThreshold` on liveness.

## 4. Expensive probes
Probe runs a SQL query, renders a page, or execs a JVM tool every 5s on 300 pods. Probes
should be O(1) and in-memory. exec probes fork processes — prefer httpGet/grpc.

## 5. Probe timeouts under CPU limits
1s timeout + CPU throttling at peak = failing probes exactly when traffic is highest → pods
removed/restarted → load concentrates on survivors → they fail too. Raise timeouts, reduce
throttling.

## 6. No probes at all / liveness only
Without readiness, pods receive traffic as soon as the container starts (before warm-up).
Without startupProbe, slow-start apps get liveness-killed on cold nodes.

## 7. Probing through the sidecar or Service
Probing the Service DNS name (`exec curl http://web.svc`) tests other pods. Probes must target
the local container (kubelet uses pod IP by default for httpGet).

## Detecting it
```bash
kubectl get pods -A --sort-by='.status.containerStatuses[0].restartCount' | tail
kubectl get events -A --field-selector reason=Unhealthy
```
Correlate restart spikes with dependency incidents — a match means pattern 1.

## Verify
- [ ] Killing the DB for 60s causes errors but **no** pod restarts and no zero-endpoint Services.

## Checked

Documentation release checked: Kubernetes website v1.37 docs (kubernetes/website main, 2026-10-23). Confirmed against the probe concept page and the probe task page:
- The docs caution that badly designed liveness probes cause cascading failures (restarts under load, failed client requests, more load on remaining pods).
- Readiness failure removes the pod IP from EndpointSlices of matching Services and does not restart the container; failing startup or liveness probes kill the container, subject to restartPolicy.
- The kubelet sends httpGet probes to the pod IP unless `host` is set; exec probes fork processes on each run and the docs warn about CPU overhead at high pod density.
- Restart backoff is capped at 300 seconds (pod lifecycle page).
Removed: a specific outage duration and an awk column filter that no documentation covers.

Method: documentation only; no commands were run.
