---
id: computing-software.cloud-infrastructure-engineering.gateway-api.route-types-and-discriminators
name: route-types-and-discriminators
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [route-types, httproute, grpcroute, tlsroute, tcproute, udproute, routing-discriminator]
level: practitioner
status: docs-checked
description: "Choose between HTTPRoute, GRPCRoute, TLSRoute, TCPRoute and UDPRoute using protocol, routing discriminator, listener TLS support and the one-route-per-listener limit for L4."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/api-overview.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/tcproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/udproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/tlsroute.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A **routing discriminator** is the information that lets multiple Routes share one Listener port.

| Route | Protocol | Discriminator | Listener TLS | Backend TLS |
|---|---|---|---|---|
| HTTPRoute | HTTP/HTTPS | anything in HTTP | Terminated only | BackendTLSPolicy |
| GRPCRoute | HTTP/HTTPS (HTTP/2) | anything in gRPC | Terminated only | BackendTLSPolicy (Extended) |
| TLSRoute | TLS | SNI / TLS properties | Passthrough or Terminate | BackendTLSPolicy (Extended, when Terminated) |
| TCPRoute | TCP | none | Passthrough or Terminate | BackendTLSPolicy (Extended, when Terminated) |
| UDPRoute | UDP | none | none | none |

Consequences:

- TCPRoute and UDPRoute carry only `parentRefs` and one rule with 1 to 16 `backendRefs`; no hostnames, matches or filters.
- With no discriminator, several L4 Routes on the same Listener are all `Accepted`, but only the oldest (by `creationTimestamp`, then `namespace/name`) receives traffic. Give each its own listener port.
- Gateways supporting GRPCRoute must support HTTP/2 without an initial upgrade from HTTP/1.
- TLSRoute `hostnames` is required, unlike HTTPRoute and GRPCRoute where it is optional.

Channel status: the overview page still labels TCPRoute/UDPRoute Experimental since v0.3.0, but the TCPRoute and UDPRoute reference pages state Standard channel since v1.6.0. TLSRoute is Standard since v1.5.0, GRPCRoute since v1.1.0.

## Checked

2026-11-04. Confirmed on the Gateway API API overview and the TCPRoute, UDPRoute and TLSRoute reference pages (api-overview.md, tcproute.md, udproute.md, tlsroute.md): comparison table, 1 to 16 backendRefs, oldest-route-wins behaviour, HTTP/2 requirement, TLSRoute required hostnames, channel wording disagreement. Removed the claim that L4 Routes are not accepted on HTTP/HTTPS listeners and the "check your release" tip (not on the pages).

Method: documentation only; no commands were run.
