---
id: computing-software.software-engineering.scala.sc-futures-execution-context
name: sc-futures-execution-context
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-concurrency-futures, futures-execution-context]
level: practitioner
status: draft
description: "Compose Futures, choose an ExecutionContext and avoid blocking and starvation."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Future, ExecutionContext and Await
- `Future { work() }(using ec)`; `map`, `flatMap`, `recover`, `Future.sequence`, `Future.traverse`.
- Futures are eager and memoised: they start when created.
- The global EC is a fork-join pool sized to CPU count; blocking inside it needs `scala.concurrent.blocking { ... }` or a dedicated pool.
- `Await.result(f, 5.seconds)` only at program edges (main, tests).
- Run Futures in parallel by creating them first, then composing.
- Handle failures: an unobserved failed Future logs nothing.
Verify: test with timeouts and failing futures.
