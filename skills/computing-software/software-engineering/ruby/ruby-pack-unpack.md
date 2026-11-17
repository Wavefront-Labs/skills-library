---
id: computing-software.software-engineering.ruby.ruby-pack-unpack
name: ruby-pack-unpack
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, pack-unpack, binary]
level: advanced
status: docs-checked
description: "Read and write binary formats in Ruby with Array#pack and String#unpack: endianness, integer widths, strings, offsets and short input."
sources: ["https://docs.ruby-lang.org/en/master/packed_data_rdoc.html", "https://docs.ruby-lang.org/en/master/String.html#method-i-unpack"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary data with pack and unpack

```ruby
header = [0xCAFE, 3, 1.5].pack("nCg")      # n=u16 big-endian, C=u8, g=float32 big-endian
magic, ver, ratio = header.unpack("nCg")
[1, 2].pack("L<2")                          # two little-endian u32
data.unpack1("N")                           # first u32 big-endian, returns a scalar
data.unpack("a4 x2 Z*")                     # 4 raw bytes, skip 2, NUL-terminated string
data.unpack1("@8 n")                        # @ jumps to absolute offset 8
data.unpack("C*")                           # array of bytes
[ "hello" ].pack("m0")                      # Base64 (RFC 4648), no newlines
"abc".unpack("H*")                          # hex string
```
Directive cheat-sheet: `C c` 8-bit, `S s` 16, `L l` 32, `Q q` 64 (uppercase unsigned), `n N` network order 16/32, `v V` little-endian 16/32, `<` `>` modifiers force endianness, `e g` single-precision floats (little- and big-endian) and `E G` double-precision, `a A Z` strings (`a` binary, null padded; `A` space padded; `Z` null-terminated), `U` UTF-8 character, `w` BER integer, `x` skip byte.

## Gotchas
- `S L Q` (and `s l q`) are fixed 16, 32 and 64 bits but in native byte order; `i I` have platform-dependent width; the `!` or `_` modifier gives the platform's native size for `s S l L q Q`. Add `<` or `>` (or use `n N v V`) for file and wire formats.
- Unpacking truncated input does not raise: a directive with no data yields `nil` (`'A'.unpack('CC')` is `[65, nil]`), so check `data.bytesize` against the expected length before parsing untrusted data. Packing with more directives than elements raises `ArgumentError`.
- `@` in unpack jumps to an absolute offset and raises `ArgumentError` when it moves outside the string; `x` and `X` skip forward and back.
- Check length fields read from input before using them to size anything else.
- `String#unpack` and `unpack1` accept `offset:` to start at a byte offset, which suits repeated record parsing.
- A value that does not fit the directive keeps only its least significant bits (`[257].pack("C").unpack("C")` is `[1]`).

Verify: round trip `[v].pack(fmt).unpack1(fmt) == v` for min, max and negative values.

## Checked
2026-11-03. Confirmed against ruby/ruby `doc/language/packed_data.md` (directive tables, `*` and counts, `@ x X` behaviour, nil padding, `offset:`, `m0`, least-significant-bit note) and `pack.rb` (`unpack1(template, offset: 0)`). Fixed: the old gotcha said `S L Q` use native size; they are fixed width, only `i I` and the `!`/`_` forms vary. Removed: Base64 `strict_encode64`, the ASCII-8BIT result claim, `byteslice`, the Ruby 3.1 version tag and the hexdump comparison.
Method: documentation only; no commands were run.
