---
id: computing-software.software-engineering.dart.dart-typed-data-bytes
name: dart-typed-data-bytes
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-bytes, typed-data-bytes]
level: practitioner
status: draft
description: "Handle binary protocols with typed_data, ByteData endianness and conversion to and from strings."
sources: ["https://dart.dev/language", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Uint8List, ByteData and endianness
- `Uint8List`, `Int32List`, `Float64List` are compact and fast; `ByteData.view(bytes.buffer)` reads fields with `getUint32(0, Endian.big)` (default is big-endian).
- `utf8.encode(s)` returns bytes, `utf8.decode(bytes, allowMalformed: true)`; `base64Encode`, `hex` via `package:convert`.
- `Uint8List.sublistView(list, 4, 8)` shares memory; `sublist` copies.
- On web, 64-bit integer accessors behave differently.
Verify: round-trip encode and decode in tests.
