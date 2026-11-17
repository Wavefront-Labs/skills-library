---
id: computing-software.cloud-infrastructure-engineering.zot.http-timeouts-and-rate-limits
name: http-timeouts-and-rate-limits
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, rate-limiting, fail-delay, read-timeout, write-timeout, slow-client]
level: practitioner
status: docs-checked
description: "Harden Zot against abuse with auth fail delay, global and per-method rate limits, and read/write timeouts for the API and metrics servers."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/admin-guide/admin-configuration.md
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/security-posture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Failure delay: seconds to wait before reporting a denied authentication, slowing automated attacks.

```json
"http": { "auth": { "failDelay": 5 } }
```

Rate limiting under `http.ratelimit`:

```json
"ratelimit": { "rate": 10, "methods": [ { "method": "GET", "rate": 5 } ] }
```

- `rate`: global limit in API calls per second.
- `methods`: optional per-method overrides, each with `method` and `rate`.

Timeouts:
- `http.readTimeout` and `http.writeTimeout` for the API server; `extensions.metrics.prometheus.readTimeout` and `writeTimeout` for the metrics exporter.
- Defaults are 60s. They guard against slow-client and stalled-connection resource exhaustion.
- Raise them for large pushes or pulls over slow networks.
- Setting a value to `0` disables the timeout and increases exposure to stalled or abusive connections.

## Checked

failDelay, ratelimit and timeout sections confirmed.

Method: docs-checked 2026-11-09 against zot docs admin-guide/admin-configuration.md (failure delay, rate limiting) and articles/security-posture.md (timeouts).
