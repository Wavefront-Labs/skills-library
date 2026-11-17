---
id: computing-software.cloud-infrastructure-engineering.gateway-api.resource-model-gatewayclass-gateway-routes
name: resource-model-gatewayclass-gateway-routes
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [resource-model, gatewayclass, gateway, httproute, api-group, concepts]
level: intro
status: docs-checked
description: "Gateway API resource model: GatewayClass (cluster-scoped), Gateway (listeners and addresses), Route types, and the request flow to a Service."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/introduction/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
All resources live in the `gateway.networking.k8s.io` API group as CRDs. Three object types make up the model:

- **GatewayClass**: a set of Gateways with common configuration and behaviour (Standard channel since v0.5.0). Cluster-scoped. Each class is handled by a single controller (a controller may handle many classes). At least one GatewayClass must exist for Gateways to work. Analogous to IngressClass and StorageClass.
- **Gateway** (Standard since v0.5.0): a request for a point where traffic is translated to Services. It binds one or more **Addresses** (usually IPs, sometimes DNS names such as AWS load balancers) to one or more **Listeners** (`port`, `protocol` and protocol-specific details). Listeners must be distinct, because any traffic must match only one Listener; non-distinct (Conflicted) Listeners make the whole Gateway invalid.
- **Routes**: protocol-specific rules mapping Gateway traffic to Services. As of v1 the docs list four Route types, HTTPRoute (Standard since v0.5.0), GRPCRoute (Standard since v1.1.0), TLSRoute (Standard since v1.5.0) and TCPRoute/UDPRoute (the API overview says Experimental since v0.3.0, while the TCP guide says TCPRoute is Standard since v1.6.0; check the release notes for your version); custom Route types are encouraged for other protocols.

Request flow for a reverse-proxy implementation:

1. Client requests `http://foo.example.com`.
2. DNS resolves to a Gateway address.
3. The proxy receives the request on a Listener and uses the Host header to match an HTTPRoute.
4. Optionally it matches on headers and path per the route's match rules.
5. Optionally it modifies the request (for example add or remove headers) per `filters`.
6. `backendRefs` choose the Service(s) or other objects to forward to.

A Gateway spec captures user intent and may omit addresses or TLS settings, which the controller managing the GatewayClass can supply; the GatewayClass and Gateway status show the result.

Extension points: `backendRefs` to objects other than Services, `HTTPRouteFilter`, and custom Route types that share `CommonRouteSpec` and `RouteStatus`.

For service mesh (GAMMA, Standard since v1.1.0) the Gateway and GatewayClass are not used; Routes attach directly to Service resources.

## Checked

2026-11-08. Read in full (GitHub markdown): the API overview and the introduction page. Confirmed: API group, the three object types and their relationships, cluster scope, one controller per class, addresses and listeners, distinctiveness rule, Route types and their channels, request flow, extension points, GAMMA note. Removed: the claim that the resulting values are read from `Gateway.status` rather than `spec` as a rule (the docs only say the controller may fill in omitted settings and surface it in status).

Method: documentation only; no commands were run.
