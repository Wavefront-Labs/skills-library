---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-buffering
name: middleware-buffering
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, buffering, request-body, response-body, streaming, middleware]
level: practitioner
status: docs-checked
description: "Buffer request and response bodies with the buffering middleware, with memory thresholds and streaming caveats."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/buffering.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware buffering
The `buffering` middleware reads the entire request into memory (possibly spilling large requests to disk) and rejects requests over a size limit, so services avoid large bodies such as `multipart/form-data`. Traefik can then send the request upstream with a fixed `Content-Length` instead of the original chunked body.

Options (all optional): `maxRequestBodyBytes` (default 0 = unlimited; over-limit requests get 413), `memRequestBodyBytes` (default 1048576, the threshold above which the request is buffered on disk), `maxResponseBodyBytes` (default 0 = unlimited; over-limit responses are replaced by a 500), `memResponseBodyBytes` (default 1048576), `retryExpression`, `disableRequestBuffer` and `disableResponseBuffer` (both default false).

```yaml
http:
  middlewares:
    limit:
      buffering:
        maxRequestBodyBytes: 2000000
        memRequestBodyBytes: 1000000
        maxResponseBodyBytes: 10000000
        memResponseBodyBytes: 1000000
```
Streaming: by default whole bodies are buffered, which is incompatible with Server-Sent Events, gRPC streaming and Kubernetes `watch` endpoints. Set `disableResponseBuffer: true` for them; `maxRequestBodyBytes` is still enforced on uploads. Disabling a buffer disables the matching size limit, and `retryExpression` cannot be used when either buffer is disabled. WebSocket connections are not affected.

`retryExpression` is a combination of `Attempts()`, `ResponseCode()` and `IsNetworkError()` with `&&` and `||`; at least one function is required.

## Checked
2026-11-03. Confirmed against the Traefik buffering reference page (docs/content/reference/routing-configuration/http/middlewares/buffering.md): every option, default, status code (413, 500), streaming guidance, limitations and retryExpression functions. Removed: "protects slow backends from slow clients and enables retries", the "confirm against your version" hedge on 413, and the invented Verify step.
Method: documentation only; no commands were run.
