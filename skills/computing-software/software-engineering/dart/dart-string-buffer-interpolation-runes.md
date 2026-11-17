---
id: computing-software.software-engineering.dart.dart-string-buffer-interpolation-runes
name: dart-string-buffer-interpolation-runes
category: computing-software
field: software-engineering
product: dart
tags: [dart, string-buffer-interpolation-runes]
level: practitioner
status: docs-checked
description: "Build Dart strings efficiently and handle code points vs UTF-16 units and grapheme clusters."
sources: ["https://dart.dev/language/built-in-types", "https://dart.dev/libraries/dart-core"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings
- `'$a ${b + c}'` interpolation calls `toString()`; adjacent literals (or `+`) concatenate; `'''multi-line'''`; `r'raw'` has no escape processing.
- Strings are immutable UTF-16 code-unit sequences: methods such as `replaceAll` return a new string.
- Build with `StringBuffer()..write(x)..writeAll(items, ' ')`; no new `String` is created until `toString()`.
- Indexing and `codeUnits` give UTF-16 code units (a treble clef `'\u{1D11E}'` is two); `runes` expose Unicode code points; use the `characters` package (`hi.characters.last`) for user-perceived characters (grapheme clusters), for example a flag emoji.
- `split`, `trim`, `substring`, `toUpperCase` exist (case conversion is wrong for some languages, for example Turkish dotless I); `RegExp(r'\d+')` with `hasMatch`, `allMatches`, and `replaceAll(RegExp, ...)`.

Verify: the `length` of a flag emoji differs from its `.characters.length`.

## Checked

Checked 2026-11-08 against https://dart.dev/language/built-in-types (read in full) and the strings and regular expressions sections of https://dart.dev/libraries/dart-core. Removed (not confirmed in pages read): `padLeft` and `replaceAllMapped`, and the `writeln` example.

Method: documentation only; no commands were run.
