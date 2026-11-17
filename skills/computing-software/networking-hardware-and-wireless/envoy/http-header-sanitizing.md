---
id: computing-software.networking-hardware-and-wireless.envoy.http-header-sanitizing
name: http-header-sanitizing
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, header-sanitizing, x-forwarded-for, use-remote-address, internal-address-config, x-envoy-headers, edge]
level: practitioner
status: docs-checked
description: "Understand which x-envoy and forwarding headers Envoy strips or rewrites on internal versus external requests and how use_remote_address decides it."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_conn_man/header_sanitizing.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http header sanitizing
For security, Envoy sanitizes a set of incoming headers depending on whether the request is internal or external. Internal versus external is determined from `x-forwarded-for`, and how that header is populated depends on the HCM `use_remote_address` setting; `internal_address_config` customizes the determination.

Headers that may be added, removed or modified include `x-envoy-decorator-operation`, `x-envoy-downstream-service-cluster`, `x-envoy-downstream-service-node`, `x-envoy-expected-rq-timeout-ms`, `x-envoy-external-address`, `x-envoy-force-trace`, `x-envoy-internal`, `x-envoy-ip-tags`, `x-envoy-max-retries`, `x-envoy-retry-grpc-on`, `x-envoy-retry-on`, `x-envoy-upstream-alt-stat-name`, `x-envoy-upstream-rq-per-try-timeout-ms`, `x-envoy-upstream-rq-timeout-alt-response`, `x-envoy-upstream-rq-timeout-ms`, `x-envoy-upstream-stream-duration-ms`, `x-forwarded-client-cert`, `x-forwarded-for`, `x-forwarded-proto`, `x-request-id` and `referer`.

Edge setting:
```yaml
# in the http_connection_manager typed_config
use_remote_address: true
```
Gotcha: the edge best-practices page says to set `use_remote_address` to true on an edge proxy to avoid consuming HTTP headers from external clients. The docs warn that how Envoy populates `x-forwarded-for` is complex, so read that section.

## Checked
2026-11-03. Confirmed against header_sanitizing.rst and best_practices/edge.rst. Removed or corrected: the forged-header claims and verify step; added x-envoy-upstream-stream-duration-ms to the list.
Method: documentation only; no commands were run.
