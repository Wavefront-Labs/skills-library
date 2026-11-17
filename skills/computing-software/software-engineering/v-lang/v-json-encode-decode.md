---
id: computing-software.software-engineering.v-lang.v-json-encode-decode
name: v-json-encode-decode
category: computing-software
field: software-engineering
product: v-lang
tags: [v-json-encode-decode, json-module, json, json.encode, json.decode, serialization, parse json, pretty print, encode_pretty, v-lang]
level: practitioner
status: draft
description: "Serialise structs and collections with json.encode, parse with json.decode(T, s)!, pretty print and handle errors."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# json.encode and json.decode

Goal: convert between V values and JSON.

- `import json`; `s := json.encode(user)`; pretty: `json.encode_pretty(user)`.
- Decode into a type: `u := json.decode(User, text)!`; arrays `json.decode([]User, text)!`; maps `json.decode(map[string]string, text)!`.
- Missing fields keep zero values; unknown JSON fields are ignored.
- Options: struct fields of `?T` decode null/missing to none.
- Nested structs, arrays, enums (as ints by default), time values (as unix ints; confirm).
- Untyped JSON: `import x.json2`; `raw := json2.raw_decode(text)!`; `m := raw.as_map()`; `m['k'].str()` (API in flux, confirm).

Gotchas:
- Decode errors tell the position loosely; validate required fields manually.
- Large ints beyond 2^53 decode properly to `i64` but not via json2 floats.
- json uses comptime: types must be known at compile time.

Verify: round trip a struct and assert equality.
