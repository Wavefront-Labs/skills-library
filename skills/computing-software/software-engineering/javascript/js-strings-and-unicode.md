---
id: computing-software.software-engineering.javascript.js-strings-and-unicode
name: js-strings-and-unicode
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-strings, unicode, utf-16, string-normalize, grapheme]
level: practitioner
status: docs-checked
description: "Work with JavaScript strings as UTF-16: code units vs code points, normalisation, Intl.Segmenter."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strings and Unicode

- Strings are sequences of UTF-16 code units. Characters outside the 16-bit range are stored as surrogate pairs, so indexes and `length` count code units and `split("")` separates a surrogate pair into two lone surrogates.
- Code points: `String.fromCodePoint` builds a string from code points.
- For locale-aware comparison use `localeCompare` or `Intl.Collator`, e.g. `str1.localeCompare(str2, locale, { sensitivity: "accent" }) === 0` for case-insensitive equality.

Verify: check that `"😄".length` is 2.

## Checked

2026-11-02. Confirmed: MDN String page: UTF-16 code units and surrogate pairs, lone surrogates, split("") splitting surrogate pairs, fromCodePoint, localeCompare with sensitivity, Intl.Collator.
Removed: Intl.Segmenter grapheme claim, normalize NFC example, toLocaleUpperCase("tr"), isWellFormed ES2024 tag, modern-helper list and regex u/v flag note (not confirmed on the page read).
Method: documentation only; no commands were run.
