---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-retries-codes-attempts-backoff
name: httproute-retries-codes-attempts-backoff
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, retry, attempts, codes, backoff, httprouteretrycodes, resilience]
level: advanced
status: docs-checked
description: "Configure HTTPRoute retry: codes, attempts (default 1, 0 disables), connection errors, interaction with request and backendRequest timeouts, and backoff (implementation specific)."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-retries.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rules[].retry` is Standard channel since v1.7.0. Extended features: `HTTPRouteRetryCodes` and `HTTPRouteRetryConnectionError`.

Fields:

- `codes`: HTTP status codes that trigger a retry. 500, 502, 503 and 504 are always supported; other codes vary by gateway.
- `attempts`: maximum retries beyond the initial request. `attempts: 2` allows up to three requests to the backend. `0` disables retries. Default `1` if unspecified.
- `backoff`: base interval before each retry (for example `100ms` or `1s`). Implementation-specific; typically exponential with jitter, may be capped. Unset means strategy and base are implementation-specific.

```yaml
rules:
- backendRefs:
  - name: backend-svc
    port: 8080
  retry:
    codes: [500, 503, 504]
    attempts: 2
```

Connection errors (disconnect, reset, timeout, TCP failure) are retried whenever `retry` is configured, even with no `codes`. The precise set varies by gateway. A rule with `attempts: 2` and no `codes` masks only network failures and returns backend status codes as-is.

Timeouts bound retries:

- `timeouts.request` covers the initial request and all retries; retries still running at expiry should be canceled.
- `timeouts.backendRequest` cancels any single attempt exceeding it.

Example bound: each attempt 500 ms, overall request 2 s, up to three retries.

## Checked

2026-11-04. Confirmed on the Gateway API HTTP retries guide (http-retries.md): Standard channel since v1.7.0, extended features, codes, attempts, connection errors, timeout interaction, backoff. Removed the idempotency and GRPCRoute tips (not on the page).

Method: documentation only; no commands were run.
