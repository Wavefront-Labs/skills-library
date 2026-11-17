---
id: computing-software.software-engineering.javascript.js-string-normalization
name: js-string-normalization
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, string-normalize, js-strings]
level: advanced
status: docs-checked
description: "Normalize Unicode strings with String.prototype.normalize before comparing; know NFC, NFD, NFKC and NFKD."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/normalize"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode normalization

- One abstract character can be one code point or a sequence: `"ñ"` and `"ñ"` both display as ñ, but `===` is false and their lengths are 1 and 2.
- `str.normalize(form)` converts to a form common to all equivalent sequences. `form` is `"NFC"` (default when omitted), `"NFD"`, `"NFKC"` or `"NFKD"`; any other value throws `RangeError`.
- Canonical equivalence: NFC is canonical decomposition followed by canonical composition, NFD is canonical decomposition. Normalize both strings to the same form before comparing: `a.normalize("NFC") === b.normalize("NFC")` (MDN's `Amélie` example becomes equal).
- NFKC is compatibility decomposition followed by canonical composition, NFKD is compatibility decomposition. Consider what the string is for: compatibility normalization suits search but may not suit display because the visual representation changes.

Self-check: `"ñ" === "ñ"` is false; after `.normalize("NFC")` on both it is true.

## Checked

Date: 2026-11-03. Confirmed on MDN String/normalize: the four forms and definitions, default, RangeError, ñ and Amélie examples, lengths, the search-versus-display note. Removed as not stated there: storage and hashing advice, localeCompare sensitivity, `toLocaleLowerCase("tr")`, stripping accents with `\p{M}`, UTF-16 length of emoji, and for...of iteration advice.

Method: documentation only; no commands were run.
