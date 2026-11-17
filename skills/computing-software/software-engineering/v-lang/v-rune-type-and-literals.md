---
id: computing-software.software-engineering.v-lang.v-rune-type-and-literals
name: v-rune-type-and-literals
category: computing-software
field: software-engineering
product: v-lang
tags: [v-rune-type-and-literals, runes-and-unicode, rune, backtick, unicode, code point, character literal, is_letter, v-lang]
level: practitioner
status: docs-checked
description: "Use rune for Unicode code points with backtick literals, convert to string, classify characters and convert to and from u32."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The rune type and character literals

Goal: work with single characters correctly.

- A `rune` represents a single UTF-32 encoded Unicode character and is an alias for `u32`. Literals use backticks: `` `🚀` ``.
- Escapes work as in strings: `` `\x61` ``, `` `\141` `` (octal), `` `a` `` are all `` `a` ``; `` `★` == `★` ``.
- A rune literal holds exactly one Unicode character; otherwise there is a compile-time error.
- Convert to a UTF-8 string with `.str()` (`` `🚀`.str() == '🚀' ``) and to UTF-8 bytes with `.bytes()` (`` `🚀`.bytes() == [u8(0xf0), 0x9f, 0x9a, 0x80] ``).
- Strings are indexed as bytes, not runes: `'🚀'[0] != `🚀``, while `'aloha!'[0] == `a``.
- A string converts to runes with `.runes()`: `hello.runes()`; `hello_runes.string() == hello`.

Verify: `assert `🚀`.bytes().len == 4`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Runes"). Removed as not stated there: the classification helpers (`is_letter`, `is_digit`, `to_upper`), `rune(0x41)` conversion, `u32(r)`, `write_rune` and string concatenation, the combining-sequence gotcha.

Method: documentation only; no commands were run.
