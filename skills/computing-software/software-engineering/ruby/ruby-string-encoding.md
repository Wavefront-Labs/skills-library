---
id: computing-software.software-engineering.ruby.ruby-string-encoding
name: ruby-string-encoding
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, string-encoding, unicode]
level: practitioner
status: docs-checked
description: "Handle Ruby string encodings: force_encoding vs encode, scrub invalid bytes, binary data, BOM and Unicode normalisation."
sources: ["https://docs.ruby-lang.org/en/master/Encoding.html", "https://docs.ruby-lang.org/en/master/String.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String encodings

Every String carries an encoding tag: `str.encoding`, `str.valid_encoding?`, `str.bytesize` vs `str.length`.
```ruby
bytes.force_encoding("UTF-8")           # relabel, bytes unchanged (use for data you know is UTF-8)
latin.encode("UTF-8", "ISO-8859-1")     # transcode, bytes change
dirty.scrub("?")                        # replace invalid sequences
s.encode("UTF-8", invalid: :replace, undef: :replace, replace: "?")
File.read(p, encoding: "bom|utf-8")     # strip BOM
File.binread(p)                         # ASCII-8BIT (BINARY) string
"é".unicode_normalize(:nfc)             # needs no gem; compare composed vs decomposed forms
```
Defaults: source files are UTF-8 (`__ENCODING__`); `Encoding.default_external` can be set with the `-E` or `--external_encoding` command-line options or `Encoding.default_external=`; `Encoding.default_internal` is `nil` by default. The `locale` encoding is the default for strings from the environment.

## Gotchas
- `Encoding::CompatibilityError` appears when concatenating UTF-8 text with a binary string holding non-ASCII bytes. Decide which side is wrong and relabel or transcode.
- `force_encoding` changes only the label, even when the result is invalid for the bytes (`valid_encoding?` then returns false).
- Some String methods raise `ArgumentError` ("invalid byte sequence in UTF-8") on an invalid string; scrub input at the boundary.
- Use `each_grapheme_cluster` to iterate user-perceived characters; `length` counts code points.
- Decode data from the network or database explicitly rather than relying on defaults.

Verify: `"\xFF".valid_encoding?` is false and `"\xFF".scrub("?").valid_encoding?` is true.

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/language/encodings.rdoc` (default_external/default_internal, `-E`, locale, BINARY/ASCII-8BIT, `__ENCODING__`), `doc/string/force_encoding.rdoc`, `string.c` (invalid byte sequence ArgumentError, scrub, unicode_normalize loaded on demand, each_grapheme_cluster), `encoding.c` (CompatibilityError text) and `io.c` (`bom|` encoding prefix). Removed: LANG=C.UTF-8 advice, FrozenError and full-case-mapping claims.
Method: documentation only; no commands were run.

Normalisation check (composed versus decomposed forms): `"é".unicode_normalize(:nfc) == "é"`.
