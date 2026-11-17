---
id: computing-software.software-engineering.d.d-json-build-and-serialize
name: d-json-build-and-serialize
category: computing-software
field: software-engineering
product: d
tags: [d-json-build-and-serialize, std-json, tojson, toprettystring, jsonvalue-build, json-serialize, json-output, jsonoptions, d]
level: practitioner
status: docs-checked
description: "Create JSON from D values with JSONValue constructors and assignments, append to arrays/objects, remove keys, and print with toString, toPrettyString and options."
sources:
  - https://dlang.org/phobos/std_json.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building JSONValue and toJSON / toPrettyString output

Goal: produce JSON text.

- Build: `JSONValue j = parseJSON("{}");` then assign members, for example `j["name"] = "Ada"; j["n"] = 3.5; j["ok"] = true;`. `JSONValue` has a templated constructor `this(T)(T arg)`.
- Arrays: `.array ~= JSONValue("D");` works on an array-typed value; objects are reached through `.object`.
- Output: `j.toString()`, `j.toPrettyString(JSONOptions)`, `toJSON(j, pretty, JSONOptions)`.
- `JSONOptions` members include `none`, `specialFloatLiterals`, `escapeNonAsciiChars`, `doNotEscapeSlashes` and `strictParsing` (see the page for the full list).
- `JSONType` values: `null_`, `string`, `integer`, `uinteger`, `float_`, `array`, `object`, `true_`, `false_`.
- Phobos has no automatic struct serialiser in `std.json`; iterate members with `__traits(allMembers, T)`.

Gotchas:
- JSON has no NaN or infinity literals; the `specialFloatLiterals` option controls how they are written (see the page).

Verify: unittest `assert(parseJSON(j.toString) == j);`

## Checked

2026-11-03. Confirmed against: std.json reference page (JSONValue, JSONOptions, toJSON, toPrettyString, parseJSON, `in` operator).

Removed because the pages read did not confirm it: third-party serialiser names (`asdf`, `mir-ion`, `jsonizer`, vibe.d), copy/`deepCopy` semantics, 17-digit float claim, NaN/Inf behaviour claim, `j.object.remove`, appender/`formattedWrite` streaming tip.

Method: documentation only; no commands were run.
