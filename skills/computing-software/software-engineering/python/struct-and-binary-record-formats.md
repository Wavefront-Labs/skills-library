---
id: computing-software.software-engineering.python.struct-and-binary-record-formats
name: struct-and-binary-record-formats
category: computing-software
field: software-engineering
product: python
tags: [python, py-serialization, struct-binary-formats, struct, endianness, binary-protocols, pack-unpack, ctypes-structure]
level: practitioner
status: docs-checked
description: "Pack and unpack fixed binary records with struct: format strings, byte order and alignment, unpack_from on buffers, iter_unpack and validating untrusted lengths."
sources: ["https://docs.python.org/3/library/struct.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# struct and binary record formats

```python
import struct

HEADER = struct.Struct("<4sHHI")            # little-endian: magic(4s) version(H) flags(H) length(I)
raw = HEADER.pack(b"DATA", 1, 0, 1024)      # 12 bytes (no padding with a byte-order prefix)
magic, ver, flags, length = HEADER.unpack(raw)
magic, ver, flags, length = HEADER.unpack_from(buffer, offset=8)    # no slicing copy; bytes/bytearray/mmap/memoryview
for rec in struct.iter_unpack("<If", payload): ...                  # payload size must be a multiple of the record
HEADER.size                                                          # 12
```

## Byte order and alignment
| Prefix | Order | Size | Alignment padding |
|---|---|---|---|
| `@` (default) | native | native | yes |
| `=` | native | standard | no |
| `<` / `>` / `!` | little / big / network | standard | no |
Always write an explicit prefix for file and wire formats. The default `@` uses native sizes and inserts C-style alignment padding (platform dependent; check `struct.calcsize`), while `"<bI"` is 5 bytes.

## Format codes
`b/B` int8, `h/H` int16, `i/I` int32, `q/Q` int64, `e/f/d` float16/32/64, `?` bool, `s` fixed bytes (`10s`, NUL-padded on pack), `p` Pascal string, `x` pad, `n/N` native ssize_t/size_t (`@` only). Variable-length data needs a length field and a second `unpack_from`.

## Gotchas
- `struct.error` for wrong size or out-of-range ints (`pack("<B", 256)`); catch it for untrusted input.
- Validate lengths read from the stream before using them (cap, check against remaining bytes) to avoid memory blowups.
- `s` returns `bytes`, not `str`; strip padding with `.rstrip(b"\0")` and decode explicitly.
- Floats: `f` loses precision relative to Python's 64-bit `d`.

## Verify
- [ ] Round-trip test with extremes (max uint, negative ints, empty strings) and a known-good byte fixture from the spec.
- [ ] Fuzz `unpack` on random truncated buffers; only `struct.error` is acceptable.

## Checked

- 2026-11-03: checked against the CPython docs `library/struct.rst`: byte order/size/alignment prefix table, `unpack` size match, `unpack_from`, `iter_unpack` (buffer must be a multiple of the record size), type codes including `e`, `n`/`N`, `p`, `s` null padding, `struct.error` on out-of-range values, buffer protocol.
- Removed: the `Struct` caching remark and third-party format library suggestions.

Method: documentation only; no commands were run.
