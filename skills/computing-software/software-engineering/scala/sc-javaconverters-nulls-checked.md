---
id: computing-software.software-engineering.scala.sc-javaconverters-nulls-checked
name: sc-javaconverters-nulls-checked
category: computing-software
field: software-engineering
product: scala
tags: [scala, javaconverters-nulls-checked]
level: practitioner
status: draft
description: "Convert Java collections with CollectionConverters, wrap nullable returns in Option, and handle checked exceptions."
sources: ["https://docs.scala-lang.org/scala3/book/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Java interop details
- `import scala.jdk.CollectionConverters.*` then `javaList.asScala` and `scalaSeq.asJava` (wrappers, not copies).
- `Option(javaCall())` turns null into None; Java annotations (`@Nullable`) are not enforced.
- Scala has no checked exceptions; annotate `@throws[IOException]` if Java callers need to catch them.
- Use `@BeanProperty` for getters/setters and `@varargs` for Java varargs.
Verify: modify the Java list and see the Scala view change.
