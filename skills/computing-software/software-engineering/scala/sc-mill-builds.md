---
id: computing-software.software-engineering.scala.sc-mill-builds
name: sc-mill-builds
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-mill, mill-builds]
level: advanced
status: draft
description: "Define modules and tasks in Mill and compare with sbt."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mill build.mill modules
- A `build.mill` (older `build.sc`) declares `object app extends ScalaModule { def scalaVersion = "3.3.x"; def ivyDeps = Agg(ivy"...") }`; the exact syntax differs by Mill version, so check the docs.
- Commands: `./mill app.compile`, `app.test`, `app.run`, `resolve __`, `show app.ivyDeps`.
- Cached tasks and parallel execution by default; `./mill -w app.test` watches.
- Use the `./mill` bootstrap script so contributors need no install.
Verify: `./mill app.test` from a clean clone.
