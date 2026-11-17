---
id: computing-software.cloud-infrastructure-engineering.gateway-api.gamma-mesh-routes-with-service-parentref
name: gamma-mesh-routes-with-service-parentref
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [gamma, mesh, service-mesh, parentref, httproute, east-west]
level: advanced
status: docs-checked
description: "Configure service mesh routing with GAMMA: a Route whose parentRef is a Service, how it matches traffic to that Service, and request rejection when no rule matches."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/gamma.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/mesh/mesh-overview.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
GAMMA (Gateway API for Mesh Management and Administration) extends Gateway API to east-west traffic. Instead of attaching a Route to a Gateway, you attach it to a **Service** using `parentRefs` with `kind: Service` and `group: core` (the page's example also sets `port: 80`). GAMMA has been in the Standard Channel since v1.1.0 and is considered GA. A mesh does not use the Gateway and GatewayClass resources, because there is typically only one mesh active in a cluster.

Behaviour:

- The Route holds configuration meant to apply to any traffic directed to that Service. Which Routes attach to a Service is controlled by the Routes themselves (working with Kubernetes RBAC).
- Request flow: the mesh data plane intercepts a request to the Service and locates the Routes associated with it. With no Routes, the request is always allowed and proceeds per the mesh's default behaviour. With Routes, the `backendRefs` of the highest-priority matching Route select the destination workload.
- If one or more Routes are attached to a Service and the request matches none of them, the request is **rejected**. A catch-all rule is therefore a sensible way to keep serving unmatched traffic (a suggestion derived from the rejection rule).
- The data plane most likely uses endpoint routing but may use Service routing.

Compare with Gateway attach: a Gateway Route accepts traffic into the cluster at a listener, while a Service-parented Route modifies how in-cluster callers reach a Service.

GAMMA's stated goal is minimal changes to Gateway API while preserving its role-oriented nature.

## Checked

2026-11-08. Read in full: the Mesh overview and GAMMA Initiative pages (raw markdown on GitHub). Confirmed: GAMMA name and purpose, east-west scope, Standard Channel since v1.1.0, Route parentRef of kind Service with group core, the three-step request flow, rejection of unmatched requests when Routes are attached, default behaviour when none are, and Gateway/GatewayClass not used in a mesh. Removed: the lists of supported fields and Route kinds, mixing mesh with edge Gateways, and the conformance report pointer, none of which are on the pages. The catch-all suggestion is derived, not quoted.

Method: documentation only; no commands were run.
