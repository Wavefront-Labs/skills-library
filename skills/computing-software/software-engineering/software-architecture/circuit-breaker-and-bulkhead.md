---
id: computing-software.software-engineering.software-architecture.circuit-breaker-and-bulkhead
name: circuit-breaker-and-bulkhead
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, resilience, circuit-breaker, bulkhead, timeouts, resilience4j, polly, fault-tolerance]
level: practitioner
status: draft
description: "Protect services from failing dependencies with timeouts, circuit breakers and bulkheads: states and thresholds, Resilience4j/Polly config, fallbacks and monitoring."
sources:
  - https://martinfowler.com/bliki/CircuitBreaker.html
  - https://resilience4j.readme.io/docs/circuitbreaker
  - https://www.pollydocs.org/strategies/circuit-breaker.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Circuit breakers and bulkheads

A slow or failing dependency can exhaust your threads, connections, and memory, spreading the outage (cascading failure). Three tools, applied together:

## 1. Timeouts (always first)
Every remote call needs a timeout shorter than the caller's own deadline. No timeout = a hung dependency hangs you. Set connect and read timeouts separately; propagate deadlines (gRPC deadlines, `context.WithTimeout`).

## 2. Circuit breaker
States:
- **Closed:** calls flow; failures counted in a sliding window.
- **Open:** after the failure rate crosses the threshold, calls fail fast immediately (no network call) for a wait duration.
- **Half-open:** after the wait, allow a few trial calls; success closes the circuit, failure reopens it.

Resilience4j (Spring Boot `application.yml`):
```yaml
resilience4j.circuitbreaker.instances.payments:
  slidingWindowType: COUNT_BASED
  slidingWindowSize: 50
  minimumNumberOfCalls: 20          # do not trip on 2 failures out of 3 at startup
  failureRateThreshold: 50          # percent
  slowCallDurationThreshold: 2s
  slowCallRateThreshold: 80         # slow calls count as failures
  waitDurationInOpenState: 30s
  permittedNumberOfCallsInHalfOpenState: 5
  ignoreExceptions: [com.shop.ValidationException]   # 4xx are not dependency failures
```
Polly v8 (.NET): `new ResiliencePipelineBuilder().AddTimeout(TimeSpan.FromSeconds(2)).AddCircuitBreaker(new() { FailureRatio = 0.5, MinimumThroughput = 20, SamplingDuration = TimeSpan.FromSeconds(30), BreakDuration = TimeSpan.FromSeconds(30) })`. Go: `sony/gobreaker`. Service mesh: Istio `outlierDetection`, Envoy circuit breaking.

## 3. Bulkhead
Isolate resources per dependency so one cannot consume them all: separate thread pools or semaphores (Resilience4j `Bulkhead`/`ThreadPoolBulkhead`, Polly `AddConcurrencyLimiter`), separate connection pools, separate service instances for critical vs batch traffic.

## Fallbacks
When open: return cached data, a default, a degraded response ("recommendations unavailable"), or fail fast with a clear error (503 + Retry-After). Never a fallback that silently corrupts data (pretending a payment succeeded).

## Combining with retries
Order (outer to inner): bulkhead -> timeout (overall) -> retry (with backoff and jitter, few attempts, only idempotent operations) -> circuit breaker -> per-attempt timeout -> call. Retries without a breaker amplify load on a struggling dependency (retry storms).

## Verify
- [ ] Metrics/alerts on breaker state transitions (Resilience4j Micrometer metrics, Polly telemetry).
- [ ] Fault-injection test (Toxiproxy, WireMock delays, chaos experiment): dependency latency spike leaves the caller's p99 bounded and other endpoints healthy.
