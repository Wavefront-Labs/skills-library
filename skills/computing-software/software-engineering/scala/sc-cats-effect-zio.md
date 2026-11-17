---
id: computing-software.software-engineering.scala.sc-cats-effect-zio
name: sc-cats-effect-zio
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-effects, cats-effect-zio]
level: advanced
status: draft
description: "Understand when to use Cats Effect IO or ZIO, structured concurrency with fibres and Resource handling."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IO and ZIO effects, resources and fibres
- Effects describe computations lazily (`IO(println("x"))`) and run only at the edge: `IOApp` or `ZIOAppDefault`.
- `Resource.make(acquire)(release)` / `ZIO.acquireRelease` guarantee release on cancel and error.
- Parallelism: `parTraverse`, `IO.both`, `race` for Cats Effect; `ZIO.foreachPar`, `zipPar` for ZIO; fibres are cancelable lightweight threads.
- Do not call blocking code on the compute pool: `IO.blocking` or `ZIO.attemptBlocking`.
- Pick one effect system per application; mixing needs interop libraries.
Verify: cancel a running fibre in a test and assert finalisers run.
