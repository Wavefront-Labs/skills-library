---
id: computing-software.cloud-infrastructure-engineering.contour.contour-timeout-and-retry-policy
name: contour-timeout-and-retry-policy
category: computing-software
field: cloud-infrastructure-engineering
product: contour
tags: [timeoutpolicy, retrypolicy, response-timeout, idle-timeout, pertrytimeout, infinity]
level: practitioner
status: docs-checked
description: "HTTPProxy per-route timeoutPolicy (response, idle, idleConnection) and retryPolicy (count, perTryTimeout), defaults and duration syntax."
sources: ["https://github.com/projectcontour/contour/blob/main/site/content/docs/main/config/request-routing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTPProxy timeouts and retries

```yaml
routes:
- timeoutPolicy:
    response: 1s
    idle: 10s
    idleConnection: 60s
  retryPolicy:
    count: 3
    perTryTimeout: 150ms
  services: [{name: s1, port: 80}]
```

timeoutPolicy:
- `response`: time from complete client request processed to complete response; Envoy default 15s when unset.
- `idle`: no-activity timeout for one request/response or HTTP/2 stream; unset means no per-route idle timeout, but the connection-manager stream idle default of 5m still applies. It does not trigger between HTTP/1.1 requests.
- `idleConnection`: how long the proxy-to-upstream connection is kept with no active requests; Envoy default 1h.

Durations use Go syntax (`ns`, `us`, `ms`, `s`, `m`, `h`), e.g. `300ms`, `5s`, `1m`. `infinity` means no timeout. `0s` is treated as unset (Envoy default).

retryPolicy retries on 5xx responses or when an attempt exceeds `perTryTimeout`:
- `count`: maximum retries; defaults to 1; `-1` disables; `0` falls back to Envoy's default of 1.
- `perTryTimeout`: ignored if larger than the request timeout; if unspecified the request timeout is used.

Global defaults live in the Contour config file `timeouts` block.

## Checked

2026-11-04. Confirmed against the Contour request routing page (config/request-routing.md, Response Timeouts) and the configuration reference: the fields, defaults, flags and behaviours stated above. Removed: a sentence that route-level policy overrides the global timeouts (not stated on the pages).

Method: documentation only; no commands were run.
