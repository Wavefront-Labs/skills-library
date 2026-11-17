---
id: computing-software.web-development.micronaut.micronaut-retry-and-circuit-breaker
name: micronaut-retry-and-circuit-breaker
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, retry-advice, retryable, circuit-breaker, named-policies, programmatic-retry, resilience]
level: practitioner
status: docs-checked
description: "Add Micronaut @Retryable, @CircuitBreaker, programmatic retry operations, named retry policies and shared named circuit breakers with a rolling window."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/aop/retry.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: retry failing operations and stop hammering a failing dependency.

Since Micronaut 4.0 the retry module must be added as a dependency (`micronaut-retry`).

## @Retryable

```java
@Retryable
public List<Book> listBooks() { ... }
```

Default: three retries with a linear delay of 1s, 2s, 3s. Set `attempts` and `delay` (strings, so placeholders work); `multiplier` gives exponential delay:

```java
@Retryable(attempts = "5", delay = "2s")
public Book findBook(String title) { ... }

@Retryable(attempts = "${book.retry.attempts:3}")   // bound from book.retry.attempts when configured
public Book getBook(String title) { ... }
```

It also works on methods returning a `Publisher` (Reactor `Flux`, RxJava `Flowable`), applying the policy to the reactive type. On `@Factory` bean methods it applies to methods of the returned object, not to the factory method itself; to retry creation delegate it to another singleton with `@Retryable`.

## @CircuitBreaker

Variation of `@Retryable` with `reset` (how long the circuit stays open; default 20 seconds):

```java
@CircuitBreaker(reset = "30s")
public List<Book> findBooks() { ... }
```

After three retries it opens the circuit for 30 seconds and rethrows the original exception.

## Programmatic

When annotations are not desirable, create a typed policy once and derive reusable operations from an injected factory bean. The programmatic API uses typed values such as `Duration` and `int` instead of annotation strings. The page's examples cover:
- synchronous work: execute the supplier directly through `RetryOperations`;
- reactive work: pass a supplier so each retry attempt creates a fresh `Publisher`;
- asynchronous work: pass a supplier that creates a new `CompletionStage` for each attempt;
- circuit breakers: build a typed `CircuitBreakerPolicy` and use the injected `CircuitBreakerOperationsFactory`; the resulting `CircuitBreakerOperations` instance owns the shared breaker state.

Look up exact builder and method names in the API docs; the page embeds them from source files.

## Named retry policies (experimental)

```yaml
micronaut:
  retry:
    policies:
      books:
        attempts: 5
        delay: 200ms
        multiplier: 2
        max-delay: 10s
        jitter: 0.1
        includes: [java.io.IOException]
        excludes: [java.io.FileNotFoundException]
```

```java
@Retryable(name = "books")
public Book findBook(String title) { ... }

@Retryable(name = "books", attempts = "1")   // explicit member overrides only that setting
public Book getBook(String title) { ... }
```

`attempts: 5` means up to six calls. An unconfigured name fails each call with `IllegalStateException` (async/reactive methods return it failed); an invalid policy fails startup. `RetryRegistry.retry(name)` returns the `RetryOperations`.

## Named, shared circuit breakers

```yaml
micronaut:
  retry:
    circuit-breakers:
      inventory:
        reset: 30s
        attempts: 1
```

`@CircuitBreaker(name = "inventory")` methods share one circuit via `CircuitBreakerRegistry`; `registry.circuitBreaker("inventory")` gives operations and `registry.guard("shipping")` a `CircuitBreakerGuard`. A `CircuitBreakerGuard` is for callers that run each operation themselves and only report its outcome: `acquire()` fails fast with a `CircuitOpenException` while the circuit is open, `onSuccess()` and `onFailure(e)` report the outcome, and `release()` returns a permit whose operation ended without one (for example when cancelled). A guard never retries. Without further settings the first failure that survives the retries opens the circuit, and a half-open circuit closes on the first success and opens again on the first failure. The reset timeout and rolling window of a named circuit are those of its configuration, and a user that declares others fails. Users of one name must agree on reset/window settings or one fails with `IllegalStateException`.

### Rolling window

Setting any of these, on `@CircuitBreaker` or under `micronaut.retry.circuit-breakers.<name>` (kebab-case there), gives the circuit a rolling window of outcomes with the defaults of the others: `requestVolumeThreshold` (default 20, the number of last calls in the window), `failureRatio` (0.5, never opens before the window is full), `successThreshold` (1, trial calls of a half-open circuit: all must succeed to close it), `failOn` (every exception) and `skipOn` (none, counted as a success whatever `failOn` says). The page's example config sets `reset: 30s`, `request-volume-threshold: 4`, `failure-ratio: 0.5`, `success-threshold: 2` and `skip-on: [java.util.NoSuchElementException]`. `CircuitBreakerRegistry.findSnapshot(name)` returns state and counters.

## Events

Register `RetryEventListener` beans for `RetryEvent`, and listeners for `CircuitOpenEvent` / `CircuitClosedEvent`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against `retry.adoc`: dependency note, default retry behaviour, string members, reactive and factory notes, circuit breaker default reset of 20 seconds, named policy YAML and rules, named circuit breaker YAML, guard behaviour, rolling-window defaults and the events. Removed: the programmatic builder and factory method calls (including `resetTimeout`, `createRetryOperations`, `execute*`), the `Permit` type and the pricing annotation example, because the page embeds these only from source files that were not readable.
