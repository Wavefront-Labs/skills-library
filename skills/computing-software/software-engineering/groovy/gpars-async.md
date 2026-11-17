---
id: computing-software.software-engineering.groovy.gpars-async
name: gpars-async
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, gpars-async]
level: advanced
status: draft
description: "Use CompletableFuture from Groovy closures, and pointers to GPars for dataflow, actors and fork-join."
sources:
  - https://groovy-lang.org/semantics.html
  - https://docs.groovy-lang.org/latest/html/gapi/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Async tasks and CompletableFuture
```groovy
import java.util.concurrent.CompletableFuture
def r = CompletableFuture.supplyAsync { 6 * 7 }.thenApply { it + 0 }.get()
assert r == 42
```
- Closures become `Supplier`/`Function` via SAM coercion.
- GPars (`@Grab('org.codehaus.gpars:gpars:...')`, version unconfirmed) provides `GParsPool.withPool { list.collectParallel { } }`, dataflow variables and actors; check it is maintained for your Groovy version before adopting.
- Prefer virtual threads on JDK 21+ via `Executors.newVirtualThreadPerTaskExecutor()` (Java API, usable from Groovy).

## Gotchas
- Exceptions in `supplyAsync` surface as `ExecutionException` on `get()`.
- Do not block ForkJoin common-pool threads with long IO.

## Self-check
Run the snippet.
