---
id: computing-software.cloud-infrastructure-engineering.grafana-mimir.grafana-mimir-ingester-circuit-breakers
name: grafana-mimir-ingester-circuit-breakers
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-mimir
tags: [circuit-breaker, ingester, push-requests, read-requests, resilience]
level: advanced
status: docs-checked
description: "Describes Mimir ingester push and read circuit breakers, their open, half-open and closed states, and the flags and defaults that control them."
sources: ["https://grafana.com/docs/mimir/latest/configure/about-ingester-circuit-breakers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Ingester circuit breakers

Circuit breakers stop repeated attempts at an operation likely to fail, saving CPU. States: `closed` (normal), `open` (requests rejected immediately with a circuit breaker open error), `half-open` (after a timeout, a limited number of trial requests decide whether to close or reopen).

Ingester circuit breakers are an experimental feature. They protect the write and read paths from slow requests only, not from other ingester problems.

## Two breakers

- **Push**: a push request fails the condition if longer than the configured maximum push duration. Not available in ingest storage architecture.
- **Read**: a read fails if longer than the maximum read duration. To protect writes, an ingester first checks its push breaker and rejects reads if it is open.

## Enable and tune

```text
-ingester.push-circuit-breaker.enabled=true
-ingester.read-circuit-breaker.enabled=true
```

Independent of each other. Defaults when enabled:

- Failure percentage measured over a moving window of `1m`; change with `-ingester.push-circuit-breaker.thresholding-period` and the read equivalent.
- Opens at 10% failing; change with `...failure-threshold-percentage`.
- Waits `10s` in open before half-open trials.

The wait is set with `-ingester.push-circuit-breaker.cooldown-period` and the read equivalent. The maximum request duration before a request counts as failing defaults to `2s` for push and `30s` for read, set with the `request-timeout` flags of each breaker.

## Checked

Confirmed the three states, the request flow, the experimental status, the push and read breaker conditions, the enable flags, the 1m window, the 10 percent threshold, the 10s wait and the flag names. Removed the closing advice on watching errors because the page does not state it. Added the cooldown and request timeout flags with defaults from the page.

Method: docs-checked 2026-11-09 against the raw grafana/mimir docs page about-ingester-circuit-breakers.md, read in full.
