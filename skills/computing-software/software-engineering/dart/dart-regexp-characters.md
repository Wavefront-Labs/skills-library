---
id: computing-software.software-engineering.dart.dart-regexp-characters
name: dart-regexp-characters
category: computing-software
field: software-engineering
product: dart
tags: [dart, dart-strings-regex, regexp-characters]
level: practitioner
status: docs-checked
description: "Use RegExp, handle UTF-16 units vs grapheme clusters with the characters package, and trim and case text."
sources: ["https://dart.dev/libraries/dart-core", "https://dart.dev/language/built-in-types"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RegExp, characters and unicode
- `RegExp(r'\d+')` offers the same capabilities as JavaScript regular expressions; use `hasMatch`, `allMatches` (each `Match` has `group(0)`), `str.contains(regexp)` and `str.replaceAll(regexp, 'XX')`.
- A Dart string is an immutable sequence of UTF-16 code units: high-numbered characters are two units, and a flag emoji is one user-perceived character but several units. `package:characters` (`hi.characters.last`) iterates user-perceived characters (grapheme clusters); `runes` expose code points.
- `split`, `trim`, `isEmpty`, `toLowerCase`/`toUpperCase` (wrong for some languages, for example Turkish dotless I).

Verify: test strings with emoji and combining marks.

## Checked

Checked 2026-11-08 against the strings and regular expressions sections of https://dart.dev/libraries/dart-core and https://dart.dev/language/built-in-types. Removed (not confirmed in pages read): named groups with `namedGroup`, `firstMatch`, `replaceAllMapped`, the "no possessive quantifiers" claim, `padLeft`/`padRight`, and the `intl` formatting note.

Method: documentation only; no commands were run.
