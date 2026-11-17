---
id: computing-software.software-engineering.scala.sc-promise-await-timeout
name: sc-promise-await-timeout
category: computing-software
field: software-engineering
product: scala
tags: [scala, promise-await-timeout]
level: practitioner
status: draft
description: "Complete Futures from callbacks with Promise, block safely with Await, and apply timeouts."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Promise and Await
- `val p = Promise[Int](); p.success(1); p.future` bridges callback APIs.
- `Await.result(f, 5.seconds)` blocks and throws `TimeoutException`; use only in main/tests, never in request threads.
- `Future.sequence`, `Future.traverse`, `recover`, `recoverWith`; there is no built-in timeout combinator, use a scheduler or effect library.
Verify: a never-completed promise throws after the timeout.
