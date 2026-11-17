---
id: computing-software.networking-hardware-and-wireless.envoy.fault-injection-filter
name: fault-injection-filter
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, fault, fault-injection, abort, delay, x-envoy-fault-abort-request, chaos, header-abort]
level: practitioner
status: docs-checked
description: "Inject delays and aborts with the Envoy fault filter, scope it by cluster or headers, and let callers control faults via x-envoy-fault headers."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/fault_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fault injection filter
The fault filter tests resiliency by injecting delays and aborts with user-defined error codes. Faults can be limited to a destination upstream cluster and/or specific request headers. Only network-observable failures are emulated (no CPU or disk faults). The filter must be inserted before any other filter, including the router.

```yaml
http_filters:
- name: envoy.filters.http.fault
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.fault.v3.HTTPFault
    max_active_faults: 100
    abort:
      header_abort: {}
      percentage:
        numerator: 100
    delay:
      header_delay: {}
      percentage:
        numerator: 100
    response_rate_limit:
      header_limit: {}
      percentage:
        numerator: 100
```
Callers can drive faults with headers when `header_abort`, `header_delay` or `header_limit` is configured (the example above enables all three): `x-envoy-fault-abort-request` (HTTP status in [200, 600)), `x-envoy-fault-abort-grpc-request`, `x-envoy-fault-abort-request-percentage`, `x-envoy-fault-delay-request`, `x-envoy-fault-delay-request-percentage`, `x-envoy-fault-throughput-response` and its percentage.

Runtime keys such as `fault.http.abort.abort_percent`, `fault.http.abort.http_status` and `fault.http.abort.grpc_status` override config; the abort percent defaults to 0 if the config has no `abort` block.

Gotchas: header control is inherently dangerous if exposed to untrusted clients; the docs suggest `max_active_faults` to cap concurrent faults. If a header appears more than once only the first value is used. Counters live under `http.<stat_prefix>.fault.` (`delays_injected`, `aborts_injected`, `response_rl_injected`, `faults_overflow`, gauge `active_faults`).

## Checked
2026-11-03. Confirmed against fault_filter.rst and the fault.proto reference. Removed or corrected: the delay/abort/upstream_cluster example (not on the pages read; replaced by the documented header-control example) and the invented verify step.
Method: documentation only; no commands were run.
