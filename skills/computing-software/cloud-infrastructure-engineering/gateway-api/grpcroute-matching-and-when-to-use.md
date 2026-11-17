---
id: computing-software.cloud-infrastructure-engineering.gateway-api.grpcroute-matching-and-when-to-use
name: grpcroute-matching-and-when-to-use
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [grpcroute, grpc, service-method-match, headers, routing]
level: practitioner
status: docs-checked
description: "Route gRPC with GRPCRoute: match on service and method, headers, weighted backends, and when HTTPRoute is enough instead."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/grpcroute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/grpc-routing.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/docs/concepts/traffic-matching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`GRPCRoute` (Standard channel since v1.1.0) routes gRPC requests from a Gateway listener to a Service. It attaches to a Gateway through `parentRefs`, can set optional `hostnames` (matched against the Host header before any rule is evaluated; IPs and ports are not allowed), and has `rules` made of `matches`, optional `filters`, optional `backendRefs` and an optional `name` (Experimental since v1.2.0). The target Gateway must allow GRPCRoutes from the route's namespace.

Matching:

- `matches[].method` selects a gRPC `service` and `method` (for example `service: com.example.User`, `method: Login`).
- `matches[].headers` matches request headers.
- Each entry in `matches` is independent: the rule matches if any single match is satisfied, while the conditions inside one match (method AND header) must all hold.
- With no matches specified, the rule matches every gRPC request.
- A route with only one match, such as one method, does not match RPCs of any other method.
- Only one Route rule may match each request when several GRPCRoutes attach to one Gateway; merging follows the same semantics as other Routes. In the guide, the most specific match wins (a request with header `env: canary` goes to the canary backend, otherwise to the default one).

Backends and filters: `backendRefs` accept `weight` for splitting (for example 90/10). With no `backendRefs` and no filter that sends a response, the gateway returns the gRPC code UNIMPLEMENTED. GRPCRoute reuses HTTPRoute filters where the functionality is identical. All core filters MUST be supported by an implementation that supports GRPCRoute, extended ones are encouraged, and implementation-specific ones carry no cross-implementation guarantee.

HTTPRoute or GRPCRoute:

- Prefer GRPCRoute when you want to match by service and method names instead of a URI path, need retries conditioned on gRPC status codes, or want gRPC-oriented metrics.
- HTTPRoute is enough for simple hostname or path based routing and load balancing; there you match a gRPC method as the path `/package.Service/Method`.
- Separate hostnames for gRPC and non-gRPC HTTP traffic are recommended. An implementation may reject a GRPCRoute or HTTPRoute whose hostnames intersect those of the other kind already attached to the same listener (Accepted condition False).
- To serve HTTP and gRPC on one hostname distinguished only by URI, when the implementation enforces that uniqueness, use HTTPRoute for both.
- Keep gRPC-specific policy (such as retries on gRPC status codes) in GRPCRoute, not HTTPRoute.

gRPC reflection (needed for tools such as grpcurl without local protobuf files) requires adding the reflection method to the GRPCRoute; enable it in production only after considering the security implications.

## Checked

2026-11-08. Read in full (GitHub markdown): the GRPCRoute reference, the gRPC routing guide and the traffic matching page. Confirmed: Standard channel since v1.1.0, name field Experimental since v1.2.0, match semantics, default match-all, UNIMPLEMENTED with no backendRefs, filter conformance levels, when-to-use guidance, cross-serving hostname rule, reflection note. Removed: the claim that a Gateway must treat gRPC and HTTP as distinct Route kinds, the claim that HTTPRoute offers HTTP-only features GRPCRoute lacks, the h2c appProtocol sentence and the claim that omitting service and method matches all traffic (none are stated in the sources). The example YAML files are included by Hugo shortcodes and were not visible, so no field spellings beyond the inline snippets are asserted.

Method: documentation only; no commands were run.
