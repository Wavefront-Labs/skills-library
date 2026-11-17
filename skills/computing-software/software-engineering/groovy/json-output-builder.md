---
id: computing-software.software-engineering.groovy.json-output-builder
name: json-output-builder
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, json-output-builder]
level: practitioner
status: docs-checked
description: "Serialize with JsonOutput.toJson and prettyPrint, build JSON with JsonBuilder and StreamingJsonBuilder, and customize output with JsonGenerator.Options."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-json/src/spec/doc/json-userguide.adoc
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-json/src/spec/doc/_json-builder.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JsonOutput and JsonBuilder
- `JsonOutput.toJson(...)` has overloads for primitives, maps, lists and also serializes POGOs (plain Groovy objects). The output is not pretty printed.
- `JsonOutput.prettyPrint(String)` formats any JSON string, not only the result of `toJson`.
- For control over the output, build a `JsonGenerator` with the `JsonGenerator.Options` builder (end with `build()`); a closure can be registered as a converter for a type and is applied to that type and its subtypes. The converter closure takes the object and optionally a second `String` parameter holding the key name.
- `JsonBuilder` creates JSON through builder syntax; pass a `JsonGenerator` when creating it to customize the output.
- `StreamingJsonBuilder` is the other builder; see the DSLs chapter.

## Checked

2026-11-03. Confirmed against the JSON user guide (JsonOutput, Customizing Output, Formatted Output) and the JsonBuilder section. Removed: code snippets and exact output strings, the memory claim about `StreamingJsonBuilder`, the specific option list, the claim about cyclic references, and the date-format claim.

Method: documentation only; no commands were run.
