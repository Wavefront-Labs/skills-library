---
id: computing-software.software-engineering.software-architecture.retry-budgets-and-jitter
name: retry-budgets-and-jitter
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, resilience, retry-budget, jitter, exponential-backoff, retry-storms, timeouts]
level: advanced
status: verified
description: "Configure timeouts and retries that don't amplify outages: exponential backoff with full jitter, retry budgets, retry at one layer only, and idempotency."
sources: ["https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/", "https://sre.google/sre-book/handling-overload/", "https://linkerd.io/2/features/retries-and-timeouts/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts, retry budgets and jitter

## Backoff with jitter
Exponential backoff alone synchronises clients: they all retry at 100 ms, 200 ms, 400 ms in waves.
**Full jitter** (AWS Builders' Library):
```python
sleep = random.uniform(0, min(cap, base * 2 ** attempt))   # base=100ms, cap=10-20s
```
"Decorrelated jitter" (AWS blog: like full jitter, but the upper bound grows from the previous sleep, e.g. `min(cap, random.uniform(base, prev_sleep * 3))`) performs similarly; AWS calls the choice between them unclear and recommends jittered backoff as the standard for remote clients. Also
jitter periodic jobs and cache TTLs.

## Retry budgets
Per-request retry limits (3 attempts) still multiply load during an outage: if every layer of a
5-deep call chain retries 3 times, the bottom sees 3^5 = 243x (the AWS Builders' Library example reports a 243x load increase on the database).
- **Retry only at one layer** (usually the edge client or the immediate caller), not every hop.
- **Budget**: retries may add at most ~10-20% to normal traffic. Google SRE: at most 3 attempts per request, and a client retries only while retries are under 10% of its requests. Implementations: Linkerd ServiceProfile `retryBudget` (`retryRatio`, `minRetriesPerSecond`, `ttl`; ratio of retries to originals, extra per-second allowance, and counting window), gRPC `retryThrottling` (`maxTokens`, `tokenRatio`: each failed RPC removes 1 token, each success adds `tokenRatio`, no retries or hedges while tokens <= maxTokens/2), Finagle `RetryBudget` (no-arg defaults: ttl 10 s, 10 min retries/s, 20% ratio), Envoy `retry_budget` (circuit-breaker threshold: `budget_percent` default 20%, `min_retry_concurrency` default 3), or a token bucket (AWS describes limiting retries locally with a token bucket; the deposit/cost values are yours to tune, e.g. gRPC-style 0.1 per success, 1 per retry).
- Google SRE: servers can return "overloaded, don't retry" when their attempt-count histograms show many retries; callers must respect it.

## What to retry
- Only idempotent operations, or writes with idempotency keys.
- Transient errors: connect failures, 502/503/504, 429 (honour `Retry-After`), gRPC UNAVAILABLE.
- Never 4xx validation errors, auth failures, or after the overall deadline.

## Timeouts
Every call has one; retries fit inside the caller's deadline; per-attempt timeout from the dependency's latency percentile at an acceptable false-timeout rate (AWS example: 0.1% false timeouts -> p99.9). Hedged requests (a duplicate sent after a delay, typically near a high percentile of normal latency) cut tail latency on idempotent reads; hedging is also gated by gRPC retry throttling.

## Verify
Load test with a dependency failing 50%: total request rate to it must stay within budget (e.g.
<= 1.2x baseline) and recover cleanly when it heals, without a thundering herd.
