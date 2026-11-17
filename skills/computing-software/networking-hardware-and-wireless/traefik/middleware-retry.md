---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-retry
name: middleware-retry
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, retry, resilience, attempts, initialinterval, idempotent, middleware]
level: practitioner
status: docs-checked
description: "Retry requests to a backend that does not reply with the retry middleware: attempts, backoff, status codes and non-idempotent methods."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/retry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware retry
The `retry` middleware retries a request a given number of times when the backend does not reply; once the server answers it stops retrying, regardless of the response status, unless `status` is configured. Options: `attempts` (required), `initialInterval` (first wait in an exponential backoff, the maximum interval is twice this; default 0 means retry immediately), `timeout` (how long the middleware may retry), `maxRequestBodyBytes` (default 2MB; -1 is unlimited and not recommended), `status` (status codes or ranges to retry on), `disableRetryOnNetworkError` (default false) and `retryNonIdempotentMethod` (default false; enables retry for `POST`, `LOCK`, `PATCH`).

```yaml
http:
  middlewares:
    test-retry:
      retry:
        attempts: 4
        initialInterval: 100ms
```
Gotchas: if `disableRetryOnNetworkError` is `true` you must also define `status`, otherwise the middleware raises a configuration error. Retrying non-idempotent methods can repeat side effects, so leave `retryNonIdempotentMethod` off unless the endpoint is safe.

## Checked
2026-11-03. Confirmed against the Traefik retry reference page (docs/content/reference/routing-configuration/http/middlewares/retry.md): options, defaults, backoff rule, status and disableRetryOnNetworkError rule, non-idempotent methods. Removed: "larger bodies are not retried", the multi-server remark, the `filters.retryAttempts` Verify step, and the "availability depends on version" hedge.
Method: documentation only; no commands were run.
