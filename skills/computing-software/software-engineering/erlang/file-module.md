---
id: computing-software.software-engineering.erlang.file-module
name: file-module
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-files, file-module]
level: practitioner
status: docs-checked
description: "Erlang file module: read_file, write_file, open with raw and read_ahead, read_line, consult, list_dir and posix error atoms."
sources:
  - https://www.erlang.org/doc/apps/kernel/file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The file module
**Goal:** read and write files safely and efficiently.

```erlang
{ok, Bin} = file:read_file("data.bin"),
ok = file:write_file("out.txt", [<<"line">>, $\n]),
{ok, Fd} = file:open("big.log", [read, binary, raw, {read_ahead, 65536}]),
{ok, Line} = file:read_line(Fd), ok = file:close(Fd),
{ok, Terms} = file:consult("config.terms"),
{ok, Names} = file:list_dir("."),
{error, enoent} = file:read_file("missing").
```
- Errors are `{error, Reason}` with POSIX atoms such as `enoent` (does not exist), `eacces` (missing permissions) and `eexist`; `file:format_error/1` turns a reason into text.
- `raw` allows faster access because no Erlang process handles the file, but the `io` module functions cannot be used on a raw file (use `read/2`, `read_line/1`, `write/2`) and a remote file server cannot be used. Combine `raw` with `{read_ahead, Size}` when using `read_line/1`.
- A normal (non-raw) file is a process usable as an I/O device; writing copies data that is not binary, so open in binary mode and write binaries.
- `file:write_file(File, Data, [append])` appends (`write_file/3` takes modes); `file:rename/2` renames a file.
- Stream large files with `read_line` or `read/2` in chunks instead of `read_file`.

## Gotchas
- Close files you open; the `read_ahead` and `delayed_write` options reduce OS calls for small reads and writes.

## Self-check
Write then read a file, and handle the `enoent` error path.

## Checked

2026-11-03. Confirmed in the `file` module page: `read_file`, `write_file/2,3`, `open/2` modes (`raw`, `binary`, `append`, `read_ahead`), `read_line/1`, `consult/1`, `list_dir/1`, `rename/2`, `format_error/1`, error atoms and the raw-mode limitations. Removed: the "process closes when the owner dies" statement, the descriptor-leak claim, and the atomic temp-file-then-rename advice (the page says renames are only atomic through the same file server and may not be on Windows).
Method: documentation only; no commands were run.
