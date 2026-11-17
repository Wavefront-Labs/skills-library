---
id: computing-software.cloud-infrastructure-engineering.contour.contour-architecture-contour-envoy
name: contour-architecture-contour-envoy
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [architecture, xds, bootstrap, leader-election, readiness-probe, controller-runtime, envoy-daemonset]
level: practitioner
status: docs-checked
description: "Contour architecture: Contour as xDS management server, Envoy bootstrap initContainer, watched resources, leader election write-back, probes, DaemonSet vs Deployment trade-offs."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/architecture.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Contour architecture

Two components: Envoy (data plane reverse proxy) and Contour (xDS management server). Contour runs as a Deployment; Envoy as a DaemonSet or Deployment.

Startup: in each Envoy pod Contour runs as an initContainer in `bootstrap` mode and writes the Envoy bootstrap config to a temporary volume; Envoy starts, reads it, and opens a gRPC session to Contour. Envoy retries gracefully if Contour is not up yet, so there is no start-order problem.

Contour watches (via controller-runtime) Services, Endpoints, Secrets, Ingress, HTTPProxy and optionally Gateway API objects, translating them to xDS: Services to CDS, Ingress/routes to RDS, Endpoints to EDS, and so on.

Probes:
- Envoy readiness: GET `/ready` on its admin endpoint.
- Contour liveness: `/healthz` on the pod's metrics port; readiness checks that Contour can reach the Kubernetes API.

High availability: Contour has built-in leader election. Every instance can serve xDS to any Envoy, but only the leader writes status back to HTTPProxy, Ingress and Gateway API resources. Data across instances is eventually consistent; HA also spreads xDS load and survives zone failures.

Envoy models:
- DaemonSet (standard): one Envoy per node, can use `hostPorts`; downside is that when a node is removed, `preStop` hooks are not available and connections can be dropped.
- Deployment with `podAntiAffinity` approximating the DaemonSet; when a node is removed the proper shutdown events fire, so connections drain cleanly.

## Checked

2026-11-08: read the Contour docs architecture in full. Confirmed: component roles, bootstrap initContainer flow, watched objects and xDS mapping, controller-runtime, probes, leader election and eventual consistency, and the DaemonSet versus Deployment trade-offs.

Method: documentation only; no commands were run.
