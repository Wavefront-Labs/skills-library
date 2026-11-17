---
id: computing-software.software-engineering.nim.json-object-mapping
name: json-object-mapping
category: computing-software
field: software-engineering
product: nim
tags: [json-object-mapping, stdlib-json-and-data, json, to, jsonutils, fromjson, tojson, marshal, serialization, deserialization, nim]
level: advanced
status: docs-checked
description: "Deserialize into typed objects with to[T] and jsonutils fromJson/toJson, with hooks and Joptions for missing or extra keys."
sources:
  - https://nim-lang.org/docs/json.html
  - https://nim-lang.org/docs/jsonutils.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping JSON to Nim types: to, jsonutils, marshal

Goal: typed JSON round-trips.

- `let user = parseJson(s).to(User)` unmarshals a `JsonNode` into the object type.
- `std/jsonutils`: `toJson(x)` and `fromJson(result, node, opts)` ships hooks for sets, tables, string tables and `Option`, with `Joptions` such as `allowMissingKeys`, `allowExtraKeys`; custom hooks `toJsonHook` / `fromJsonHook` for special types.

Gotchas:
- Known limitations of `to`: heterogeneous arrays, sets in object variants and `not nil` annotations are not supported.

Verify: parse to User and `%*` back yields equal JSON.

## Checked

2026-11-03. Confirmed against the json and jsonutils pages: `to(node, T)` and its listed limitations, toJson, fromJson with Joptions allowMissingKeys/allowExtraKeys, toJsonHook/fromJsonHook hooks (sets, tables, StringTableRef, Option). Removed: std/marshal, variant-discriminator, field-renaming, third-party package, ref/nil and enum-parsing claims, and the missing-field KeyError claim (none confirmed on these pages).

Method: documentation only; no commands were run.
