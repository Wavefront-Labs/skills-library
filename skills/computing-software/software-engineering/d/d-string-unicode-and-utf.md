---
id: computing-software.software-engineering.d.d-string-unicode-and-utf
name: d-string-unicode-and-utf
category: computing-software
field: software-engineering
product: d
tags: [d-string-unicode-and-utf, std-string, unicode, utf-8, std-utf, std-uni, decode, encode, validate, normalize, codepoint, toutf8, dstring, d]
level: practitioner
status: docs-checked
description: "Handle UTF-8/16/32 safely with std.utf (decode, encode, validate, toUTF8), std.uni (isAlpha, toLower, normalize, graphemes) and conversions between string, wstring, dstring."
sources:
  - https://dlang.org/phobos/std_utf.html
  - https://dlang.org/phobos/std_uni.html
  - https://dlang.org/phobos/std_encoding.html
  - https://dlang.org/spec/arrays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode in D: std.utf, std.uni, normalization and case

Goal: treat text as Unicode, not bytes.

- `string` is UTF-8, `wstring` UTF-16, `dstring` UTF-32. Convert with `toUTF8`, `toUTF16`, `toUTF32` (std.utf) or `std.conv.to`.
- Decode manually: `size_t i = 0; dchar c = decode(s, i);` advances `i`; `encode`; `codeLength!char(c)`; `validate(s)`; `isValidDchar`; `replacementDchar`; `byDchar` for iteration that replaces invalid sequences.
- `std.uni`: `isAlpha`, `isNumber`, `isWhite`, `isUpper`, `toLower`, `toUpper`, `asCapitalized`, `normalize` with `NFC`/`NFD`/`NFKD`, `byGrapheme`, `sicmp` and `icmp` for caseless comparison, `unicode` property sets.
- `std.encoding` handles other encodings (`transcode`, `EncodingScheme`).
- `char.init` is `0xFF`, which is invalid UTF-8, so uninitialised chars are detectable.

Gotchas:
- Slicing at arbitrary byte offsets can cut a code point.
- Canonically equivalent strings compare equal only after normalization.

Verify: unittest round-trip `s.to!dstring.to!string == s` for multilingual text.

## Checked

2026-11-03. Confirmed against: std.utf, std.uni, std.encoding and the arrays spec page (`char.init == 0xFF`).

Removed because the pages read did not confirm it: `toTitlecase` (not on the page; `asCapitalized` is listed), `unicode.Greek`/`unicode.script` details beyond the property-set API, `NFKC` kept (listed), `text`/`wtext`/`dtext`, BOM remark.

Method: documentation only; no commands were run.
