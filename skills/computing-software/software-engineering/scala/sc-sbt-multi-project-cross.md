---
id: computing-software.software-engineering.scala.sc-sbt-multi-project-cross
name: sc-sbt-multi-project-cross
category: computing-software
field: software-engineering
product: scala
tags: [scala, sbt-multi-project-cross]
level: advanced
status: draft
description: "Structure sbt multi-module builds with lazy val projects, dependsOn/aggregate, crossScalaVersions and + commands."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sbt multi-project
- `lazy val core = project.in(file("core"))`; `lazy val app = project.dependsOn(core)`; root `.aggregate(core, app)`.
- Share settings with `ThisBuild / scalaVersion := "3.3.x"` (confirm current LTS) or a `commonSettings` Seq.
- Cross-build: `crossScalaVersions := Seq("2.13.x", "3.3.x")` then `sbt +test`.
- `sbt "core/test"` runs one module; `sbt ~compile` watches.
Verify: `sbt projects` lists all modules.
