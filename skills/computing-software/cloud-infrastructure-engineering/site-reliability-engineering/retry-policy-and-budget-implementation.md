---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.retry-policy-and-budget-implementation
name: retry-policy-and-budget-implementation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [retry-policy-implementation, retry-budget-config, retries, exponential-backoff, jitter, envoy-retry-budget, istio]
level: practitioner
status: docs-checked
description: "Implement retry policies with backoff, jitter, deadlines and retry budgets in code, Envoy retry_budget and Istio, so retries cannot amplify a cascade."
sources: ["https://sre.google/sre-book/addressing-cascading-failures/", "https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/cluster/v3/circuit_breaker.proto", "https://istio.io/latest/docs/reference/config/networking/virtual-service/", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retry policy and budget implementation

SRE Book retry rules (Addressing Cascading Failures): always use randomized exponential backoff; limit retries
per request and never retry indefinitely; consider a server-wide retry budget (the book's example is 60 retries
per minute in a process, after which the request just fails); decide whether a given level needs to retry at
all; separate retriable from non-retriable errors and return a specific status when overloaded so clients back
off. Do not retry permanent errors or malformed requests. Servers should also propagate deadlines rather than
inventing new ones.

## In application code (Go, illustrative)
```go
func callWithRetry(ctx context.Context, f func(context.Context) error) error {
    const maxAttempts = 3
    base, cap := 50*time.Millisecond, 1*time.Second
    var err error
    for a := 0; a < maxAttempts; a++ {
        if err = f(ctx); err == nil || !retriable(err) { return err }
        if !budget.TryRetry() { return err }                 // process-wide retry budget
        sleep := time.Duration(rand.Int63n(int64(min(cap, base<<a))))  // jitter
        if dl, ok := ctx.Deadline(); ok && time.Until(dl) < sleep { return err }
        select { case <-time.After(sleep): case <-ctx.Done(): return ctx.Err() }
    }
    return err
}
```
`budget` is whatever process-wide limiter you build (for example a counter allowing N retries per minute, as in
the SRE Book example). The attempt cap and base/cap durations are choices to tune, not documented defaults.

## Envoy retry budget
```yaml
circuit_breakers:
  thresholds:
  - priority: DEFAULT
    retry_budget:
      budget_percent: { value: 20.0 }
      min_retry_concurrency: 3
```
- `budget_percent` limits concurrent retries as a percentage of active requests plus active pending requests
  (25 percent of 100 active requests allows 25 active retries). Optional, defaults to 20 percent.
- `min_retry_concurrency` is the floor under the active-retry limit. Optional, defaults to 3.
- `budget_interval` optionally counts recently started requests too; default 0ms means only currently active and
  pending requests count.
- If `retry_budget` is set it overrides any configured `max_retries` circuit breaker (default 3 parallel
  retries), and remaining retry resources are not tracked.

## Istio VirtualService
```yaml
http:
- route: [{ destination: { host: orders } }]
  timeout: 2s
  retries: { attempts: 2, perTryTimeout: 500ms, retryOn: "connect-failure,refused-stream,unavailable" }
```
- `attempts` is the number of retries allowed; the maximum number of requests is 1 + `attempts`; 0 disables
  retries. With a route `timeout` or `perTryTimeout` set, the actual retries also depend on those values.
- `perTryTimeout` defaults to the route `timeout` (so effectively no per-try timeout).
- If `retryOn` is not specified it defaults to `connect-failure,refused-stream,unavailable,cancelled`. Status
  codes can be listed too (`"503,reset"`), but they match responses actually received: a reset connection is
  reported as 503 by Istio yet matches `reset`, not `503`.
- `backoff` sets the base interval of the exponential backoff; the default minimum is 25ms.
Set retries explicitly so the policy is visible and coordinated with app-level retries.

## Coordinating layers
Write down, per call path, which layer retries. The SRE Book warns that attempts multiply across layers: if the
backend, frontend and JavaScript layers each issue 3 retries (4 attempts), one user action can create 64 attempts
(4 to the power 3) on the database. If the mesh retries, the app should not (or vice versa).

## Gotchas
- Retrying on non-idempotent requests can duplicate side effects; use idempotency keys or restrict `retryOn` to
  connection-level failures such as `connect-failure` and `refused-stream`.
- `perTryTimeout` times attempts must fit within the overall timeout (the Istio `backoff` note shows how timeout
  and backoff cut the number of retries actually made).
- Graphs of retry rates help spot bad retry behaviour in an outage, but may look like a symptom rather than a
  compounding cause.
- Jitter is not only for retries: the AWS Builders' Library recommends adding jitter to timers and periodic
  jobs to spread out spikes.

## Verify
- [ ] Inventory of retry config per hop; multiplied attempts across layers computed.
- [ ] Overload test shows retries being refused by the budget instead of amplifying load.

## Checked

Checked 2026-11-09. Confirmed against the SRE Book Addressing Cascading Failures page (retry rules, 60 retries per minute example, 4 attempts cubed to 64, deadline propagation), the Envoy circuit_breaker proto page (RetryBudget fields, defaults, override of max_retries) and the Istio VirtualService reference (HTTPRetry fields and defaults). Removed: the Istio default of 2 retries, the 10 percent token-bucket budget, the Envoy route retry_policy block, retry metric names and the attempts-at-most-3 rule, none confirmed on a page read.

Method: docs-checked 2026-11-09 against the pages above, read in full from downloaded copies; no commands were run.
