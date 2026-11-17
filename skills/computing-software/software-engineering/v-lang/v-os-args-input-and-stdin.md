---
id: computing-software.software-engineering.v-lang.v-os-args-input-and-stdin
name: v-os-args-input-and-stdin
category: computing-software
field: software-engineering
product: v-lang
tags: [v-os-args-input-and-stdin, os-module, os.args, os.input, stdin, get_line, command line arguments, argv, stdout, stderr, v-lang]
level: intro
status: docs-checked
description: "Read os.args, prompt with os.input, read stdin lines with os.get_line and os.get_raw_lines_joined, and write to stderr."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Command-line args and standard input

Goal: build simple console programs.

- `os.args` is `[]string`, index 0 is the program; `os.args[1..]` are user arguments. For flags use the `flag` module.
- Prompt: `name := os.input('Name: ')` (prints the prompt, strips the trailing CR/LF, returns `<EOF>` at end of input); `os.input_opt` returns `?string` instead.
- Loop stdin: `for { line := os.get_line(); if line.len == 0 { break } ... }`, or whole stdin `os.get_raw_lines_joined()`.
- `os.stdin().read_bytes(n)` for binary; `os.stdout().write_string(s)!`; errors to `eprintln`.
- `os.get_line()` returns one line from stdin with its CRLF or LF removed; `os.get_raw_line()` keeps the ending, so use it to tell a blank line from the end of input.
- Terminal detection: `os.is_atty(0)` returns an `int`.

Gotchas:
- `os.input` returns the string `<EOF>` when input ends, so check for it in scripts and CI.

Verify: `echo 3 | v run sum.v` reads the number.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: os.args as a constant array (vlib/os/os.c.v), input/input_opt behaviour and doc comments, get_line, get_raw_line, get_raw_lines_joined, is_atty, stdin()/stdout() and File.read_bytes/write_string (vlib/os).
Removed or corrected: 'os.input blocks forever', 'EOF returns an empty string' wording, the Windows console encoding gotcha, and '(confirm)' markers.
Method: documentation only; no commands were run.
