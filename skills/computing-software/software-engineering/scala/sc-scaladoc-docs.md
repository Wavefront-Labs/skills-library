---
id: computing-software.software-engineering.scala.sc-scaladoc-docs
name: sc-scaladoc-docs
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-scaladoc, scaladoc-docs]
level: practitioner
status: draft
description: "Document code with Scaladoc tags and generate site docs with sbt doc."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing Scaladoc and publishing API docs
- Comments `/** ... */` with `@param`, `@return`, `@throws`, `@see`, `[[link]]`; Scala 3 Scaladoc also reads Markdown.
- `sbt doc` produces API docs under `target/scala-*/api`.
- Set `apiURL` and `autoAPIMappings := true` so dependencies link to their docs.
- Warnings on invalid links appear in `sbt doc`; fix them to keep docs clean.
Verify: open `index.html` in the generated API directory.
