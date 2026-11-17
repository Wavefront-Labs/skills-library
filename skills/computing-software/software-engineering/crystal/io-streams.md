---
id: computing-software.software-engineering.crystal.io-streams
name: io-streams
category: computing-software
field: software-engineering
product: crystal
tags: [io-streams, stdlib-io-files, io, io-memory, stdin, stdout, stderr, gets, read-bytes, io-copy, multiwriter, io-pipe, buffer, crystal]
level: practitioner
status: draft
description: "Use the IO abstraction: gets, read, write, copy, IO::Memory buffers, STDIN/STDOUT sync, encodings and IO::MultiWriter."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IO, IO::Memory, STDIN and pipes

Goal: write IO-polymorphic code.

- Accept `IO` params, not File, so tests can pass `IO::Memory`: `io = IO::Memory.new; io << "hi"; io.to_s`.
- Read: `gets` (nil at EOF; `chomp: true` default), `gets_to_end`, `read(slice)`, `read_byte`, `each_line`, `each_char`, `read_string(n)`.
- Write: `<<`, `print`, `puts`, `write(slice)`, `write_byte`, `flush`, `sync = true` for unbuffered terminals.
- Helpers: `IO.copy(src, dst)`, `IO::MultiWriter.new(a, b)`, `IO::Delimited`, `IO::Sized`, `IO.pipe`, `IO::Stapled`, `io.set_encoding("UTF-8")`.
- STDIN loop: `while line = gets; ...; end`.

Gotchas:
- STDOUT is line buffered on TTY, otherwise fully buffered; flush before `exit!` or `Process.exec`.
- `IO::Memory#to_s` reads the whole buffer; `rewind` before re-reading.
- Closing twice is fine; reading after close raises `IO::Error`.

Verify: spec passes IO::Memory to a method that prints.
