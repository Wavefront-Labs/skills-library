---
id: computing-software.software-engineering.java.structured-concurrency-scopes
name: structured-concurrency-scopes
category: computing-software
field: software-engineering
product: java
tags: [java, java-concurrency-core, structured-concurrency, structuredtaskscope, shutdownonfailure, jep-453, virtual-threads, preview-api]
level: advanced
status: docs-checked
description: "Fork subtasks in a StructuredTaskScope (preview API in Java 21), choose ShutdownOnFailure/ShutdownOnSuccess, join, and propagate cancellation without leaked threads."
sources: ["https://openjdk.org/jeps/453", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/StructuredTaskScope.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structured concurrency scopes

**Version note:** `StructuredTaskScope` is a **preview API** in Java 21 (JEP 453); compile with `javac --release 21 --enable-preview` and run with `java --enable-preview`. The API may change in later preview rounds; check the JEP for your JDK before copying code.

## Idea
Treat concurrent subtasks like a block of code: they start inside a scope and all finish (or are cancelled) before the scope exits, so no thread outlives its parent and errors propagate.

## Java 21 pattern: all must succeed
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    StructuredTaskScope.Subtask<User>  user  = scope.fork(() -> findUser(id));
    StructuredTaskScope.Subtask<Order> order = scope.fork(() -> findOrder(id));
    scope.join().throwIfFailed();            // wait for both; cancel the other on first failure
    return new Page(user.get(), order.get());   // get() only after join()
}
```
`ShutdownOnSuccess<T>` captures the first successful result and shuts the scope down, interrupting unfinished subtasks ("invoke any"):
```java
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<String>()) {
    mirrors.forEach(m -> scope.fork(() -> fetch(m)));
    return scope.join().result();
}
```
`ShutdownOnFailure` suits "invoke all": it captures the first failure and shuts down.

## Properties
- Each `fork` starts a new thread for the subtask, by default a virtual thread.
- `shutdown()` cancels unfinished subtasks by interrupting their threads, so tasks must respond to interruption; `close()` waits for threads that did not.
- `join` and `close` may only be invoked by the owner (the thread that created the scope); `close` throws `IllegalStateException` if the owner did not join after forking.
- Subtasks inherit `ScopedValue` bindings (JEP 446).

## Gotchas
- `Subtask.get()` before `join()` throws `IllegalStateException`.
- Do not share a scope across threads; only the owner joins and closes.
- A subtask that ignores interrupts keeps running until it finishes; `close()` waits for it.

## Verify
Test with one subtask throwing: assert the other is interrupted and `throwIfFailed` rethrows the cause.

## Checked
2026-11-09. Confirmed against JEP 453 and the Java 21 StructuredTaskScope API page: preview status and the --release 21 --enable-preview commands, fork default virtual threads, owner-only join/close, IllegalStateException on close without join and on get() before join, shutdown interrupting threads and close waiting, ShutdownOnSuccess/ShutdownOnFailure semantics, ScopedValue inheritance.
Removed: the JDK 25 `open(...)` joiner remark, the "Java 21-24" range, the quoted preview-disabled error text, the blocking-I/O cancellation claim, the CompletableFuture comparison, and the dev.java source (404).
Method: documentation only; no commands were run.
