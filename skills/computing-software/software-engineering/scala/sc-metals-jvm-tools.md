---
id: computing-software.software-engineering.scala.sc-metals-jvm-tools
name: sc-metals-jvm-tools
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-debugging-profiling, metals-jvm-tools]
level: practitioner
status: draft
description: "Debug Scala with Metals (DAP), the REPL and JVM tools such as jstack and Flight Recorder."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metals debugger, REPL and JVM profiling
- Metals provides LSP, DAP debugging and test explorer in VS Code, Neovim and others; it needs a BSP build (sbt, Mill, scala-cli).
- `sbt console` / `scala-cli repl` for experiments; `sbt -jvm-debug 5005` for remote debugging.
- `jstack <pid>`, `jcmd <pid> JFR.start`, async-profiler for CPU and allocation profiles.
- JVM flags via `.jvmopts` or `javaOptions in run`; `fork := true` for the run/test JVM.
Verify: set a breakpoint in a test and step.
