---
id: computing-software.cloud-infrastructure-engineering.gateway-api.httproute-timeouts-request-and-backend
name: httproute-timeouts-request-and-backend
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [httproute, timeouts, request-timeout, backendrequest, duration, httprouterequesttimeout]
level: practitioner
status: docs-checked
description: "Set HTTPRoute rule timeouts: request versus backendRequest, zero disables, minimum 1ms, backendRequest must not exceed request, and unset behaviour is implementation specific."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/http-timeouts.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/httproute.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`rules[].timeouts` (Standard channel since v1.2.0). Request timeout is the Extended feature `HTTPRouteRequestTimeout`; backend timeout is `HTTPRouteBackendTimeout`.

Two timeouts:

- `request`: time for the gateway to send a response to the client; intended to cover as much of the whole request/response transaction as possible (an implementation may start the clock after the full request stream is received).
- `backendRequest`: timeout for a single request from the gateway to a backend, from start of sending to full response received. Useful when the gateway retries.

Rules:

- If unspecified, timeout behaviour is implementation-specific.
- Type is Duration. `"0s"` MUST disable the timeout; a valid non-zero value MUST be at least `1ms`.
- `request` encompasses `backendRequest`, so `backendRequest` must not be greater than `request`.

```yaml
rules:
- matches:
  - path:
      type: PathPrefix
      value: /request-timeout
  backendRefs:
  - name: infra-backend-v1
    port: 8080
  timeouts:
    request: 500ms
```

A request on that path taking longer than 500 ms makes the gateway return a timeout error. Disable explicitly with `request: "0s"`.

Combined, the reference example sets `request: 10s` and `backendRequest: 2s`.

## Checked

2026-11-04. Confirmed on the Gateway API HTTP timeouts guide and HTTPRoute reference (http-timeouts.md, httproute.md): Standard channel since v1.2.0, request and backendRequest semantics, "0s" and 1ms rules, 500ms example, 10s/2s example; HTTPRouteBackendTimeout name from the retries guide. Removed the mesh consumer 100ms example (not on the fetched pages).

Method: documentation only; no commands were run.
