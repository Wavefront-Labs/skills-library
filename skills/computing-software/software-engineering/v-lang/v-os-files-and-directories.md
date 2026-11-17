---
id: computing-software.software-engineering.v-lang.v-os-files-and-directories
name: v-os-files-and-directories
category: computing-software
field: software-engineering
product: v-lang
tags: [v-os-files-and-directories, os-module, os, read_file, write_file, ls, walk, mkdir_all, file io, join_path, file, v-lang]
level: practitioner
status: docs-checked
description: "Use os.read_file, write_file, open, create, ls, walk, mkdir_all, rm and path helpers with result-based error handling."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading, writing and walking files

Goal: do file system work with `import os`.

- Whole file: `s := os.read_file(path)!`; `os.write_file(path, data)!`; lines: `os.read_lines(path)!`.
- Streams: `mut f := os.open(path)!`, `defer { f.close() }`, `f.read_bytes(n)`; create/append: `os.create(path)!`, `os.open_append(path)!`; `f.writeln('x')!`.
- Dirs: `os.ls(dir)!`, `os.mkdir_all(p)!`, `os.rmdir_all(p)!`, `os.rm(file)!`, `os.cp(a, b)!`, `os.mv(a, b)!`, `os.walk(dir, fn (p string) { ... })`, `os.walk_ext(dir, '.v')`.
- Checks: `os.exists(p)`, `os.is_dir(p)`, `os.is_file(p)`, `os.file_size(p)`, `os.file_last_mod_unix(p)`.
- Paths: `os.join_path(a, b)`, `os.dir(p)`, `os.base(p)`, `os.file_ext(p)`, `os.abs_path(p)`, `os.home_dir()`, `os.temp_dir()`, `os.getwd()`, `os.chdir(d)!`.

Gotchas:
- Build paths with `os.join_path(base, ...dirs)` rather than concatenating separators.
- `os.ls(path)!` returns a `[]string` of entries.
- Close files you open; `read_file` returns the whole content as one string.

Verify: write, read back, delete a temp file in a test.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: signatures of os.read_file, write_file, read_lines, open, create, open_append, ls, mkdir_all, rmdir_all, rm, cp, mv, walk, walk_ext, exists, is_dir, is_file, file_size, file_last_mod_unix, join_path, dir, base, file_ext, abs_path, home_dir, temp_dir, getwd, chdir; File.read_bytes, writeln, write_string (vlib/os).
Removed or corrected: 'os.ls returns names not full paths and unordered' (the ordering and path form are not documented in the source read) and the 'loads everything in memory' warning (reworded to what the signature says).
Method: documentation only; no commands were run.
