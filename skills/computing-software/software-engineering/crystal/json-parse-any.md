---
id: computing-software.software-engineering.crystal.json-parse-any
name: json-parse-any
category: computing-software
field: software-engineering
product: crystal
tags: [json-parse-any, json-yaml, json, json-any, json-parse, to-json, json-build, pull-parser, as-s, as-i, pretty-json, crystal]
level: practitioner
status: docs-checked
description: "Parse JSON to JSON::Any, access values with as_s/as_i and dig, build JSON with JSON.build and to_json, pretty print."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON parsing and generation

Goal: handle JSON dynamically.

```crystal
require "json"
j = JSON.parse(%({"a": {"b": [1, 2]}}))
j["a"]["b"][0].as_i          # 1
j.dig("a", "b", 1).as_i
j["x"]?                      # nil
{a: 1, b: [1, 2]}.to_json
JSON.build(indent: 2) { |b| b.object { b.field "a", 1 } }
```
- Accessors raise on wrong type: `as_s`, `as_i` (Int32), `as_i64`, `as_f` (Float64), `as_bool`, `as_a`, `as_h`, `as_nil`; the `?` variants such as `as_s?` return nil.
- Streaming: `JSON::PullParser` for big documents.
- `value.to_pretty_json` (indent defaults to two spaces) pretty-prints any serializable value.

Gotchas:
- `JSON::Any` stores integers as Int64 and floats as Float64 (`as_i` narrows to Int32).
- Missing key with `[]` raises KeyError.
- Invalid input raises `JSON::ParseException` with line/col.

Verify: round trip a document in a spec.

## Checked

Date 2026-11-03. Confirmed JSON::Any types (Nil, Bool, Int64, Float64, String, Array, Hash), [] and []? on String keys and Int indexes, dig and dig?, the as_* and as_*? accessors (as_i is Int32, as_i64 is Int64), to_pretty_json and JSON.build with indent and object/field in the JSON source. ParseException line and column come from the parser source.

Method: documentation only; no commands were run.
