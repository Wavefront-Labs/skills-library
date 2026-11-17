---
id: computing-software.software-engineering.nim.strings-mutation-slicing
name: strings-mutation-slicing
category: computing-software
field: software-engineering
product: nim
tags: [strings-mutation-slicing, strings-and-sequences, string, slice, concatenation, cstring, runes, unicode, add, nim]
level: intro
status: docs-checked
description: "Work with Nim's mutable value strings: concatenation, slicing, unicode runes and conversion to cstring."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/system.html
  - https://nim-lang.org/docs/unicode.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings: mutation, slicing and cstring

Goal: use strings efficiently and correctly.

- Strings are mutable, value-semantics byte sequences, UTF-8 by convention; `s.add "x"`, `s &= "x"`, `a & b`; `s.len`.
- Slicing: `s[1..3]` (inclusive), `s[1..^1]` (to end), `s[0..<n]`; `^1` indexes from the back (BackwardsIndex).
- Iterate characters with `for c in s`, bytes with `for b in s.items`, Unicode with `import std/unicode` and `for r in s.runes`.
- `$` converts values to string; `cstring(s)` converts for C APIs.
- Preallocate for loops: `newStringOfCap(n)`; strings are zero-terminated and carry a length, so conversion to `cstring` is O(1) and allocation-free.

Gotchas:
- `s[i]` is a byte, so non-ASCII text indexes wrongly; use runes.

Verify: `"hello"[1..^2]` is "ell".

## Checked

2026-11-03. Confirmed against the manual, system and unicode pages: strings are zero-terminated with a length field, UTF-8 by convention (not enforced), `s[i]` is a byte, `runes` iterator in std/unicode, newStringOfCap, BackwardsIndex `^`. Removed: the IndexDefect claim for slicing and the cstring-to-string copy wording (not confirmed).

Method: documentation only; no commands were run.
