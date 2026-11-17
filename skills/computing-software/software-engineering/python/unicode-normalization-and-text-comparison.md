---
id: computing-software.software-engineering.python.unicode-normalization-and-text-comparison
name: unicode-normalization-and-text-comparison
category: computing-software
field: software-engineering
product: python
tags: [python, py-text, unicode-normalization, unicodedata, nfc, nfkc, casefold, text-comparison, encoding]
level: practitioner
status: docs-checked
description: "Compare, dedupe and sort Unicode text safely with unicodedata.normalize (NFC/NFKC), str.casefold, grapheme caveats and encoding errors handlers."
sources: ["https://docs.python.org/3/library/unicodedata.html", "https://docs.python.org/3/howto/unicode.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unicode normalization and text comparison

The same visible text can be different code points: "é" is U+00E9 (precomposed) or "e"+U+0301.

```python
import unicodedata as ud
a, b = "café", "café"
assert a != b and len(a) == 4 and len(b) == 5
assert ud.normalize("NFC", a) == ud.normalize("NFC", b)

def key(s: str) -> str:                       # identity key for lookup/dedupe
    return ud.normalize("NFKC", s).casefold()

key("Straße") == key("STRASSE")               # True: casefold maps ß -> ss
```

## Which form
- **NFC**: store and compare text (web, databases). **NFD**: when you want to strip accents.
- **NFKC/NFKD**: also fold compatibility characters (fullwidth "ＡＢＣ", ligature "ﬁ", superscripts). Lossy; good for search keys and usernames, wrong for stored display text.
- Strip accents: `"".join(c for c in ud.normalize("NFD", s) if not ud.combining(c))`.
- Case-insensitive compare: `casefold()`, not `lower()`.

## Encoding
Pass `encoding="utf-8"` to `open()` explicitly. Decoding error handlers: `errors="replace"` (U+FFFD), `"ignore"` (drops the character), `"backslashreplace"` (inserts a `\xNN` escape), and `"surrogateescape"`, which maps undecodable bytes to U+DC80..U+DCFF so they round-trip when written back.

## Gotchas
- `len(s)` counts code points, not user-perceived characters (emoji with ZWJ, flags); Python 3.15 adds `unicodedata.iter_graphemes()` for grapheme clusters.
- Normalize at the trust boundary once, not at every comparison.

## Verify
- [ ] A test pairs precomposed and decomposed inputs and expects equal keys.
- [ ] Reading a file with the wrong encoding fails loudly (no silent `errors="ignore"`).

## Checked

2026-11-08. Confirmed on the unicodedata page and the Unicode HOWTO: `normalize()` forms NFC, NFKC, NFD, NFKD, NFC composes and NFD decomposes, `combining()`, `casefold()` turns ß into ss and is the case-insensitive tool, normalising before comparing combining characters, errors handlers `strict`/`replace` (U+FFFD)/`ignore`/`backslashreplace`, the `surrogateescape` range U+DC80 to U+DCFF, and `unicodedata.iter_graphemes()` (added in 3.15). Removed: the locale-dependent default encoding remark, the third-party grapheme modules, confusable-script advice, `isalpha`/`\d`/`re.ASCII` and `locale.strxfrm` sorting bullets (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
