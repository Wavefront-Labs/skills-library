---
id: computing-software.software-engineering.java.resilience4j-retry-and-circuit-breaker
name: resilience4j-retry-and-circuit-breaker
category: computing-software
field: software-engineering
product: java
tags: [java, spring-messaging, resilience4j, circuit-breaker, retry, bulkhead, ratelimiter, spring-retry]
level: practitioner
status: docs-checked
description: "Protect Java service calls with Resilience4j: retry, circuit breaker sliding windows, bulkheads, fallback methods, aspect order and Spring Boot configuration."
sources: ["https://resilience4j.readme.io/docs/getting-started-3", "https://resilience4j.readme.io/docs/circuitbreaker", "https://resilience4j.readme.io/docs/retry", "https://resilience4j.readme.io/docs/bulkhead", "https://docs.spring.io/spring-framework/reference/core/resilience.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resilience4j retry and circuit breaker

As of Spring Framework 7.0 the core framework has its own `@Retryable` and `@ConcurrencyLimit` annotations (default: any exception retried, `maxRetries = 3` after the initial failure, 1 second delay, with `delay`, `jitter` and multiplier attributes). This skill covers Resilience4j.

## Spring Boot setup
The starter expects `spring-boot-starter-actuator` and `spring-boot-starter-aop` on the runtime classpath (plus `resilience4j-reactor` for WebFlux).
```
implementation "io.github.resilience4j:resilience4j-spring-boot3:${resilience4jVersion}"
implementation "org.springframework.boot:spring-boot-starter-actuator"
implementation "org.springframework.boot:spring-boot-starter-aop"
```
```yaml
resilience4j.circuitbreaker:
  instances:
    inventory:
      slidingWindowType: COUNT_BASED      # or TIME_BASED (window size then means seconds)
      slidingWindowSize: 20               # default 100
      minimumNumberOfCalls: 10            # default 100; no failure rate is computed below this
      failureRateThreshold: 50            # percent, default 50
      slowCallDurationThreshold: 2s       # default 60000 ms
      slowCallRateThreshold: 80           # percent, default 100
      waitDurationInOpenState: 30s        # default 60000 ms
      permittedNumberOfCallsInHalfOpenState: 3
      ignoreExceptions: [com.acme.BusinessRuleException]   # count as neither failure nor success
```
Retry config properties (Java builder names, same names as the Boot properties): `maxAttempts` (default 3, **including** the initial call), `waitDuration` (default 500 ms, fixed), `retryExceptions`, `ignoreExceptions`, `retryOnResultPredicate`, `failAfterMaxAttempts`. The wait is constant unless you set an `IntervalFunction`: the Java API offers `ofExponentialBackoff(...)` and `ofRandomized()`. Bulkhead: `maxConcurrentCalls` (default 25) and `maxWaitDuration` (default 0).

```java
@CircuitBreaker(name = "inventory", fallbackMethod = "stockFallback")
@Retry(name = "inventory")
public Stock stock(String sku) { return client.get(sku); }
private Stock stockFallback(String sku, Throwable t) { return Stock.unknown(sku); }
```
Fallback methods work like catch blocks: same class, same signature plus ONE exception parameter, and the closest-matching exception type is invoked. The fallback runs regardless of circuit breaker state. The `@Bulkhead` annotation defaults to the semaphore type; `type = Bulkhead.Type.THREADPOOL` switches to a thread pool.

## Rules
1. Retry only idempotent calls and only transient errors; use `ignoreExceptions` for validation or business failures.
2. Budget retries so layers do not multiply (3 x 3 x 3 attempts).
3. Default aspect order is Retry ( CircuitBreaker ( RateLimiter ( TimeLimiter ( Bulkhead ( Function ))))), so Retry wraps the breaker and each attempt is seen by it. To change it set `resilience4j.retry.retryAspectOrder`, `resilience4j.circuitbreaker.circuitBreakerAspectOrder` and the matching rate limiter, time limiter and bulkhead properties; the higher value is the higher priority (applied outermost). Or use functional chaining.
4. Fallbacks should degrade (cached or default data), not hide errors: log and count them.

## Gotchas
- The annotations are AOP aspects, so they apply only to calls through the Spring proxy.
- `CallNotPermittedException` is what an OPEN breaker throws (and HALF_OPEN rejects beyond the permitted calls); map it to a 503 in your handler.
- Per the circuit breaker page, an OPEN breaker moves to HALF_OPEN after the wait duration.

## Verify
A test forces failures and asserts the CLOSED -> OPEN -> HALF_OPEN transitions through `CircuitBreakerRegistry`.

## Checked
Confirmed on the cited Resilience4j pages: circuit breaker, retry and bulkhead property names and defaults, Spring Boot setup, fallback rules, aspect order and order properties; on the Spring Framework resilience page: `@Retryable` defaults from 7.0.
Removed (not on the cited pages): kebab-case Retry exponential-backoff property keys, the TimeLimiter and platform-thread claim, the Retry-After and 429 advice, health and Micrometer metric names.
Method: docs-only read of cited pages, 2026-11-08
