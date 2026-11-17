---
id: computing-software.software-engineering.scala.sc-literals-string-interpolation
name: sc-literals-string-interpolation
category: computing-software
field: software-engineering
product: scala
tags: [scala, literals-string-interpolation]
level: practitioner
status: docs-checked
description: "Use the Scala s, f and raw string interpolators, multiline strings with stripMargin, and custom interpolators."
sources: ["https://docs.scala-lang.org/scala3/book/string-interpolation.html", "https://docs.scala-lang.org/scala3/book/first-look-at-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String interpolation
- `s"..."`, `f"..."` and `raw"..."` are the standard interpolators. `f` is type-safe (passing a double where an integer format is given is a compile error) and uses Java's string format utilities for the `%` formats; `raw"a\nb"` does not process escapes.
- Triple quotes allow multi-line strings and unescaped double quotes; put `|` in front of lines after the first and call `stripMargin`.
- There are no extractors by default for `f` and `raw`, so `case f"..."` and `case raw"..."` do not work.
- You can write your own interpolator on `StringContext`; the book shows a worked example.
Verify: evaluate each interpolator in the REPL.

## Checked

Date: 2026-11-02. Confirmed on the Scala 3 book pages String Interpolation and First Look at Types. Removed as not confirmed: the `$$` escape, the 3.14 example output, the exact extension signature.

Method: documentation only; no commands were run.
