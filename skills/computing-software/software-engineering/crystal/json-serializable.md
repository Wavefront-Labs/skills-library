---
id: computing-software.software-engineering.crystal.json-serializable
name: json-serializable
category: computing-software
field: software-engineering
product: crystal
tags: [json-serializable, json-yaml, json-field, mapping, deserialization, converter, emit-null, strict, use-json-discriminator, from-json, crystal]
level: practitioner
status: docs-checked
description: "Map JSON to typed classes with include JSON::Serializable, use JSON::Field for key, ignore, converter, emit_null and strict mode."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON::Serializable and JSON::Field

Goal: typed JSON models.

```crystal
class User
  include JSON::Serializable
  property id : Int64
  @[JSON::Field(key: "full_name")]
  property name : String
  property email : String?
  @[JSON::Field(ignore: true)]
  property cache : String?
  @[JSON::Field(converter: Time::EpochConverter)]
  property created : Time
end
u = User.from_json(str)
u.to_json
```
- `JSON::Field` options: `key`, `ignore`, `ignore_serialize`, `ignore_deserialize`, `emit_null`, `converter`, `root`, `presence`; class-level `@[JSON::Serializable::Options(emit_nulls: true)]`.
- `include JSON::Serializable::Strict` rejects unknown keys; `::Unmapped` collects extras in `json_unmapped`.
- Polymorphism: `use_json_discriminator` (see `JSON::Serializable.use_json_discriminator`).
- Other types: Array/Hash/NamedTuple/Enum/Time work out of the box (Time as RFC 3339).

Gotchas:
- A missing non-nilable key raises `JSON::ParseException` ("Missing json attribute").
- A property with a default value is optional.

Verify: spec on a payload missing a required key.

## Checked

Date 2026-11-03. Confirmed the JSON::Field properties (ignore, ignore_serialize, ignore_deserialize, key, root, converter, presence, emit_null), JSON::Serializable::Strict and Unmapped (json_unmapped), JSON::Serializable::Options emit_nulls, use_json_discriminator, default values making a property optional, and the 'Missing json attribute' JSON::ParseException in the JSON source. Removed the nilable option and JSON::SerializableError (neither exists in the source) and the JSON.mapping history claim.

Method: documentation only; no commands were run.
