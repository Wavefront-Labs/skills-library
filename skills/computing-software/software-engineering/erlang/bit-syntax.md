---
id: computing-software.software-engineering.erlang.bit-syntax
name: bit-syntax
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-binaries, bit-syntax]
level: practitioner
status: docs-checked
description: "Erlang bit syntax: segment size, type, endianness, signedness and unit specifiers for parsing and building binary protocols."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bit syntax construction and matching
**Goal:** parse and build binary formats declaratively.

```erlang
Pkt = <<1:8, 513:16/big, "hi">>.
<<Ver:8, Len:16/little-unsigned, Body:Len/binary, Rest/binary>> = Data.
<<A:4, B:4>> = <<16#AB>>.                     % A=10, B=11
```
- Segment form: `Value:Size/TypeSpecifierList`. Types: `integer`, `float`, `binary`, `bitstring`, `utf8`, `utf16`, `utf32`; signedness `signed`/`unsigned`; endianness `big` (default), `little`, `native`; `unit:N`.
- A size can use a variable bound earlier in the same pattern (length-prefixed fields).
- `Rest/binary` must be last; matching it creates a sub-binary, not a copy.

## Gotchas
- Size is in bits for integers, bytes for `binary` (unit 8).
- A match failure raises `badmatch`; for network input prefer a `case` with an explicit short-data clause.

## Self-check
Encode `{1, 513, <<"hi">>}` then parse it back with the pattern above.

## Checked
2026-11-02. Confirmed: system/bit_syntax.html and expressions.html: Value:Size/TypeSpecifierList, unit, big/little/native, signedness, utf8/utf16/utf32 with no Size.
Removed: See edits: unverified performance claim and the example line with a corrupt byte sequence.
Method: documentation only; no commands were run.
