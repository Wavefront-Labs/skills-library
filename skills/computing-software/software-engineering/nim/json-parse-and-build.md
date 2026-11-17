---
id: computing-software.software-engineering.nim.json-parse-and-build
name: json-parse-and-build
category: computing-software
field: software-engineering
product: nim
tags: [json-parse-and-build, stdlib-json-and-data, json, parsejson, jsonnode, pretty, getstr, getint, kind, jsonparse, nim]
level: practitioner
status: docs-checked
description: "Parse JSON text, navigate JsonNode, build values with %* and serialize with pretty or $."
sources:
  - https://nim-lang.org/docs/json.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON: parse, query and construct with std/json

Goal: read and write JSON.

- `import std/json`; `let j = parseJson(text)`; `parseFile(path)`.
- Navigate: `j["user"]["name"].getStr()`, `getInt`, `getFloat`, `getBool`, `getElems`, `getFields`; safe: `j{"a","b"}` returns `nil` if a field is missing, and the `get` procs return a default (`getInt(n, default = 0)`) on nil or a wrong kind; `j.hasKey("x")`; check `j.kind == JObject`.
- Build: `let n = %* {"name": "x", "tags": ["a","b"], "n": 3}`; `%` converts basic values.
- Output: `$j` is compact, `j.pretty(indent=2)` is indented.
- Errors: malformed input raises `JsonParsingError`; `[]` on a missing key raises `KeyError`.

Gotchas:
- Numbers that do not fit `BiggestInt` are kept as a "raw number" `JString` and printed without quotes.
- `getInt` on the wrong kind silently returns the default.

Verify: roundtrip parseJson($j) equals j.

## Checked

2026-11-02. Confirmed against lib/pure/json.nim (procs, `{}` vs `[]`, `get*` defaults, `JsonParsingError`, `KeyError`, raw-number handling). Fixed: large integers are stored as raw-number strings, not 'lose precision'.
Method: documentation only; no commands were run.
