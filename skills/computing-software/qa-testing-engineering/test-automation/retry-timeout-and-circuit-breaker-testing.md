---
id: computing-software.qa-testing-engineering.test-automation.retry-timeout-and-circuit-breaker-testing
name: retry-timeout-and-circuit-breaker-testing
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [circuit-breaker-testing, retry-testing, timeout-testing, resilience4j, reliability-testing]
level: advanced
status: docs-checked
description: "Test resilience patterns: timeout budgets, retry counts, non-retryable errors, and circuit breaker closed, open and half-open transitions."
sources:
  - https://resilience4j.readme.io/docs/circuitbreaker
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing retries, timeouts and circuit breakers

**Goal:** prove resilience settings do what the design says, because misconfigured retries and breakers cause outages instead of preventing them.

## What the pattern docs define
- Microsoft: a circuit breaker blocks access to a remote service after failures reach a threshold instead of repeatedly retrying an operation likely to fail. Transient faults (overcommitted resources, slow networks, time-outs) typically correct themselves and suit the Retry pattern; longer faults should not be retried continually.
- States: Closed (requests pass; the proxy counts recent failures; when the count exceeds the threshold within a time period it goes Open and starts a time-out timer), Open (requests fail immediately with an exception), Half-Open (after the timer expires; a limited number of trial requests are allowed, which stops a recovering service being flooded).
- The Closed failure counter is time based and resets periodically, so occasional failures do not open the breaker. In Half-Open, the breaker closes after a specified number of consecutive successes; any failure sends it straight back to Open and resets the success counter.
- Resilience4j: states CLOSED, OPEN and HALF_OPEN, plus METRICS_ONLY, DISABLED and FORCED_OPEN. An OPEN breaker rejects calls with `CallNotPermittedException`. After the wait duration it moves to HALF_OPEN and permits a configurable number of calls; further calls are rejected until the permitted calls complete.
- Resilience4j settings worth pinning in a test: `failureRateThreshold` (default 50 percent), `slidingWindowType` (`COUNT_BASED` default or `TIME_BASED`), `slidingWindowSize` (default 100), `minimumNumberOfCalls` (default 100; with 10, nine failures will not open the breaker), `waitDurationInOpenState` (default 60000 ms), `permittedNumberOfCallsInHalfOpenState`, `recordExceptions` and `ignoreExceptions` (ignored exceptions count as neither success nor failure).
- Resilience4j emits `CircuitBreakerEvent`s (state transition, reset, success, recorded error, ignored error) that a registered consumer can assert on.

## Know the configuration
Write down per dependency: connect and read timeouts, total deadline, retry count, backoff, which errors are retryable, and the breaker settings above.

## Tests
Use a controllable stub and count the requests it receives.
- **Timeout:** stub delays beyond the read timeout; the caller fails at the timeout, not at the stub delay; total time with retries stays within the deadline.
- **Retry count:** stub always returns a retryable error; it receives exactly one initial request plus the configured retries.
- **Non-retryable:** errors the design excludes are not retried.
- **Success after retry:** failures then success returns success to the caller.
- **Idempotency:** retried writes do not duplicate side effects.
- **Breaker opens:** after the failure threshold with at least the minimum number of calls, calls fail fast with no stub hits (Open state), returning the fallback if one is configured.
- **Half-open:** after the wait duration only the permitted trial calls reach the stub; success closes the breaker, failure reopens it.
- **Ignored exceptions:** a business exception listed in `ignoreExceptions` does not move the failure rate.

## Gotchas
- Retries at several layers multiply (3 attempts at each of three layers is 27 calls to the dependency); test end to end.
- Tests with a controllable clock are faster than waiting real backoff time.

## Verify
For each dependency a test proves timeout, retry count, non-retry of excluded errors, breaker open, half-open and close, with request counts asserted at the stub.

## Checked
2026-11-09: checked against the Resilience4j CircuitBreaker page (states, defaults, half-open behaviour, exceptions, events) and the Microsoft Circuit Breaker pattern page (states and counters). Removed: the ISTQB CTAL-TTA source (certification overview page, no pattern content), WireMock, Toxiproxy and MockServer tool names, backoff multiplier and jitter details, the `resilience4j_circuitbreaker_state` Micrometer metric name, and the `getState()` Java snippet, none of which appear in the cited pages.

Method: documentation only; no commands were run.
