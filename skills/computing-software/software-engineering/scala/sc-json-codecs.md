---
id: computing-software.software-engineering.scala.sc-json-codecs
name: sc-json-codecs
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-json-serialization, json-codecs]
level: practitioner
status: draft
description: "Encode and decode JSON with circe or upickle and handle optional fields and sealed traits."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# circe, upickle and jsoniter-scala
- circe: `import io.circe.generic.auto.*`, `import io.circe.syntax.*`, `person.asJson.noSpaces`, `decode[Person](str)` returns `Either[Error, Person]`.
- Sealed hierarchies need a discriminator strategy (`Configuration.default.withDiscriminator("type")` with generic-extras, or semiauto codecs).
- upickle: `read[Person](str)`, `write(p)`, via `ReadWriter.macroRW`.
- Optional fields: `Option[T]` decodes missing as `None`; use defaults deliberately.
- jsoniter-scala is the fastest, with a compile-time codec macro.
Verify: round-trip test with property-based inputs.
