---
id: computing-software.software-engineering.scala.sc-scalafmt-scalafix
name: sc-scalafmt-scalafix
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-formatting-linting, scalafmt-scalafix]
level: practitioner
status: draft
description: "Format with Scalafmt, refactor with Scalafix and enable useful compiler warnings."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scalafmt, Scalafix and compiler lint flags
- `.scalafmt.conf` with `version = "x.y.z"` and `runner.dialect = scala3`; `sbt scalafmtCheckAll` in CI.
- Scalafix rules live in `.scalafix.conf` (`RemoveUnused`, `OrganizeImports`); run `sbt "scalafixAll --check"`; semantic rules need SemanticDB.
- Compiler flags: `-deprecation`, `-feature`, `-Wunused:all` and `-Wvalue-discard` (2.13/3.3), `-Xfatal-warnings` or `-Werror` in CI only.
- Style: names `camelCase`, types `PascalCase`, no `return` keyword, no `null`, avoid `var`.
Verify: CI runs check commands and fails on drift.
