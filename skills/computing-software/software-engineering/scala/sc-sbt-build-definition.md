---
id: computing-software.software-engineering.scala.sc-sbt-build-definition
name: sc-sbt-build-definition
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-build-sbt, sbt-build-definition]
level: practitioner
status: draft
description: "Write build.sbt with settings, dependencies, cross-building and multi-project aggregation."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# build.sbt, settings, tasks and multi-project builds
- `ThisBuild / scalaVersion := "3.3.x"` (use your chosen version); `libraryDependencies += "org.typelevel" %% "cats-core" % "x.y.z"`; `%%` appends the Scala binary version, `%` does not, `%%%` is for Scala.js/Native.
- Projects: `lazy val core = project`, `lazy val app = project.dependsOn(core)`, root `.aggregate(core, app)`.
- `project/build.properties` pins `sbt.version`; `project/plugins.sbt` adds plugins (`addSbtPlugin`).
- `crossScalaVersions` with `+test` and `++3.3.x`; `sbt ~compile` triggers on change; `sbt shell`, `sbt "testOnly *Spec"`.
- `show dependencyTree` (sbt 1.4 or newer) inspects the graph; `evicted` shows conflicts.
Verify: `sbt clean test` from a clean clone.
