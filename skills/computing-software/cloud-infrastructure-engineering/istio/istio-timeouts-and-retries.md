---
id: computing-software.cloud-infrastructure-engineering.istio.istio-timeouts-and-retries
name: istio-timeouts-and-retries
category: computing-software
field: cloud-infrastructure-engineering
product: istio
tags: [istio, timeouts-retries, retry-policy, request-timeout]
level: practitioner
status: docs-checked
description: "Configure per-route timeout and retry policy in a VirtualService, and know the documented defaults and how attempts interact with timeouts."
sources: ["https://istio.io/latest/docs/reference/config/networking/virtual-service/", "https://istio.io/latest/docs/tasks/traffic-management/fault-injection/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Timeouts and retries are HTTP route fields. Documented defaults: `timeout` is disabled, and the default cluster-wide retry policy is `attempts: 2` with `retryOn: "connect-failure,refused-stream,unavailable,cancelled"`. Set explicit values when you need bounded tail latency.

```yaml
http:
- route: [{destination: {host: ratings}}]
  timeout: 3s
  retries:
    attempts: 2
    perTryTimeout: 1s
    retryOn: gateway-error,connect-failure,refused-stream
```

How the fields interact (from the reference): `attempts` is the number of retries, so the maximum number of requests is 1 + attempts; `attempts: 0` disables retries. The interval between retries is set automatically (25ms base, tunable with `backoff`). When a route `timeout` or `perTryTimeout` is configured, the retries actually made also depend on them; the reference's example is attempts 3, backoff 2s and timeout 3s, which retries only once. `perTryTimeout` defaults to the route timeout, meaning no per-try timeout. Keep `timeout` at least as long as the attempts you intend to allow.

Gotcha: the reference notes timeouts and retries are not enabled when client-side fault injection is configured on the route, so do not use fault injection to test them on the same rule. The fault injection task also shows a caller with a hard-coded 3 s timeout plus one retry giving up after about 6 s regardless of the injected delay.

## Checked

2026-11-03. Confirmed against the VirtualService reference (HTTPRoute `timeout`, `retries` default policy, HTTPRetry `attempts`, `perTryTimeout`, `backoff`, `retryOn` example) and the Fault Injection task. Real error fixed: the draft said retries default to two on connect failures; the documented default `retryOn` list is longer. Removed: invented stats verify step, unsourced advice on POST retries, retry storms and gateway timeouts, and the unresolved "confirm" marker.
Method: documentation only; no commands were run.
