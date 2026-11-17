---
id: computing-software.networking-hardware-and-wireless.traefik.middleware-circuitbreaker
name: middleware-circuitbreaker
category: computing-software
field: networking-hardware-and-wireless
product: traefik
tags: [networking-hardware-and-wireless, traefik, circuitbreaker, resilience, expression, fallbackduration, middleware]
level: practitioner
status: docs-checked
description: "Trip a circuit breaker on network error ratio, status ratio or latency with Traefik expressions, and know the closed, open and recovering states."
sources:
  - https://github.com/traefik/traefik/blob/master/docs/content/reference/routing-configuration/http/middlewares/circuitbreaker.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# middleware circuitbreaker
`circuitBreaker` opens when `expression` is true and then returns a fallback instead of calling the service. Options: `expression`, `checkPeriod` (default 100ms; interval between condition checks), `fallbackDuration` (default 10s; how long it waits before trying to recover), `recoveryDuration` (default 10s; how long it spends recovering) and `responseCode` (default 503, returned while open).

```yaml
http:
  middlewares:
    latency-check:
      circuitBreaker:
        expression: "LatencyAtQuantileMS(50.0) > 100"
```
Expression metrics: `NetworkErrorRatio()`, `ResponseCodeRatio(from, to, dividedByFrom, dividedByTo)`, `LatencyAtQuantileMS(quantile)` and `RequestThreshold()`. `ResponseCodeRatio(500, 600, 0, 600) > 0.25` means 5XX responses make up more than 25% of responses with a status from 0 to 5XX; `from` is inclusive, `to` is exclusive, and it returns 0 if the divisor sum is 0. Combine with `&&` and `||`; comparison operators are `>`, `>=`, `<`, `<=`, `==`, `!=`. Example: `ResponseCodeRatio(500, 600, 0, 600) > 0.30 && RequestThreshold() >= 20`.

States: Closed (only collects metrics, evaluates `expression` every `checkPeriod`), Open (fallback for `fallbackDuration`, then Recovering), Recovering (sends linearly increasing traffic for `recoveryDuration`; a failure re-opens it, a clean run closes it).

Gotcha: the quantile for `LatencyAtQuantileMS` must be a floating point number with the trailing `.0`.

## Checked
2026-11-03. Confirmed against the Traefik circuitBreaker reference page (docs/content/reference/routing-configuration/http/middlewares/circuitbreaker.md): options and defaults, metrics, ResponseCodeRatio semantics, operators, states, quantile format. Removed: per-router instance and "only observes what comes after it" claims (not on the page), the multi-metric example expression, and the invented Verify step.
Method: documentation only; no commands were run.
