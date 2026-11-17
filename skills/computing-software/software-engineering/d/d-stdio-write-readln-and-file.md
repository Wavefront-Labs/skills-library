---
id: computing-software.software-engineering.d.d-stdio-write-readln-and-file
name: d-stdio-write-readln-and-file
category: computing-software
field: software-engineering
product: d
tags: [d-stdio-write-readln-and-file, std-stdio, writeln, writefln, readln, readf, file, byline, bychunk, stderr, stdin, lockingtextwriter, d]
level: intro
status: docs-checked
description: "Print and read with writeln/writefln/stderr, readln/readf, open File with modes r w a +, iterate byLine and byChunk, and close/flush/lock behaviour."
sources:
  - https://dlang.org/phobos/std_stdio.html
  - https://dlang.org/phobos/std_format.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# writeln, writefln, readln, File open modes and byLine

Goal: standard I/O and file streams.

- Output: `write`, `writeln`, `writefln("%s=%d", k, v)`, `stderr.writeln("warn")`, `stdout.flush()`. A format spec `%(%s, %)` formats a range, e.g. `writefln("%(%s, %)", arr)`.
- Input: `readln()` returns a line; `readln(buf)` reuses a buffer. `readf!" %d"(x)` or `readf(" %d", &x)` reads with a format (the leading space is used in the page's own examples). `foreach (line; stdin.byLine)` reuses its buffer, so copy lines you keep; `byLineCopy` allocates a copy per line.
- Files: `File(name, mode)`; the default mode is `"rb"` and modes have the semantics of C `fopen`. Methods include `rawRead`, `rawWrite`, `seek`, `tell`, `size`, `flush`, `close`, `byChunk(size)`, `tmpfile`.
- `File` is reference counted: the underlying `FILE*` closes when the last `File` bound to it goes out of scope.
- Speed: `stdout.lockingTextWriter` and `setvbuf(size, mode = _IOFBF)`.
- Errors: `ErrnoException` if the file could not be opened.

Gotchas:
- Reusing the `byLine` buffer bites when you store lines.
- `rawRead` and `rawWrite` always use binary mode on Windows.

Verify: unittest writing a temp file and reading it back by line.

## Checked

2026-11-03. Confirmed against: std.stdio reference page (File constructor and modes, readf, readln, byLine, byLineCopy, rawRead/rawWrite, setvbuf, lockingTextWriter, ErrnoException).

Removed because the pages read did not confirm it: the explicit mode list (the page defers to C `fopen`), `File.tmpfile`/`f.size` semantics beyond names, the Windows newline gotcha, `scope(exit)` style advice.

Method: documentation only; no commands were run.
