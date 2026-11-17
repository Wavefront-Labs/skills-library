---
id: computing-software.software-engineering.v-lang.v-utf8-iteration-and-bytes
name: v-utf8-iteration-and-bytes
category: computing-software
field: software-engineering
product: v-lang
tags: [v-utf8-iteration-and-bytes, runes-and-unicode, utf-8, runes, bytes, iterate string, u8, string to runes, v-lang]
level: practitioner
status: docs-checked
description: "Iterate a string by byte or by rune, convert between string, []rune and []u8, and measure character counts."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Iterating UTF-8 text and bytes

Goal: loop over text at the right granularity.

- Bytes: indexing a string gives a `u8` (`s[0]`), so loop with `for i in 0 .. s.len { s[i] }`.
- Characters: `for r in s.runes() { }` yields `rune`; `s.runes().len` is the char count.
- To string from runes: `[]rune` has `.string()`; from bytes: `bytes.bytestr()`; to bytes: `s.bytes()`.
- Check validity: `import encoding.utf8; utf8.validate_str(s)`; the builtin `utf8_str_visible_length(s)` counts displayed characters (its doc points to `utf8.east_asian.display_width` for spec-compliant width).
- Index by character requires converting first: `rs := s.runes(); rs[2]`.

Gotchas:
- Indexing and slicing by byte offset can land mid-character and yield invalid UTF-8.

Verify: iterate `'日本'` by bytes (6) and by runes (2) and assert the counts.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: string indexing yields bytes and runes() returns the characters (doc/docs.md, Strings section), []rune.string(), []u8.bytestr(), string.bytes() (vlib/builtin), utf8.validate_str (vlib/encoding/utf8/utf8.v), utf8_str_visible_length (vlib/builtin/utf8.v).
Removed or corrected: 'for b in s yields bytes' (not in the docs read), '(confirm name)', and the unverified claim that runes() allocates.
Method: documentation only; no commands were run.
