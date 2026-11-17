---
id: computing-software.software-engineering.crystal.enum-conversion-serialization
name: enum-conversion-serialization
category: computing-software
field: software-engineering
product: crystal
tags: [enum-conversion-serialization, enums, enum-to-s, enum-json, enum-from-value, symbol-arg, enum-converter, to-i, crystal]
level: practitioner
status: draft
description: "Convert enums to and from strings, integers and JSON, including converters and symbol shorthand in arguments."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enum conversion and serialisation

Goal: persist enums safely.

- `to_i`/`value` for ints, `to_s` for the name, `to_s.underscore` for snake case; `Color.parse(str)` for names.
- JSON: enums serialise as integers by default via `JSON.mapping`/`JSON::Serializable`; use `@[JSON::Field(converter: Enum::ValueConverter(Color))]` or `String` converter variants (check the converter names in the API docs).
- Symbols auto-convert to enums at call sites: `paint(:red)` works when the parameter is typed `Color`.
- `Color.from_value?(n)` guards untrusted ints.

Gotchas:
- Renaming a member changes its string form; persist ints if names may change.
- Symbol shorthand only works when the parameter type is exactly the enum.
- Unknown names in JSON raise `JSON::ParseException`.

Verify: round-trip an enum through JSON in a spec.
