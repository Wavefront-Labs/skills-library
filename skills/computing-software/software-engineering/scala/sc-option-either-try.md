---
id: computing-software.software-engineering.scala.sc-option-either-try
name: sc-option-either-try
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-options-errors, option-either-try]
level: practitioner
status: gated
description: "Model absence and failure with Option, Either and Try and convert between them without throwing."
sources: ["https://docs.scala-lang.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Option, Either and Try
- `Option(x)` turns null into `None`; `getOrElse`, `map`, `flatMap`, `fold`, `orElse`; avoid `.get`. (gated: unconfirmed, source is paywalled or blocked)
- `Either[Err, A]` is right-biased since 2.12: `for { a <- e1; b <- e2 } yield a + b`; `Left` is the error.
- `Try { riskyCall() }` catches non-fatal exceptions only (not `OutOfMemoryError`, `InterruptedException`); `toEither`, `toOption`, `recover`.
- `scala.util.control.NonFatal` in `catch` blocks; `case NonFatal(e) =>`.
- Prefer a typed error ADT in `Either` over exceptions for expected failures.
Verify: test both the success and failure branches.

## Checked

Date: 2026-11-02. Gated: Scala docs not fetched; NonFatal exclusions and right-biased Either not confirmed.

Method: documentation only; no commands were run.
