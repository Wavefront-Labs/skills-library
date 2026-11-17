---
id: computing-software.software-engineering.scala.sc-repl-worksheets
name: sc-repl-worksheets
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-repl-worksheets, repl-worksheets]
level: intro
status: draft
description: "Explore code in the Scala REPL, Metals worksheets (.worksheet.sc) or Jupyter with Almond."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# REPL, Metals worksheets and Almond
- `scala-cli repl --dep org.typelevel::cats-core:x.y.z` starts a REPL with dependencies.
- Metals worksheets (`.worksheet.sc`) evaluate on save and show results inline.
- Almond is a Scala Jupyter kernel.
- Restart between runs; REPL state can mask compile errors in packages.
Verify: results in a worksheet match a compiled test.
