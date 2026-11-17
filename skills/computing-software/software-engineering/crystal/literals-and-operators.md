---
id: computing-software.software-engineering.crystal.literals-and-operators
name: literals-and-operators
category: computing-software
field: software-engineering
product: crystal
tags: [literals-and-operators, syntax-basics, literals, integers, strings, symbols, ranges, tuple-literal, operators, string-interpolation, crystal]
level: intro
status: draft
description: "Integer, float, string, symbol, array, hash, range, tuple, regex literals and the main operators with their method-call semantics."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Literals and operators

Goal: read and write all core literals.

- Ints: `1`, `1_000`, `0xff`, `0b101`, `1_i64`, `2u8`; floats `1.5`, `1e3_f32`.
- Strings: `"a #{x}"` interpolates, `'c'` is a Char, `%w(a b)` is Array(String), `%i(a b)` Array(Symbol), heredoc `<<-TXT`.
- Collections: `[1, 2]`, `{"k" => 1}`, `{1, "a"}` Tuple, `{a: 1}` NamedTuple, `1..5` and `1...5` ranges, `/re/i` Regex.
- Operators are methods (`a + b` calls `a.+(b)`), so user types can define them; `&&`, `||`, `!` are not overloadable.
- Integer overflow raises `OverflowError` for `+`, while `&+` wraps.

Gotchas:
- `{}` alone is invalid; write `{} of String => Int32`.
- Default integer literal type is Int32 unless the value needs Int64.
- Single quotes are a Char, not a string.

Verify: `crystal eval 'p typeof({a: 1}, [1], 1..2)'`.
