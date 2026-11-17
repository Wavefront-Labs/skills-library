---
id: computing-software.cloud-infrastructure-engineering.kubernetes.gateway-api-mesh-traffic-routing
name: gateway-api-mesh-traffic-routing
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, gateway-api, httproute, grpcroute, gamma, service-mesh, istio, linkerd, east-west-traffic, parentref, traffic-splitting, vendor-neutral-routing]
level: advanced
status: docs-checked
description: "Using Gateway API's GAMMA mesh extension (HTTPRoute attached to a Service) for vendor-neutral east-west traffic splitting instead of mesh-specific CRDs like Istio's VirtualService."
sources: ["https://gateway-api.sigs.k8s.io/docs/mesh/gamma/", "https://gateway-api.sigs.k8s.io/docs/mesh/mesh-overview/", "https://gateway-api.sigs.k8s.io/reference/api-types/httproute/", "https://github.com/kubernetes-sigs/gateway-api/tree/main/conformance/reports"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gateway API mesh traffic routing (GAMMA)

**Goal:** route and split east-west (service-to-service) traffic with the vendor-neutral
`HTTPRoute`/`GRPCRoute` API instead of a mesh-specific CRD, so the routing config survives
a mesh migration (Istio ↔ Linkerd ↔ Cilium). This is distinct from using Gateway API at
the cluster edge, which is `mesh-ingress-egress-gateway-design`. Istio's own native
traffic-management CRDs are covered in `istio-traffic-management-virtualservice-destinationrule`
— that skill has richer per-feature detail (mirroring, outlier detection) than the GAMMA
subset below has today.

## 1. The mesh-routing trick: `parentRef` targets a Service, not a Gateway
Normal Gateway API attaches an `HTTPRoute` to a `Gateway` (edge). **GAMMA** (the mesh
extension to Gateway API) instead lets an `HTTPRoute`'s `parentRef` target a `Service`
directly:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata: {name: reviews-split}
spec:
  parentRefs:
  - {name: reviews, kind: Service, group: core, port: 9080}
  rules:
  - backendRefs:
    - {name: reviews-v1, port: 9080, weight: 90}
    - {name: reviews-v2, port: 9080, weight: 10}
```
Any pod calling the `reviews` Service's ClusterIP/DNS name gets split per these weights —
no mesh-specific VirtualService, no subset labels on a DestinationRule. The mesh
implementation is whatever intercepts the traffic and applies the rule. Once a Route is attached to a
Service, requests that match none of its Routes are rejected, so add a catch-all rule when you only
mean to split some traffic.

## 2. What this covers today, and what it doesn't
- GAMMA has been in the Standard channel since Gateway API v1.1.0 and is considered GA. The Service
  is the binding point because there is typically one mesh per cluster, so Gateway and GatewayClass are
  not used for mesh routing.
- Support for individual HTTPRoute features (filters such as RequestMirror, extended match types,
  weights) is declared per implementation as supported features in its conformance report. Don't assume
  parity with `istio-traffic-management-virtualservice-destinationrule` without checking the specific
  feature for your mesh and version.
- Conformance reports for mesh implementations (for example Istio and Linkerd) live in the
  Gateway API repository under `conformance/reports`; check the one matching your version.

## 3. Why bother, given the gaps
- **Consistency**: GAMMA's stated aim is consistent Gateway API behaviour across mesh projects,
  so routes written as `HTTPRoute` are less mesh-specific than VirtualServices, which are Istio CRDs.
- **One mental model across edge and mesh**: the same `HTTPRoute` kind (just a different
  `parentRef` target) is used for both ingress routing (`mesh-ingress-egress-gateway-design`)
  and mesh-internal routing — less API surface for a platform team to teach.
- Plan for "Gateway API first, the mesh's native CRD for the specific feature it lacks," not an
  all-or-nothing choice.

## Verify
- [ ] `kubectl get httproute <name> -o yaml` under `status` shows `Accepted: True` from
  the mesh's controller (not just created — Gateway API routes can exist unaccepted).
- [ ] Before relying on a feature (mirroring, fault injection) through GAMMA, checked it
  against the current conformance report for the specific mesh and version in use.
- [ ] A test request shows the expected weighted split at the Service, confirmed via
  mesh-specific observability (`service-mesh-observability-integration`), not assumed from
  the YAML alone.

## Checked

Documentation release: Gateway API docs (kubernetes-sigs/gateway-api site/content and apis/v1, latest release v1.6.3, repo commit 2026-10-23; v1.7.0 is at release-candidate stage).
Confirmed: GAMMA initiative scope (2022, east/west traffic); Routes attach to a Service via `parentRef` (`kind: Service`, `group: core`, `port`); unmatched requests are rejected once a Route is attached; Standard channel and GA since v1.1.0; Gateway and GatewayClass are not used for mesh; conformance reports exist for mesh implementations.
Removed: the claims that mirroring, outlier detection and fault injection are outside GAMMA, and the Cilium/Linkerd portability promises, which no Gateway API page states.

Method: documentation only; no commands were run.
