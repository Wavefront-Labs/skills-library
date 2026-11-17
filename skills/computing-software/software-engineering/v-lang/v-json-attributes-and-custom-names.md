---
id: computing-software.software-engineering.v-lang.v-json-attributes-and-custom-names
name: v-json-attributes-and-custom-names
category: computing-software
field: software-engineering
product: v-lang
tags: [v-json-attributes-and-custom-names, json-module, json-attributes, json, skip, required, field-rename, snake-case, camelcase, v-lang]
level: practitioner
status: docs-checked
description: "Control JSON field mapping in V's json2 module with @[required], @[skip], @[json: '-'] and @[json: name] renames, and decode or encode with json2.decode and json2.encode."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON field attributes

Goal: control the JSON shape. The current V docs describe a pure-V `json2` module that uses compile-time reflection.

```v
import json2

struct User {
	name      string @[required]
	age       int
	foo       Foo    @[skip]
	last_name string @[json: lastName]
}
user := json2.decode[User](data) or { return }
```

- `@[required]`: decoding fails if the field is missing. A field that is not required and is missing gets its default (0, `''`).
- `@[skip]` skips a field. `@[json: '-']` makes only the JSON encoder skip it; `@[sql: '-']` makes only the SQL ORM skip it.
- `@[json: lastName]` names the field in JSON when it differs from the V name (the docs example writes the name unquoted).
- `json2.decode[T](data)` takes the target type as a generic argument and the JSON string; arrays work too (`json2.decode[[]Foo](s)!`).
- `json2.encode(value, escape_unicode: true)` encodes maps and structs; the docs show `{"name":"Pierre","score":1024}` for a struct. `json2` also supports anonymous struct fields for deeply nested JSON.
- V requires `snake_case` for field and variable names, so rename explicitly when the JSON uses camelCase.

Verify: encode a user and assert a skipped field is absent.

## Checked
2026-11-08. Checked against the JSON section of the V documentation (`doc/docs.md`). Removed (not in the docs): `@[omitempty]`, `@[raw]`, `@[json_as_number]`, custom `to_json`/`from_json` methods, the older bracket-attribute syntax note and the zero-value gotcha for skipped fields. The docs now use `json2` rather than `json`; the skill previously assumed the `json` module. Replaced landing-page sources with the raw docs file.
Method: documentation only; no commands were run.
