---
id: computing-software.software-engineering.concurrency.structured-concurrency-across-languages
name: structured-concurrency-across-languages
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, structured-concurrency-patterns, structured-concurrency, task-groups, cancellation, nurseries]
level: advanced
status: gated
description: "Apply structured concurrency in Python TaskGroup/Trio, Kotlin coroutineScope, Swift task groups, Java StructuredTaskScope and Go errgroup: scoped lifetimes and cancellation."
sources: ["https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/", "https://docs.python.org/3/library/asyncio-task.html#task-groups", "https://kotlinlang.org/docs/coroutines-basics.html#structured-concurrency", "https://openjdk.org/jeps/505"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured concurrency across languages

**Principle** (Nathaniel Smith, "go statement considered harmful"): concurrent tasks are started
inside a scope and the scope **does not exit until all of them finish**. Errors propagate to the
parent; if one child fails, siblings are cancelled. No orphaned background tasks, and stack-like
reasoning about lifetimes returns.

## By language
**Python 3.11+ asyncio**
```python
async with asyncio.TaskGroup() as tg:
    user = tg.create_task(fetch_user(uid))
    orders = tg.create_task(fetch_orders(uid))
# both done here; one failure cancels the other and raises ExceptionGroup (handle with except*)
# run on Python 3.14: the sibling saw CancelledError and `except* ValueError` caught an ExceptionGroup
```
Trio/AnyIO nurseries (`async with trio.open_nursery() as n: n.start_soon(...)`) are the origin.
Timeouts as scopes: `async with asyncio.timeout(2):` (raises `TimeoutError`; run). A Trio nursery exits only after its children finish (run with trio, `pip install trio`).

**Kotlin** (not run here (gated: unconfirmed, source is paywalled or blocked))
```kotlin
suspend fun load(uid: String) = coroutineScope {
    val user = async { fetchUser(uid) }
    val orders = async { fetchOrders(uid) }
    Profile(user.await(), orders.await())
}   // supervisorScope when children should fail independently
```
Avoid `GlobalScope`; use lifecycle scopes (`viewModelScope`, `lifecycleScope`).

**Swift** (not run here (gated: unconfirmed, source is paywalled or blocked)): `async let` and `withThrowingTaskGroup { group in group.addTask {...} }`; unstructured
`Task {}` only at boundaries.

**Java 21+ (preview: JEP 505, fifth preview, delivered in JDK 25; JEP 525, sixth preview, in JDK 26)**: `StructuredTaskScope` with virtual threads; `StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())` or `Joiner.anySuccessfulResultOrThrow()`, then `fork()` subtasks and `join()` (names from the JEP text; Java code not compiled here (gated: unconfirmed, source is paywalled or blocked)). Preview API
shapes changed between JDK releases; check your version.

**Go**: goroutines are unstructured; impose structure with `errgroup.WithContext`:
```go
g, ctx := errgroup.WithContext(ctx)
g.Go(func() error { return fetchUser(ctx, uid) })
g.Go(func() error { return fetchOrders(ctx, uid) })
if err := g.Wait(); err != nil { ... }        // first error cancels ctx for the others
```
`g.SetLimit(n)` bounds concurrency (run with golang.org/x/sync v0.24.0: first error `boom` cancelled the shared ctx for the sibling; `SetLimit(2)` over 6 tasks peaked at 2 running).

**C#/.NET** (not run here (gated: unconfirmed, source is paywalled or blocked)): no built-in scopes; approximate with `Task.WhenAll` plus a shared
`CancellationTokenSource` cancelled on first failure.

## Rules
- Pass cancellation (context/token/scope) into every child; children must check it.
- Fire-and-forget work goes to an explicitly long-lived scope (a supervisor/service-owned scope),
  never an implicit global.
- Handle grouped errors (`ExceptionGroup`, aggregated exceptions).
