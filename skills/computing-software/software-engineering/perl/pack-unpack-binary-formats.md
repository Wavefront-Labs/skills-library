---
id: computing-software.software-engineering.perl.pack-unpack-binary-formats
name: pack-unpack-binary-formats
category: computing-software
field: software-engineering
product: perl
tags: [perl, pack, unpack, binary-data, endianness, perlpacktut, pack-unpack-binary-formats]
level: advanced
status: docs-checked
description: "Encode and decode binary records with pack/unpack templates (A, a, Z, N, n, V, v, C, w, U), counts, groups and endianness modifiers."
sources: ["https://perldoc.perl.org/perlpacktut", "https://perldoc.perl.org/perlfunc"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pack and unpack

**Goal:** read and write fixed binary layouts.

| Letter | Meaning |
|---|---|
| `a A Z` | string padded with NUL (a), space-padded/stripped (A), NUL-terminated (Z) |
| `C c` | unsigned/signed char (byte) |
| `n N` | unsigned 16/32-bit big-endian (network order) |
| `v V` | unsigned 16/32-bit little-endian |
| `s l q` (`S L Q`) | signed 16/32/64-bit (`S L Q` unsigned); `!` forces native sizes for `s l`; `<` or `>` force little or big endian |
| `H h` | hex string, high/low nybble first |
| `U` | Unicode code point; `w` BER integer; `f d` floats |
| `x X @` | null byte, back up a byte, absolute position |
| `N/a*` | length-prefixed string |

```perl
my $rec  = pack('A8 n C Z*', 'name', 513, 7, 'tail');
my ($n, $port, $flag) = unpack('A8 n C', $rec);
my @bytes = unpack('C*', $str);                        # byte values
my $hex   = unpack('H*', $bytes);   my $raw = pack('H*', 'deadbeef');
my $ip    = join '.', unpack('C4', pack('N', $n));
my ($len, $payload) = unpack('N/a* a*', $buf);
my @fields = unpack('(A3)*', $fixed);                  # group repeated
my $le = pack('l< q>', -2, 5);                         # explicit endianness
my $chk = unpack('%32C*', $data) % 65535;             # checksum prefix %32
```

## Rules
- `i I` are native-size integers and `!` forces native sizes; for portable files use `n N v V` or the `<` and `>` modifiers.
- `A` strips trailing spaces/NULs on unpack; use `a` to keep exactly.
- `vec` handles bit vectors; `sprintf('%b', $n)` formats a number in binary.

## Self-check
- [ ] `perl -e 'print unpack("H*", pack("n", 513))'` prints `0201`.

## Checked
2026-11-03: confirmed against perlfunc pack/unpack (template letters a A Z b B h H c C s S l L q Q i I n N v V f d U w x X @, the ! < > modifiers, repeat counts and groups, N/a* length prefixes, the %32 checksum prefix, A stripping and a keeping trailing data) and perlpacktut. Fixed: s, l, q are fixed-size 16/32/64-bit, native sizes need `!`. Removed: U0/C0 remark, short-data remark, oct('0b') claim, Convert::Binary::C and Data::ParseBinary.
Method: documentation only; no commands were run.
