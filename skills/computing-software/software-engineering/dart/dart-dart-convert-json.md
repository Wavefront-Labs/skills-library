---
id: computing-software.software-engineering.dart.dart-dart-convert-json
name: dart-dart-convert-json
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-json-io, dart-convert-json]
level: practitioner
status: docs-checked
description: "Decode and encode JSON with dart:convert, destructure with map patterns, encode custom types and UTF-8 streams."
sources: ["https://dart.dev/libraries/dart-convert", "https://dart.dev/language/pattern-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jsonEncode, jsonDecode and typed models
- `import 'dart:convert';` then `jsonDecode(s)` turns a JSON string into Dart objects; the result is dynamic, so check or destructure it. A map pattern such as `if (data case {'user': [String name, int age]})` matches and binds. Matching a key that is missing from a map throws a `StateError`.
- `jsonEncode(obj)` encodes supported objects. For other objects either pass a second argument (a function returning something encodable) or omit it so the encoder calls the object's `toJson()`.
- `utf8.decode(bytes)` and `utf8.encode(string)` convert between bytes and strings; `utf8.decoder.bind(inputStream)` (with `const LineSplitter()`) converts a stream of bytes.
Verify: test inputs include missing and null fields.

## Checked
2026-11-03. Confirmed against dart.dev libraries/dart-convert (jsonDecode, jsonEncode, toJson and second-argument forms, utf8 encode/decode, decoder.bind with LineSplitter) and language/pattern-types plus language/patterns (map patterns, StateError on missing key). Removed: `JsonEncoder.withIndent`, `toIso8601String()` for DateTime, `json.decoder` streaming and the `compute` isolate suggestion (not on the pages read).
Method: documentation only; no commands were run.
