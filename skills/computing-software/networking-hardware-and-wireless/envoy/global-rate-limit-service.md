---
id: computing-software.networking-hardware-and-wireless.envoy.global-rate-limit-service
name: global-rate-limit-service
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, rate-limit, ratelimit-service, descriptors, global-rate-limit, redis, rate-limits-actions, quota]
level: practitioner
status: docs-checked
description: "Use Envoy global rate limiting through the gRPC rate limit service with route descriptors, and know when it beats circuit breaking."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/other_features/global_rate_limiting.rst
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/rate_limit_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# global rate limit service
Distributed circuit breaking is not enough when many hosts fan in to a few low-latency hosts (a database): you cannot set a per-downstream limit tight enough yet permissive in normal operation. Global rate limiting fits. Envoy has two forms: per-connection or per-request checks against a gRPC rate limit service, and a quota based model with periodic load reports for fair sharing among many Envoys. The reference service is envoyproxy/ratelimit (Go, Redis backend). Features include a network-level filter (called per new connection), an HTTP filter (per request) and route-level descriptor actions.

```yaml
http_filters:
- name: envoy.filters.http.ratelimit
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.ratelimit.v3.RateLimit
    domain: edge
    rate_limit_service:
      grpc_service: { envoy_grpc: { cluster_name: ratelimit } }
      transport_api_version: V3
```
and on routes:
```yaml
rate_limits:
- actions:
  - source_cluster: {}
  - remote_address: {}
  - generic_key: { descriptor_value: some_value1 }
```
Descriptor actions in the docs examples: `source_cluster`, `remote_address`, `generic_key`, `request_headers`, and an `extension` computing a descriptor from an expression.

Gotchas: if the call to the rate limit service errors, `failure_mode_deny: true` returns a 500, otherwise the request is allowed through. Over-limit responses are 429 by default (`rate_limited_status`). The filter's stats are under `cluster.<route target cluster>.ratelimit.<optional stat prefix>.` (`ok`, `error`, `over_limit`, `shadow_over_limit`, `failure_mode_allowed`). The quota based form applies to HTTP requests only.

## Checked
2026-11-03. Confirmed against global_rate_limiting.rst, rate_limit_filter.rst and the ratelimit.proto reference. Removed or corrected: the added-latency claim and the ratelimit.* verify step (the stats live under cluster.<name>.ratelimit.).
Method: documentation only; no commands were run.
