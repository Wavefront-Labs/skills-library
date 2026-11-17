---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.retry-pattern
name: retry-pattern
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, retry-pattern, distributed-systems-design, retries-with-backoff, exponential-backoff, jitter, retry-budget, timeouts, deadline-propagation, transient-faults, retry-storm, retry-storm-antipattern]
level: practitioner
status: docs-checked
description: "Retry transient faults without causing retry storms: classify errors, capped exponential backoff with jitter, idempotency, retrying at one layer and a token-bucket retry limit."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/retry", "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/", "https://grpc.io/docs/guides/retry/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Retries with backoff and jitter

## Rules
1. **Pick a strategy per fault.** Cancel if the fault is not transient or unlikely to succeed on repeat;
   retry immediately for rare faults (a corrupted packet); retry after a delay for common connectivity or
   busy faults, spreading retries from many instances. Different services can have different policies.
2. **Client errors are not retried** with the same request (HTTP separates client and server errors), though
   eventual consistency blurs this: a client error can become a success as state propagates.
3. **Backoff**: wait between tries; exponential is common, capped to a maximum, and with a limited number of
   retries. Add **jitter** (randomness) so clients do not retry in synchronised waves; AWS also suggests
   jitter on timers and periodic jobs.
4. **Idempotency**: only retry operations that are idempotent or carry an idempotency token (the EC2
   `RunInstances` token is AWS's example). A timed-out call may have succeeded.
5. **Retry at one layer.** AWS's example: three retries at each layer of a five-deep stack multiplies load on
   the database 243x. Make lower layers fail fast and report to the layer with the retry policy.
6. **Limit retries locally with a token bucket**: retries proceed while tokens remain, then drop to a fixed
   rate. gRPC's `retryThrottling` (`maxTokens`, `tokenRatio`) pauses retries when the count falls below half
   of `maxTokens`; the AWS SDK has had this behaviour since 2016.
7. **Tune to the workload**: interactive paths fail fast with few retries and short delays; batch jobs can
   use more retries with exponentially increasing delay.
8. **Log** early failures as informational and only the final failed attempt as an error.

## gRPC policy knobs
`retryPolicy` with `maxAttempts`, `initialBackoff`, `maxBackoff`, `backoffMultiplier` and
`retryableStatusCodes`, configured per method. gRPC applies plus or minus 20% jitter to the backoff delay.

## Gotchas
- Many client libraries already retry (for example Entity Framework Core for database operations); check
  before wrapping your own retry around them.
- Retries are "selfish": under overload they add load and can delay recovery. After many failures stop and
  consider a circuit breaker.
- Retrying a timed-out write that actually succeeded produces duplicates.

## Verify
- [ ] Count calls during an injected failure burst: total load stays near normal, not multiplied.
- [ ] Logs show attempt numbers and final outcome.
- [ ] No retry wrapper on top of a client that already retries.

## Checked
2026-11-01. Confirmed against the Azure Retry pattern page, the AWS Builders' Library article and the gRPC
Retry guide. Removed: the specific HTTP status list, the p99.9 per-attempt timeout rule, the full-jitter
formula and example numbers, the 10% budget, Envoy `retry_budget`, AWS SDK mode names and attempt counts,
the Azure and Google SDK claims, and the `X-Request-Deadline` header, none of which those pages state.
Method: documentation only; no commands were run.
