---
id: computing-software.software-engineering.scala.sc-scala-regex
name: sc-scala-regex
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-strings-regex, scala-regex]
level: practitioner
status: draft
description: "Use the Regex class with pattern matching extractors and Java regex semantics."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regex, pattern extraction and text processing
- `val Date = """(\d{4})-(\d{2})""".r`, then `s match { case Date(y, m) => ... }` requires the whole string to match (unanchored matching with `findFirstIn`, `findAllMatchIn`).
- `replaceAllIn(text, m => ...)`; quote replacement `$`/`\` with `Regex.quoteReplacement`.
- `split(",")` takes a regex string; `String.split` drops trailing empty strings.
- It is `java.util.regex` underneath, so Java syntax and flags apply.
Verify: unit-test anchors and empty matches.
