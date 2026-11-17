---
id: computing-software.software-engineering.d.d-stdio-binary-io-and-stdin-patterns
name: d-stdio-binary-io-and-stdin-patterns
category: computing-software
field: software-engineering
product: d
tags: [d-stdio-binary-io-and-stdin-patterns, std-stdio, binary-io, rawread, rawwrite, bitmanip, mmfile, stdin, bychunk, endian, nativetobigendian, memory-mapped-file, d]
level: practitioner
status: draft
description: "Read and write binary data with rawRead/rawWrite and std.bitmanip, process stdin line streams quickly, and memory-map big files with std.mmfile.MmFile."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Binary I/O, stdin processing patterns and std.mmfile

Goal: efficient byte-level I/O.

- Binary records: `struct Hdr { uint magic; ushort ver; }` (check `align(1)`/padding) then `Hdr h; f.rawRead((&h)[0 .. 1]);` for fixed layouts; write with `f.rawWrite((&h)[0 .. 1])`.
- Endianness: `std.bitmanip.read!(uint, Endian.bigEndian)(ubyte[]range)`, `write!`, `peek!`, `nativeToBigEndian(x)` returning `ubyte[N]`, `bigEndianToNative!uint(bytes)`, `swapEndian`.
- Stream bytes: `foreach (ubyte[] chunk; f.byChunk(65536))` (chunk buffer reused).
- stdin filters: `foreach (line; stdin.byLine) { ... }` for streaming; `stdin.byLineCopy.array` to load; `File("/dev/stdin")` on POSIX.
- Memory map: `auto mm = new MmFile("big.bin", MmFile.Mode.read, 0, null); auto data = cast(const(ubyte)[]) mm[];` access like a slice, no copying; size 0 maps the whole file; use `MmFile.Mode.readWriteNew` + size to create.
- `std.outbuffer.OutBuffer` for building binary messages; `std.zlib`/`std.zip` for compression.

Gotchas:
- Struct padding differs from on-disk layout; serialise field by field.
- mmap of files shrinking underneath you produces SIGBUS.

Verify: round-trip a struct through a temp file and compare.
