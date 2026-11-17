---
id: computing-software.software-engineering.nim.terminal-io-and-files
name: terminal-io-and-files
category: computing-software
field: software-engineering
product: nim
tags: [terminal-io-and-files, stdlib-os-and-paths, readfile, writefile, open, readline, lines, stdin, streams, file-io, nim]
level: intro
status: docs-checked
description: "Read and write text and binary files with readFile, writeFile, open, lines, readLine and the standard streams."
sources:
  - https://nim-lang.org/docs/syncio.html
  - https://nim-lang.org/docs/terminal.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading and writing files and standard I/O

Goal: do file and console I/O.

- Whole file: `let s = readFile("a.txt")`, `writeFile("b.txt", s)`.
- Line loop: `for line in lines("a.txt"): ...` or `let f = open("a.txt"); defer: f.close(); while f.readLine(line): ...`.
- Modes: `fmRead`, `fmWrite`, `fmAppend`, `fmReadWrite`; binary: `readBytes`, `writeBytes`, `readBuffer`.
- Console: `stdin.readLine()`, `readLine(stdin)`, `echo`, `stdout.write`, `stderr.writeLine`, `flushFile(stdout)`.
- `std/syncio` is the module that documents these file and console procs.

Gotchas:
- `readFile` loads everything in memory.

Verify: round-trip writeFile then readFile returns identical text.

## Checked

2026-11-03. Confirmed against the syncio page: readFile, writeFile, lines, open(f, filename, mode), readLine, readBytes, writeBytes, readBuffer, flushFile, FileMode values fmRead/fmWrite/fmAppend/fmReadWrite, stdin/stdout/stderr. Removed: the std/streams line and the open-failure behaviour claim (not read from official pages).

Method: documentation only; no commands were run.
