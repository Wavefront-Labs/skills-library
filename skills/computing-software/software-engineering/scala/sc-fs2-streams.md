---
id: computing-software.software-engineering.scala.sc-fs2-streams
name: sc-fs2-streams
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-fs2, fs2-streams]
level: advanced
status: draft
description: "Process data with fs2 streams in IO, with chunking, concurrency combinators and resource safety."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fs2 Stream, pull-based streaming and resource safety
- `Stream.emits(List(1,2,3)).map(_ + 1).compile.toList` runs a pure stream; effects use `Stream.eval(IO(...))`.
- `evalMap`, `parEvalMap(n)`, `merge`, `groupWithin(n, d)` give concurrency and batching.
- `fs2.io.file.Files[IO].readUtf8Lines(path)` streams a file without loading it.
- Streams are lazy descriptions: `compile.drain` runs them; resources close on completion, error and cancel.
Verify: process a file larger than the heap.
