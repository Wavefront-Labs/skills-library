---
id: computing-software.cloud-infrastructure-engineering.kubernetes.mesh-ingress-egress-gateway-design
name: mesh-ingress-egress-gateway-design
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, service-mesh, istio, ingress-gateway, egress-gateway, gateway-api, tls-termination, mtls-boundary, mesh-boundary, egress-control, dedicated-gateway]
level: advanced
status: docs-checked
description: "Designing a mesh's edge: dedicated ingress/egress gateways, where TLS/mTLS terminates and re-originates, and controlling egress instead of leaving it wide open."
sources: ["https://istio.io/latest/docs/setup/additional-setup/gateway/", "https://istio.io/latest/docs/tasks/traffic-management/egress/egress-control/", "https://istio.io/latest/docs/tasks/traffic-management/egress/egress-gateway/", "https://istio.io/latest/docs/ops/configuration/traffic-management/tls-configuration/", "https://istio.io/latest/docs/tasks/traffic-management/ingress/secure-ingress/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mesh ingress/egress gateway design

**Goal:** design the boundary where traffic crosses into and out of the mesh correctly:
where TLS terminates, where mTLS begins, and whether egress is actually controlled or just
nominally routed through a gateway while still allowed anywhere. This is the edge; traffic
shaping once inside the mesh is `istio-traffic-management-virtualservice-destinationrule`
or `gateway-api-mesh-traffic-routing`.

## 1. Ingress gateway: a dedicated Envoy, not a sidecar
An Istio ingress gateway is a **separate Deployment** running Envoy with no application
container attached; it is the proxy at the mesh edge, exposed through its own Kubernetes
Service (for example a cloud load balancer). Istio's configuration for ingress and egress
gateways is identical: they are two specialized gateway deployments (the client of an
ingress gateway is outside the mesh; the destination of an egress gateway is outside it).
- **Every request through a gateway has two connections with independent TLS settings**:
  the downstream connection from the client (configured in the `Gateway` server, for
  example `tls.mode: SIMPLE`, or `MUTUAL` for client certificates) and the upstream
  connection from the gateway to the backend (configured by `DestinationRule` TLS settings
  or by auto mTLS, which sends Istio mutual TLS to sidecar-injected workloads when no TLS
  mode is configured). The usual pattern is TLS terminated at the gateway and mTLS
  to the backend. If you terminate TLS earlier (a cloud LB) and the gateway only
  sees plaintext, document that explicitly: the edge of your encrypted perimeter is then the
  cloud LB, not the Istio gateway, and anyone between them sees plaintext.
- Istio's gateway guide says a manually written gateway Deployment is the bare minimum and
  recommends a `HorizontalPodAutoscaler`, a `PodDisruptionBudget` and resource
  requests/limits for production; these are included automatically by the other gateway
  installation methods. Scale gateways independently from application workloads.
- You can deploy more than one gateway (per team or environment) with the same
  mechanisms; the guide also describes revision-specific gateway Deployments.

## 2. Egress gateway: the control most clusters skip
By default, a meshed pod can call any external host: Istio's default is
`outboundTrafficPolicy.mode: ALLOW_ANY`, so sidecars pass through requests for unknown
destinations. The mesh controls east-west traffic and does nothing about "can this pod call
an arbitrary third-party API" unless you lock it down:
```yaml
apiVersion: networking.istio.io/v1
kind: ServiceEntry
metadata: {name: external-api}
spec:
  hosts: [api.example.com]
  ports: [{number: 443, name: https, protocol: TLS}]
  location: MESH_EXTERNAL
  resolution: DNS
```
- `meshConfig.outboundTrafficPolicy.mode: REGISTRY_ONLY` (a mesh-wide setting) makes the
  proxy block any host without a matching service or `ServiceEntry`. Without it,
  `ServiceEntry` adds the host to the registry but does not stop calls to other hosts
  (`ALLOW_ANY`).
- A dedicated **egress gateway** (the same gateway Deployment pattern) centralizes
  outbound TLS origination and gives you one place to apply firewall rules for egress IPs,
  valuable when a downstream firewall needs a small, stable set of source IPs rather
  than every node's IP.
- Istio documents that it **cannot securely enforce** that all egress traffic goes through
  the egress gateway: an attacker who bypasses the sidecar can reach external hosts
  directly. The cluster administrator or cloud provider must enforce it with mechanisms
  outside Istio, such as a firewall that denies traffic not coming from the gateway, or
  Kubernetes NetworkPolicies that forbid egress not originating from the egress gateway.
  An egress `Gateway` also gives its nodes no special protection; run it on dedicated,
  hardened nodes if you need that.
- Adding `ServiceEntry` objects reactively, without ever setting `REGISTRY_ONLY`, gives
  you the upkeep of maintaining them with none of the blocking benefit.

## 3. Gateway API as the vendor-neutral edge option
Istio supports the Kubernetes Gateway API: with it you do not install and manage a gateway
`Deployment` yourself, because a gateway Deployment and Service are provisioned
automatically from the `Gateway` configuration. Decide per platform whether to standardize
on Gateway API at the edge (portable config) or stay on Istio's `Gateway`/`VirtualService`
for features Gateway API does not cover; check current conformance for the features you
need.

## Verify
- [ ] For every external host a pod calls, a `ServiceEntry` (or mesh egress policy
  equivalent) exists AND `meshConfig.outboundTrafficPolicy.mode` is `REGISTRY_ONLY`, not
  `ALLOW_ANY` by oversight.
- [ ] The actual TLS termination point (cloud LB vs. mesh gateway) is documented, not
  assumed, by checking what protocol the gateway's listener actually receives.
- [ ] Ingress gateway has its own HPA/PDB, independent of backend workload scaling.
- [ ] A downstream firewall rule referencing "the cluster's egress IPs" maps to an actual
  egress gateway's stable IP set, and a non-gateway egress path is blocked outside Istio.

## Checked
2026-10-27. Documentation releases: istio.io docs (main) and istio/api, Istio 1.31.3.
Confirmed: gateway as a separate Deployment and the identical ingress/egress configuration; two independent TLS configurations per gateway request; SIMPLE/MUTUAL modes; auto mTLS behaviour; HPA/PDB recommendation; `ALLOW_ANY` default and `REGISTRY_ONLY` effect; `networking.istio.io/v1` `ServiceEntry`; the "cannot securely enforce" egress statement and its mitigations; Gateway API automated deployment.
Method: documentation only; no commands were run.
