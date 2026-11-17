---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.sidecar-pattern
name: sidecar-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, design-patterns-cloud, sidecar-pattern, sidecar, native-sidecars, init-containers, service-mesh, envoy, log-shipper, dapr, ambient-mesh]
level: practitioner
status: docs-checked
description: "Attach cross-cutting capabilities (proxy, log shipping) as a co-located container: sidecar vs library vs ambient mesh, Kubernetes native sidecar lifecycle, cost."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/sidecar", "https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/", "https://istio.io/latest/docs/ambient/overview/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sidecar

A helper process deployed alongside each app instance, sharing its lifecycle, network namespace
and (optionally) volumes. Language-agnostic, upgradable independently of the app.

## Choose between library, sidecar, node agent
| Need | Prefer |
|---|---|
| One language, deeper integration, least network overhead | library (Azure guidance: libraries give deeper integration and less network overhead) |
| Polyglot fleet needing one consistent interface | sidecar (language independent, shares the app's life cycle) |
| Evaluate first whether it is better as a separate service or a traditional daemon | separate service / daemon |
| Mesh without per-pod proxies | Istio ambient mode: per-node ztunnel (L3/L4, mTLS) plus optional waypoint proxies (L7, Envoy, run outside app pods) |

Sidecar and ambient pods can co-exist in the same Istio mesh.

## Kubernetes specifics
- Use **native sidecars**: an `initContainers` entry with `restartPolicy: Always`. The feature
  is enabled by default since Kubernetes v1.29 and stable since v1.33 (first available in v1.28).
  Sidecars follow init-container ordering: the next init container starts after the sidecar has
  started. On Pod termination, the kubelet waits for the main containers to stop, then shuts
  sidecars down in reverse order of the spec. A sidecar does not stop a Job from completing.
- A `readinessProbe` on the sidecar feeds the Pod's ready state.
- Plain multi-container Pods remain valid when you do not need start/stop ordering, or must support older clusters without container-level `restartPolicy`.
- Set requests and limits for the sidecar explicitly; they multiply across every pod.

## Gotchas
- Each application instance gets its own sidecar, so the overhead scales with instance count.
- Azure notes sidecar proximity minimises latency, but it is still a separate process: measure.
- A sidecar that is part of the Pod's readiness makes its failure domain the app's.

## Verify
- [ ] App's first outbound call at startup succeeds (proxy ready first).
- [ ] Job pods complete and terminate.
- [ ] Sidecar resource totals reviewed in cost reports.

## Checked
2026-11-08
Method: documentation only; no commands were run.
Confirmed against the Azure Architecture Center Sidecar pattern, the Kubernetes Sidecar Containers page and the Istio ambient overview. Removed unconfirmed claims: Cilium, node-agent/DaemonSet cost comparison, Istio `holdApplicationUntilProxyStarts` and `EXIT_ON_ZERO_ACTIVE_CONNECTIONS`, ECS/App Service/Cloud Run equivalents, webhook rollout advice and sub-millisecond latency.
