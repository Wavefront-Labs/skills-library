---
id: computing-software.networking-hardware-and-wireless.envoy.router-retries-and-timeouts
name: router-retries-and-timeouts
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, retry-policy, retry-on, x-envoy-retry-on, x-envoy-max-retries, per-try-timeout, backoff, timeouts]
level: practitioner
status: docs-checked
description: "Configure Envoy retry policies and timeouts: retry-on conditions, jittered back-off, per-try timeout and why the route timeout includes retries."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_filters/router_filter.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# router retries and timeouts
Retries are off unless a route or virtual host `retry_policy` exists or the caller sends `x-envoy-retry-on` / `x-envoy-retry-grpc-on`. Default is 1 retry; override with `num_retries` or `x-envoy-max-retries` (the header wins).

```yaml
route:
  cluster: backend
  timeout: 3s
  retry_policy:
    retry_on: "gateway-error,connect-failure,refused-stream"
    num_retries: 2
    per_try_timeout: 1s
```
Policies (comma-separated): `5xx` (includes connect-failure and refused-stream), `gateway-error` (502, 503, 504 or no response), `reset`, `reset-before-request`, `connect-failure`, `envoy-ratelimited`, `retriable-4xx` (only 409), `refused-stream`, `retriable-status-codes`, `retriable-headers`.

Facts from the docs:
- The route timeout (`timeout`, `x-envoy-upstream-rq-timeout-ms`, or `grpc-timeout` with `max_grpc_timeout`) includes all retries. With 3s total and a first attempt taking 2.7s, the retry has 0.3s. This avoids retry/timeout explosion.
- A request that exceeds the overall timeout (504) is not retried; use `per_try_timeout` (or `x-envoy-upstream-rq-per-try-timeout-ms`) to retry slow attempts.
- Back-off is fully jittered exponential, base 25 ms, capped at 10x base (250 ms); runtime key `upstream.base_retry_backoff_ms` changes the base. A rate-limited back-off can honour `Retry-After` or `X-RateLimit-Reset`.

Gotcha: `retriable-4xx` (409) can loop on optimistic-locking conflicts. Verify with `cluster.<name>.upstream_rq_retry` and `upstream_rq_retry_success` stats.

## Checked

2026-11-03. Confirmed against: router_filter.rst (default one retry, header precedence, retry-on policies, 409 for retriable-4xx, 25 ms base and 10x cap, route timeout includes retries, 504 not retried). Removed or corrected: nothing.

Method: documentation only; no commands were run.
