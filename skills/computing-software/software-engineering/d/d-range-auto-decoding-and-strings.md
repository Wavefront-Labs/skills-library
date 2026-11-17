---
id: computing-software.software-engineering.d.d-range-auto-decoding-and-strings
name: d-range-auto-decoding-and-strings
category: computing-software
field: software-engineering
product: d
tags: [d-range-auto-decoding-and-strings, std-range, auto-decoding, bycodeunit, bychar, bydchar, bygrapheme, utf-8, std-uni, string-range, d]
level: advanced
status: docs-checked
description: "Understand D string auto-decoding to dchar in range functions, avoid it with byCodeUnit/byChar for ASCII speed, and use std.uni byGrapheme and normalization."
sources:
  - https://dlang.org/phobos/std_utf.html
  - https://dlang.org/phobos/std_uni.html
  - https://dlang.org/phobos/std_range.html
  - https://dlang.org/phobos/std_range_primitives.html
  - https://dlang.org/phobos/std_algorithm_iteration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings as ranges: auto-decoding, byCodeUnit, byChar, byGrapheme

Goal: iterate text correctly and fast.

- Range functions treat narrow strings (`char[]`/`string`) as ranges of `dchar`: `std.range.primitives.front` decodes UTF and throws on invalid sequences, and narrow strings cannot be indexed as ranges (`isAutodecodableString`).
- Skip decoding: `byCodeUnit` (nothrow, bypasses the decoding that `front` does), `byChar`, `byWchar`, `byDchar` (std.utf); `representation` (std.string) exposes the integral code units.
- Count and walk: `walkLength` counts elements of a range (code points for a decoded string); `std.utf.stride`, `strideBack`, `toUTFindex` (std.utf) for offsets.
- User-perceived characters: `std.uni.byGrapheme`, `graphemeStride`; `normalize` (NFC by default) and the forms `NFC`, `NFD`, `NFKD`; case mapping `toLower`, `toUpper`, `asLowerCase`, `asUpperCase` (lazy); `icmp` and `sicmp` for caseless comparison.
- Validation and decoding: `std.utf.validate`, `std.utf.decode(s, idx)` reads one code point and advances `idx`.

Gotchas:
- Slicing a string at an arbitrary byte offset can cut a UTF-8 sequence.
- A grapheme can consist of several code points; count graphemes with `byGrapheme`.

Verify: unittest comparing `walkLength`, `.length` and the `byGrapheme` count on a combining-accent string.

## Checked

2026-11-03. Confirmed against: std.utf, std.uni and std.range reference pages.

Removed because the pages read did not confirm it: the two-byte accented-letter length example, `std.utf.count`, `std.conv.text`/`dtext`/`wtext`, the `s[i]` byte remark.

Method: documentation only; no commands were run.
