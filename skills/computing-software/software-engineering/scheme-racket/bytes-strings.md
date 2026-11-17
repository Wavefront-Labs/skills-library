---
id: computing-software.software-engineering.scheme-racket.bytes-strings
name: bytes-strings
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, bytes-strings]
level: practitioner
status: docs-checked
description: "Handle raw data with bytes, convert with string->bytes/utf-8 and bytes->string/utf-8, and avoid decoding errors."
sources:
  - https://docs.racket-lang.org/guide/bytestrings.html
  - https://docs.racket-lang.org/reference/bytestrings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bytes and conversion
**Goal:** convert between text and bytes.
```racket
(define bs (string->bytes/utf-8 "héllo"))
(bytes->string/utf-8 #"h\303\251llo")
(bytes->string/utf-8 bs)
(bytes->string/utf-8 #"\377" #\?)   ; "?" : replacement char for bad input
```
- `bytes->string/utf-8` takes `bstr [err-char start end]`; `err-char` defaults to `#f`.
- With `err-char` `#f`, a byte string that is not valid UTF-8 raises `exn:fail:contract`. If `err-char` is a char, it is used for bytes in the range 128 to 255 that are not part of a valid encoding sequence.
- `string->bytes/utf-8` always succeeds; its `err-byte` argument is ignored.
- `bytes-ref` returns the byte (an integer 0 to 255) at a zero-based position and raises `exn:fail:contract` if the position is out of range.
## Self-check
Decode `#"\377"` with and without the `#\?` argument: the first raises, the second gives `"?"`.

## Checked
2026-11-08. Read in full: Racket Guide 3.5 Bytes and Byte Strings (guide/bytestrings.html); read the Racket Reference bytestrings page entries for `bytes-ref`, `bytes->string/utf-8` and `string->bytes/utf-8` (the page was searched for these, not read end to end). Confirmed the signatures and defaults, the `exn:fail:contract` raise when `err-char` is `#f`, the 128-255 rule for `err-char`, and that `err-byte` is ignored. Fixed a corrupted non-ASCII literal in the example, defined `bs` (it was undefined), and replaced the unrelated strings/symbols and reference/strings sources with the byte-string pages. Removed nothing else.
Method: documentation only; no commands were run.
