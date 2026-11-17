---
id: computing-software.software-engineering.groovy.toml-slurper
name: toml-slurper
category: computing-software
field: software-engineering
product: groovy
tags: [groovy, toml-slurper]
level: practitioner
status: docs-checked
description: "Parse TOML with TomlSlurper from the optional groovy-toml module: type mapping, null handling and date-time values returned as strings."
sources:
  - https://github.com/apache/groovy/blob/master/subprojects/groovy-toml/src/spec/doc/toml-userguide.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TomlSlurper
- `groovy-toml` is an optional module for converting between Groovy objects and TOML; its classes are in the `groovy.toml` package. Because it is optional, add the module to your build first.
- `TomlSlurper` parses TOML text or reader content into maps, lists and primitives. It has overloaded `parse` methods plus `parseText` for a String.
- Type mapping: string to `String`; number to `BigDecimal` or `Integer`; table/object to `LinkedHashMap`; array to `ArrayList`; booleans; `null` to Groovy `null`; offset/local date-time, local date and local time to `String` (a limitation of the underlying Jackson TOML support, for the untyped `parse`/`parseText` API).
- Results conform to GPath expressions, so they can be navigated like other slurper results.
- `TomlSlurper` parses TOML as defined by a TOML spec release candidate linked in the guide (v1.0.0-rc.3).

## Checked

2026-11-03. Confirmed against the TOML user guide (TomlSlurper, type table, date notes). Removed: the Groovy 4+ version claim, the claim that dates map to `java.time` types (the guide says `String`), `TomlBuilder` details, and the code snippet and self-check.

Method: documentation only; no commands were run.
