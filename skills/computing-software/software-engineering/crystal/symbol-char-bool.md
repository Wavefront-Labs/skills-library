---
id: computing-software.software-engineering.crystal.symbol-char-bool
name: symbol-char-bool
category: computing-software
field: software-engineering
product: crystal
tags: [symbol-char-bool, stdlib-strings-numbers, symbol, char, bool, object, tap, inspect, to-s, pp, p, then, crystal]
level: intro
status: draft
description: "Work with interned Symbols, Unicode Chars, Bool and common Object methods like to_s, inspect, ==, ===, hash and tap."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Symbol, Char, Bool, Nil and Object basics

Goal: know the small core types.

- Symbols `:name` are compile-time constants (there is no runtime String to Symbol conversion; use Symbols for fixed identifiers, enums or strings otherwise).
- Char `'a'`, `c.ord`, `c.letter?`, `c.number?`, `c.upcase`, `Char::ZERO`; `65.chr`.
- Debug: `p x` (inspect and returns x), `pp x` pretty, `puts x` (to_s), `print`, `STDERR.puts`, `p!(x)` prints expression and value.
- Object helpers: `tap { |o| }`, `try`, `itself`, `is_a?`, `nil?`, `as`, `hash`, `object_id`, `dup`, `clone`, `instance_variable`-like via macros only.

Gotchas:
- No `send`/`method_missing` at runtime; use macros or case.
- Symbols compare by identity, fast; but convert with `to_s`.
- `Bool` has no `to_i`.

Verify: `crystal eval 'p! 1+1'`.
