---
id: computing-software.software-engineering.d.d-json-parse-and-navigate
name: d-json-parse-and-navigate
category: computing-software
field: software-engineering
product: d
tags: [d-json-parse-and-navigate, std-json, parsejson, jsonvalue, jsontype, json-parse, object, array, integer, floating, str, d]
level: intro
status: docs-checked
description: "Parse text into std.json JSONValue, navigate objects and arrays, check JSONType, use .str .integer .floating .array .object, and handle missing keys and errors."
sources:
  - https://dlang.org/phobos/std_json.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# parseJSON, JSONValue navigation and type checks

Goal: read JSON documents.

```d
import std.json;
auto j = parseJSON(`{"name":"Ada","tags":["x","y"],"age":36}`);
string n = j["name"].str;
long age = j["age"].integer;
foreach (t; j["tags"].array) writeln(t.str);
if (auto p = "email" in j) writeln(p.str); else writeln("none");
```
- Types: `j.type` is a `JSONType`: `null_`, `string`, `integer`, `uinteger`, `float_`, `array`, `object`, `true_`, `false_`. Getters (`.str`, `.integer`, `.uinteger`, `.floating`, `.boolean`, `.array`, `.object`) throw `JSONException` on read when the type is wrong. `.floating` is a 64-bit double.
- Missing key: test with `"k" in j`, which returns a pointer to the value or null (it throws `JSONException` if `j` is not an object); `j["k"]` also throws `JSONException` if `j` is not an object.
- Convenience: `j["a"].get!int` converts to a D type (numbers, bool, string, `JSONValue[]`, `JSONValue[string]`); it throws `JSONException` if the type cannot hold the value and `ConvException` on integer overflow.
- `parseJSON(text, maxDepth, options)`: `maxDepth` of -1 disables depth checking; a deeper document throws `JSONException`. `JSONOptions` include `strictParsing` (RFC 8259 grammar), `specialFloatLiterals` (NaN/Inf as strings) and `preserveObjectOrder`; `doNotEscapeSlashes` and `escapeNonAsciiChars` affect output.
- Output: `toString`, `toPrettyString`; `toJSON` serializes objects in key-sorted order.
- Build values with `JSONValue(...)`, `JSONValue.emptyObject`, `JSONValue.emptyArray`, and `jj.object["k"] = ...`.

Gotchas:
- `JSONValue` is a DOM; the page warns it causes GC problems at hundreds of megabytes, so use a stream parser for huge inputs.
- `.object` and `.array` are `@system`; `objectNoRef` and `arrayNoRef` are the `@safe` by-value getters, and modifications to the returned copy of a null object or appended array are not visible in the `JSONValue`.

Verify: unittest round-trips a sample doc and asserts specific fields.

## Checked

2026-11-08. Confirmed against the std.json page: `parseJSON` signature and `maxDepth`, `JSONOptions`, `JSONType`, getters and their exceptions, `get!T`, `in` operator, `emptyObject`/`emptyArray`, `toString`/`toPrettyString`/`toJSON`, `objectNoRef`/`arrayNoRef`, the large-input warning.

Removed because the page did not confirm it: `j.object.get(...)` and `j.get("k", default)`, the claim about integers larger than long becoming `uinteger` or float, the duplicate-key claim, and third-party libraries (`mir-ion`, `asdf`, `jsonizer`). Corrected `doNotEscapeSlashes`/`escapeNonAsciiChars`, which are encoding options, not parse options. Replaced landing-page sources with the std.json page.

Method: documentation only; no commands were run.
