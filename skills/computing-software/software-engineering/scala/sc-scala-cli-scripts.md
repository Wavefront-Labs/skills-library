---
id: computing-software.software-engineering.scala.sc-scala-cli-scripts
name: sc-scala-cli-scripts
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-scala-cli, scala-cli-scripts]
level: intro
status: draft
description: "Run scripts and small projects with Scala CLI using using-directives, dependencies and packaging."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scala CLI scripts and directives
- `scala-cli run Hello.scala`, `scala-cli test .`, `scala-cli package --assembly`, `scala-cli repl`.
- Directives at the top of a file: `//> using scala 3.3.x`, `//> using dep "com.lihaoyi::os-lib:x.y.z"`, `//> using jvm 21`.
- `scala-cli setup-ide .` generates BSP config for Metals; `scala-cli fmt` runs Scalafmt.
- Scala CLI is the `scala` command in current Scala 3 installers (verify with `scala --version`).
Verify: run the script in a clean directory.
