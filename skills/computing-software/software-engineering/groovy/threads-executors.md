---
id: computing-software.software-engineering.groovy.threads-executors
name: threads-executors
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, threads-executors, groovy-concurrency]
level: advanced
status: draft
description: "Start threads and executors from Groovy, use @Synchronized / read-write lock annotations and concurrent collections."
sources:
  - https://groovy-lang.org/semantics.html
  - https://docs.groovy-lang.org/latest/html/gapi/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Threads, executors and synchronized annotations
```groovy
import java.util.concurrent.*
def pool = Executors.newFixedThreadPool(4)
def f = pool.submit({ 21 * 2 } as Callable)
assert f.get() == 42
pool.shutdown()
Thread.start { println 'in thread' }
```
- Closures coerce to `Runnable`/`Callable`.
- `@Synchronized`, `@WithReadLock`, `@WithWriteLock` (groovy.transform) wrap methods in locks.
- Use `ConcurrentHashMap`, `AtomicInteger` rather than shared Groovy maps.
- Parallel collections and actors live in the separate GPars library (version/compat unconfirmed for current Groovy).

## Gotchas
- Scripts and `Binding` variables are not thread-safe.
- Always `shutdown()` executors or JVM may hang.

## Self-check
Run the snippet.
