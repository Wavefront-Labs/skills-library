---
id: computing-software.software-engineering.v-lang.v-bufio-and-line-reading
name: v-bufio-and-line-reading
category: computing-software
field: software-engineering
product: v-lang
tags: [v-bufio-and-line-reading, io-and-streams, bufio, buffered reader, read_line, line by line, scanner, large file, buffered writer, v-lang]
level: practitioner
status: docs-checked
description: "Wrap readers in io.BufferedReader for read_line, buffer writes with io.BufferedWriter, and process large files line by line."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bufio: buffered readers, scanners and writers

Goal: stream large inputs efficiently.

- This V tree has no `bufio` module; buffering lives in `io`.
- Read: `import io; import os; mut f := os.open(p)!; defer { f.close() }; mut r := io.new_buffered_reader(reader: f); for { line := r.read_line() or { break }; process(line) }`. `BufferedReaderConfig` has `cap` (default 128 KiB) and `retries`; `r.lines()` returns a `LineIterator`.
- Files also offer `os.read_lines(p)!` for small inputs and `f.read_bytes(n)`.
- Writer: `mut w := io.new_buffered_writer(writer: f)!` (default `cap` is 128 KiB); write with `w.write(bytes)!`; call `w.flush()!` before closing.
- `os.get_line()` returns one stdin line without its CRLF or LF ending.

Gotchas:
- Call `flush()` before closing a buffered writer.
- With the default delimiter, `read_line` accepts `\n` and `\r\n` endings and strips them; pass `delim:` to change it. It returns `io.Eof` at the end of the stream.

Verify: count lines in a generated 100 MB file with constant memory.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: io.new_buffered_reader and BufferedReaderConfig (cap, retries), BufferedReadLineConfig delim, read_line semantics and Eof, lines() (vlib/io/buffered_reader.v, lines.v), io.new_buffered_writer, BufferedWriterConfig, flush and write (vlib/io/buffered_writer.v), os.get_line (vlib/os/os.v), os.read_lines, File.read_bytes.
Removed or corrected: the whole `bufio` API (new_reader, new_writer, new_reader_size: no bufio module in vlib), the claim that os.get_line buffers, and the '(confirm)' on huge lines.
Method: documentation only; no commands were run.
