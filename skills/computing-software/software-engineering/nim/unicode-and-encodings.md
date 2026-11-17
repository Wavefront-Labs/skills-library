---
id: computing-software.software-engineering.nim.unicode-and-encodings
name: unicode-and-encodings
category: computing-software
field: software-engineering
product: nim
tags: [unicode-and-encodings, stdlib-strutils-text, unicode, rune, utf8, runes, encodings, casefold, widestring, nim]
level: practitioner
status: docs-checked
description: "Handle UTF-8 text with std/unicode runes, case conversion and conversions with std/encodings."
sources:
  - https://nim-lang.org/docs/unicode.html
  - https://nim-lang.org/docs/encodings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode, runes and encodings

Goal: process non-ASCII text correctly.

- `import std/unicode`; `for r in s.runes`, `s.runeLen`, `runeAt(s, i)`, `s.toRunes` (seq[Rune]), `$r`, `toUTF8(r)`.
- `toUpper`, `toLower`, `capitalize` and `reversed` in std/unicode work on Unicode text; `isAlpha`, `isUpper`, `isLower`, `isSpace` test runes.
- Validate: `validateUtf8(s)` returns the position of the first bad byte or -1.
- `std/encodings`: `convert(s, "UTF-8", "ISO-8859-1")` (uses iconv/Win32).
- `graphemeLen(s, i)` returns the number of bytes belonging to the character at byte index `i`, including following combining code units.

Gotchas:
- `s.len` is bytes, not characters.

Verify: `"héllo".runeLen` is 5 while `.len` is 6.

## Checked

2026-11-03. Confirmed against the unicode and encodings pages: runes iterator, runeLen, runeAt, toRunes, toUTF8, validateUtf8 (position of the invalid byte, else -1), convert(s, destEncoding, srcEncoding) with iconv on UNIX and the Windows API, graphemeLen. Real error fixed: removed `s.title`, which std/unicode does not provide (only `isTitle`). Removed the claim that the stdlib has no grapheme support (graphemeLen exists).

Method: documentation only; no commands were run.
