---
id: computing-software.software-engineering.java.completablefuture-composition-and-error-handling
name: completablefuture-composition-and-error-handling
category: computing-software
field: software-engineering
product: java
tags: [java, completablefuture, async, concurrency, thencompose, allof]
level: practitioner
status: docs-checked
description: "Compose async Java work with CompletableFuture: supplyAsync with an executor, thenCompose/thenCombine/allOf, exception handling, timeouts and common pitfalls."
sources: ["https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CompletableFuture composition

## Start work on your own executor
```java
ExecutorService io = Executors.newFixedThreadPool(32);
CompletableFuture<User> u = CompletableFuture.supplyAsync(() -> repo.find(id), io);
```
Without an executor, async stages run on `ForkJoinPool.commonPool()`; do not block it with I/O.

## Compose
- `thenApply(f)`: map value. `thenCompose(f)`: flatMap when `f` returns a future (avoids nested futures).
- `thenCombine(other, bi)`: join two independent results.
- `allOf(f1, f2, ...)`: completes when all do; it returns `Void`, so read each future with `join()` after it completes. `anyOf` for first.
- `thenApplyAsync` / `...Async(..., executor)` move the callback to another thread; the plain versions run on the completing thread (or the caller if already done).

## Errors and timeouts
```java
supplier.exceptionally(ex -> fallback)                       // only on failure
        .handle((v, ex) -> ex == null ? v : fallback)        // both outcomes
        .whenComplete((v, ex) -> log(v, ex))                 // side effect, does not change result
        .orTimeout(2, TimeUnit.SECONDS)                      // fails with TimeoutException (Java 9)
        .completeOnTimeout(defaultValue, 2, TimeUnit.SECONDS);
```
Exceptions arrive wrapped in `CompletionException`; unwrap with `getCause()`. `join()` throws unchecked `CompletionException`; `get()` throws checked `ExecutionException`.

## Pitfalls
- Dropped futures swallow exceptions: always attach a terminal handler.
- `cancel(...)` is just `completeExceptionally(new CancellationException())`: the future has no control over the computation, so the running task is not interrupted.
- Blocking `join()` inside a pool task can starve the pool.
- Context (MDC, security, transactions) does not follow threads; propagate explicitly.
- On Java 21, virtual threads with plain blocking code are often simpler.

## Verify
Unit test: failing stage triggers the fallback; timeout test with a sleeping supplier completes within the limit.

## Checked

2026-11-02. Checked against the Java SE 21 CompletableFuture API page: default pool is `ForkJoinPool.commonPool()`, non-async dependents run on the completing thread or any caller of a completion method, `allOf` returns `CompletableFuture<Void>`, `orTimeout` completes exceptionally with `TimeoutException`, `completeOnTimeout`, `get()` throws `ExecutionException` while `join()` throws `CompletionException` (cause preserved), `handle`/`whenComplete` signatures. Fixed: cancellation wording made precise.

Method: documentation only; no commands were run.
