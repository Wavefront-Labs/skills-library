---
id: computing-software.software-engineering.scala.sc-scala3-rewrite-flags
name: sc-scala3-rewrite-flags
category: computing-software
field: software-engineering
product: scala
tags: [scala, scala3-rewrite-flags]
level: advanced
status: docs-checked
description: "Move Scala 2.13 code to Scala 3 using -source:3.0-migration, -rewrite, cross-building and the TASTy reader."
sources: ["https://docs.scala-lang.org/scala3/guides/migration/syntax-rewriting.html", "https://docs.scala-lang.org/scala3/guides/migration/migrating-to-3-3.html", "https://docs.scala-lang.org/scala3/guides/migration/interoperability.html", "https://docs.scala-lang.org/scala3/guides/migration/incompat-dropped-features.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scala 3 rewrite flags
- Compile on 2.13 with `-Xsource:3` first; then `-source:3.0-migration -rewrite` rewrites some incompatibilities (dropped features among them).
- Syntax conversion is optional (the Scala 2 style stays valid in Scala 3). With `-rewrite`: `-new-syntax` (`if x then`, `while x do`, `for ... do`), `-old-syntax` (parentheses), `-indent` (significant indentation), `-no-indent` (braces).
- Run `-new-syntax` first: `-indent` keeps the braces around the generators of a `for` that uses the old syntax.
- Dependencies cross with `CrossVersion.for3Use2_13` (Scala 3 using a 2.13 library) and `CrossVersion.for2_13Use3` (the reverse).
- Dropped features to replace: symbol literals, procedure syntax, `do`-`while`, early initializers (trait parameters replace them).
Verify: the project compiles with the new flags.

## Checked

Date: 2026-11-02. Confirmed on the Syntax Rewriting, Migrating to Scala 3.3, Interoperability and Dropped Features migration pages. Removed as not confirmed: `-source:future` warning-free claim, implicit macros replacement, 'macros do not cross' wording beyond the macro page.

Method: documentation only; no commands were run.
