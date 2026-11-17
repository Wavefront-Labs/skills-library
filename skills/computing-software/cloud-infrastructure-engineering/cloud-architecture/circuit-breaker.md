---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.circuit-breaker
name: circuit-breaker
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, resiliency-patterns, circuit-breaker, half-open, fail-fast, resilience4j, polly, envoy-outlier-detection, istio, fallback, cascading-failure]
level: practitioner
status: docs-checked
description: "Stop calling a failing dependency: closed/open/half-open states, Resilience4j settings and defaults, what counts as failure, fallbacks, monitoring and Envoy outlier detection."
sources: ["https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker", "https://resilience4j.readme.io/docs/circuitbreaker", "https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/outlier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Circuit breaker

## States (Azure pattern page)
- **Closed**: requests go through; the proxy counts recent failures over a time-based counter that resets
  periodically, so occasional failures do not trip it. Exceeding the threshold within the interval moves it
  to Open and starts a time-out timer.
- **Open**: calls fail immediately with an exception, or return a meaningful default value. When the timer
  expires it becomes Half-Open.
- **Half-Open**: a limited number of trial requests protect a recovering service from a flood. A specified
  number of consecutive successes closes the breaker; any failure re-opens it immediately.

## Resilience4j settings (defaults from its page)
| Property | Default |
|---|---|
| `slidingWindowType` | `COUNT_BASED` (or `TIME_BASED`; size then means seconds) |
| `slidingWindowSize` | 100 |
| `minimumNumberOfCalls` | 100 |
| `failureRateThreshold` | 50 (percent) |
| `slowCallRateThreshold` | 100 (percent) |
| `slowCallDurationThreshold` | 60000 ms |
| `waitDurationInOpenState` | 60000 ms |

- `minimumNumberOfCalls` is the number of calls required before the failure or slow-call rate is computed.
  Slow calls count towards the slow-call rate, which can also open the breaker.
- By default every exception counts as a failure; list the exceptions that count (`recordExceptions`/
  `recordFailurePredicate`) or ignore (`ignoreExceptions`) so unrelated errors do not trip it.
- While OPEN, calls are rejected with `CallNotPermittedException`; after the wait it becomes HALF_OPEN and
  permits a configurable `permittedNumberOfCallsInHalfOpenState` calls, rejecting others until they finish.
- Tune to the recovery pattern: staying Open too long raises exceptions after the fault is gone; switching to
  Half-Open too quickly makes the breaker fluctuate.

## Pattern variations (Azure page)
Increasing time-out timer, a periodic ping or health endpoint instead of a timer, a manual override for
administrators, replaying journaled failed requests, and default or cached responses while Open.

## Mesh alternative
Envoy outlier detection ejects individual hosts (settings include `outlier_detection.consecutive_5xx` and
`outlier_detection.max_ejection_percent`), and ejected hosts return after the ejection time. Envoy suggests
using it alongside active health checking. It acts per host, so it complements a breaker on the whole
dependency.

## Gotchas
- A breaker should expose clear observability of failed and successful requests; alert on state changes.
- Breakers shared across unrelated endpoints or shards can block healthy traffic: scope them to what fails
  together.

## Verify
- [ ] Inject errors or latency in the dependency: callers fail fast and threads do not pile up.
- [ ] Restore it: the breaker closes after Half-Open probes succeed.
- [ ] Breaker state is visible on a dashboard or alert.

## Checked
2026-11-01. Confirmed against the Azure Circuit Breaker pattern page, the Resilience4j CircuitBreaker page
(defaults, state transitions, exception handling) and the Envoy outlier detection page. Removed: the Polly
and Istio claims, the 20-100 call and 10-60 s window recommendations, the 3-10 half-open call range, the
4xx exclusion rule and the Resilience4j decorator ordering, none of which those pages state.
Method: documentation only; no commands were run.
