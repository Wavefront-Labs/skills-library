---
id: computing-software.software-engineering.crystal.string-api
name: string-api
category: computing-software
field: software-engineering
product: crystal
tags: [string-api, stdlib-strings-numbers, string, string-methods, split, gsub, strip, starts-with, substring, utf-8, char, bytesize, string-builder, format, ljust, crystal]
level: intro
status: docs-checked
description: "Use immutable UTF-8 String: slicing by chars, split, strip, gsub, scan, format, interpolation, bytes vs chars and StringBuilder."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String API

Goal: manipulate text correctly.

- Strings are immutable UTF-8; `size` counts chars, `bytesize` bytes; character indexing and slicing scan from the start unless the string is known to be ASCII-only (`ascii_only?`).
- Common: `split`, `strip`, `lstrip`, `downcase`, `upcase`, `capitalize`, `starts_with?`, `includes?`, `index`, `sub`, `gsub(/re/) { |m| }`, `tr`, `reverse`, `center`, `ljust`, `rjust`, `lines`, `chars`, `bytes`, `each_char`, `to_i`, `to_i?`, `to_f`, `%` and `sprintf` / `"%05.2f" % x` for formatting.
- Build efficiently: `String.build { |io| io << "a" << 1 }`, `IO::Memory`.
- `s.to_i` raises ArgumentError on bad input; `to_i?` returns nil; `to_i(base)`.
- Unicode: `s.unicode_normalize` (default NFC; also `:nfd`, `:nfkc`, `:nfkd`), `Char#ord`.

Gotchas:
- `String#+` allocates; in loops use `String.build`.
- Case mapping is Unicode-aware.
- A byte that does not start a valid UTF-8 sequence is read as U+FFFD when iterating chars (no exception); check `valid_encoding?`, `scrub` repairs.

Verify: `"héllo".size` is 5 and `.bytesize` is 6.

## Checked

Date 2026-11-03. Confirmed String.build, size/bytesize, unicode_normalize (forms :nfc default, :nfd, :nfkc, :nfkd), valid_encoding? and the U+FFFD behaviour for invalid bytes, to_i/to_i? and the ArgumentError doc, sub/gsub (pattern with block), split, scan, center/ljust/rjust, tr, lines, each_char, capitalize, lstrip, reverse, scrub, and Kernel#sprintf in the String and Kernel source. Removed the O(n) wording (source only says slicing is slower unless ASCII-only is proven), the unverified heredoc bullet and the 'case mapping' gotcha.

Method: documentation only; no commands were run.
