---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.readiness-probes
name: readiness-probes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, 12-factor-app, readiness-probes, liveness-probes, startup-probes, kubernetes-probes, health-checks]
level: practitioner
status: docs-checked
description: "Configure liveness, readiness and startup probes correctly: what each should check, timing parameters, dependency handling and avoiding restart storms."
sources: ["https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/", "https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/", "https://learn.microsoft.com/azure/container-apps/health-probes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Liveness / readiness / startup probes

## What each means (Kubernetes)
- **Startup probe**: has the app started? Until it succeeds, liveness and readiness probes do not run. It runs only at
  startup; if it fails the kubelet kills the container, subject to its restart policy. Use it for slow starters
  instead of a long liveness interval: if the container usually starts in more than
  `initialDelaySeconds + failureThreshold x periodSeconds`, add a startup probe on the liveness endpoint with a high
  `failureThreshold`, leaving the liveness settings unchanged.
- **Readiness probe**: is the container ready for traffic? Failure makes the EndpointSlice controller remove the Pod's
  IP from matching Services; the container is not restarted. It runs for the whole container lifecycle and is useful
  for warm-up (connections, files, caches) and later for recovering from temporary faults or overload.
- **Liveness probe**: when to restart a container, for example a deadlock. It does not wait for readiness. Use it
  with care: incorrect liveness probes can cause cascading failures (restarts under high load, failed requests, more
  load on the remaining pods). If the process crashes on its own you may not need one.

## Dependencies
Kubernetes suggests, when the app has a strict dependency on back-end services, a liveness probe that passes when the
app itself is healthy and a readiness probe that additionally checks each required back end, so traffic is not sent to
Pods that can only return errors. A common pattern is the same cheap HTTP endpoint for both, with a higher
`failureThreshold` on liveness so the pod is observed not-ready for a while before it is killed.

## Check mechanisms and fields
- Exactly one of `exec` (exit code 0), `grpc` (status SERVING), `httpGet` (status >= 200 and < 400) or `tcpSocket`
  (port open). `exec` forks processes on every run, which can add node CPU overhead at high pod density. The kubelet
  reads at most 10KiB of an httpGet response body, so use a minimal-body health endpoint.
- Defaults: `initialDelaySeconds` 0, `periodSeconds` 10 (minimum 1), `timeoutSeconds` 1, `successThreshold` 1 (must be
  1 for liveness and startup), `failureThreshold` 3.
- Example from the task page: startup `failureThreshold: 30` with `periodSeconds: 10` gives the app 300 seconds to
  start, then liveness with `failureThreshold: 1` takes over.
- Probe-level `terminationGracePeriodSeconds` is stable since v1.28 and is rejected for readiness probes.
- Named ports work for HTTP and TCP probes, not gRPC.

## Azure Container Apps
Startup, liveness and readiness probes, TCP or HTTP(S) only: one of each type per container, no exec, no gRPC, no named
ports. With ingress enabled the portal adds default TCP probes to the main container if you do not define them
(startup: failure threshold 240; readiness: 5 s period, failure threshold 48; liveness: TCP on the target port). In
multiple-revision mode, wait for readiness success before shifting traffic.

## Verify
- [ ] Dependency outage: pods become unready (or degrade) but are not restarted by liveness.
- [ ] Rolling update shows zero failed requests.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kubernetes probe concept page, the Configure Probes task page and the Azure Container Apps health
probes page. Removed: the sample timings and /healthz paths, "unauthenticated internal port", SIGTERM/preStop sequence,
GC-pause advice and the rule against readiness on dependency loss (not stated in the pages; the page instead suggests
dependency checks in readiness).
