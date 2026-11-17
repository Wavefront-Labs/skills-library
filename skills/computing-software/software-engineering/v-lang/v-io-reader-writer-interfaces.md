---
id: computing-software.software-engineering.v-lang.v-io-reader-writer-interfaces
name: v-io-reader-writer-interfaces
category: computing-software
field: software-engineering
product: v-lang
tags: [v-io-reader-writer-interfaces, io-and-streams, io, io.reader, io.writer, read_all, copy, stream, interfaces, readers writers, v-lang]
level: practitioner
status: docs-checked
description: "Program against io.Reader and io.Writer, copy streams, read all, and compose readers for files, sockets and buffers."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# io.Reader, io.Writer and helpers

Goal: write I/O code independent of the source.

- `interface Reader { read(mut buf []u8) !int }` and `Writer { write(buf []u8) !int }` live in `io`; files such as `os.File` and TCP connections can be passed where a `Reader` or `Writer` is expected.
- Read everything: `data := io.read_all(reader: r)!`.
- Copy: `io.cp(mut src, mut dst)!`.
- Multi: `io.new_multi_writer(w1, w2)` takes variadic `...Writer` and returns a `Writer`.
- Fixed buffer: `mut buf := []u8{len: 4096}; n := r.read(mut buf)!` then use `buf[..n]`.
- Return `io.Eof` handling: `r.read(mut buf) or { if err is io.Eof { break } return err }`.

Gotchas:
- A read may return fewer bytes than requested; loop until Eof.
- `io.cp(mut src, mut dst)` takes both arguments as `mut`.

Verify: pipe a string through two writers and assert both received it.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: Reader interface (read(mut buf []u8) !int, returns io.Eof at end of stream), Writer, io.read_all(ReadAllConfig), io.cp(mut src Reader, mut dst Writer, params), new_multi_writer(writers ...Writer) Writer (vlib/io).
Removed or corrected: 'strings.Builder and buffers implement them' (not confirmed), the array form of new_multi_writer, and '(confirm)'.
Method: documentation only; no commands were run.
