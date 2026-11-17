---
id: computing-software.software-engineering.scala.sc-java-interop
name: sc-java-interop
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-java-interop, java-interop]
level: practitioner
status: draft
description: "Use Java libraries from Scala and expose Scala APIs that are friendly to Java."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling Java from Scala and Scala from Java
- Null: Java methods return platform types; wrap with `Option(...)`; Scala 3 explicit nulls (`-Yexplicit-nulls`) makes them `T | Null`.
- Java generics wildcard: `java.util.List[? <: Number]` in Scala 3.
- Java varargs and SAM types accept Scala lambdas: `executor.submit(() => work())`.
- For Java callers, avoid implicits and default arguments in public APIs; use `@varargs`, `@static` and `@throws`; `scala.jdk.FunctionConverters` for functional interfaces.
- Scala traits with concrete members compile to interfaces with default methods (2.12 and newer).
Verify: call the API from a small Java test class.
