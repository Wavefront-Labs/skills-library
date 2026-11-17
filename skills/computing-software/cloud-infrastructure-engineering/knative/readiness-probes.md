---
id: computing-software.cloud-infrastructure-engineering.knative.readiness-probes
name: readiness-probes
category: computing-software
field: cloud-infrastructure-engineering
product: knative
tags: [probing, readiness-probe, liveness-probe, startup-probe, queue-proxy-probe, multi-container-probing]
level: advanced
status: docs-checked
description: "Define readiness, liveness and startup probes and understand how Knative rewrites readiness through queue-proxy."
sources:
  - https://knative.dev/docs/serving/services/configure-probing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure health probes and know why Knative and Kubernetes can disagree about readiness.

Knative probing differs from Kubernetes probing: Knative probes at a vastly higher interval (aggressive probing) to shorten cold starts.

Architecture:
- Users may define Readiness, Liveness and Startup probes in the Knative Service CR.
- Liveness and Startup probes are executed by the kubelet against the container.
- Readiness probes are rewritten by Knative and executed by the Queue-Proxy container.
- Knative probes from several places (the activator, the net-* controller and the Queue-Proxy) to confirm the whole network stack is configured.
- With no user probe, Knative defines a default Readiness probe on the primary container that checks a TCP socket on the traffic port.
- Queue-Proxy has its own Readiness probe. Its health endpoint aggregates the rewritten readiness probes of all user containers, primary plus sidecars.

A Pod is ready when the Queue-Proxy probe succeeds and the networking layer reconfiguration has finished.

Pitfall: Knative may see a Pod as ready while Kubernetes does not, or the reverse. Deployment and Pod statuses do not reflect Knative's view; check the conditions on Service, Configuration, Revision, PodAutoscaler, ServerlessService, Route and Ingress.

Define probes as in Kubernetes inside `spec.template.spec.containers`. With multiple containers in one Service, enable the multiple container probing feature flag.

## Checked

2026-11-03. Confirmed on the Knative Serving services/configure-probing page: probing architecture, default TCP readiness probe, Queue-Proxy aggregation, readiness mismatch and object conditions. Removed: nothing.
Method: documentation only; no commands were run.
