---
id: computing-software.software-engineering.scala.sc-java-collection-conversion
name: sc-java-collection-conversion
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-collections, java-collection-conversion]
level: practitioner
status: draft
description: "Convert between Java and Scala collections with scala.jdk.CollectionConverters and watch for wrapper semantics."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Java collection interop
- `import scala.jdk.CollectionConverters.*` then `javaList.asScala`, `scalaSeq.asJava` (2.13 and Scala 3; `JavaConverters` is deprecated).
- `asScala` and `asJava` create wrappers, not copies; mutation through one is visible in the other; use `.toList` / `.toBuffer` to copy.
- `Option` and `java.util.Optional` convert with `scala.jdk.OptionConverters`.
Verify: mutate the Java list and observe the Scala wrapper.
