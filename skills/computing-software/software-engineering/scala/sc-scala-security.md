---
id: computing-software.software-engineering.scala.sc-scala-security
name: sc-scala-security
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-security, scala-security]
level: practitioner
status: draft
description: "Avoid injection and unsafe deserialization and audit dependencies in Scala projects."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Input handling, deserialization and dependency auditing in Scala
- Use parameterised queries (Doobie/Slick interpolation); never `s"..."` to build SQL.
- Avoid Java serialization (`ObjectInputStream`) on untrusted data; parse JSON into case classes.
- Audit dependencies in CI (for example sbt-dependency-check) and keep libraries current with Scala Steward.
- Keep secrets in environment variables or a secret manager, not in `application.conf`.
Verify: a dependency audit runs in CI.
