---
id: computing-software.software-engineering.crystal.file-api
name: file-api
category: computing-software
field: software-engineering
product: crystal
tags: [file-api, stdlib-io-files, file, file-read, file-write, file-open, each-line, file-info, file-exists, tempfile, append, crystal]
level: intro
status: docs-checked
description: "Read and write files with File.read, File.open blocks, each_line, write, append mode, info, permissions, rename and delete."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/crystal/tree/master/src
  - https://github.com/crystal-lang/crystal-book/tree/master/docs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File reading, writing and metadata

Goal: do file IO safely.

- Whole file: `File.read(path)`, `File.write(path, str)`, `File.read_lines(path)`, `File.exists?`, `File.size`, `File.info(path)` (mtime, permissions, size).
- Streaming: `File.open(path, "r") { |f| f.each_line { |l| ... } }` closes automatically; `File.new` needs manual `close`.
- Manipulate: `File.rename`, `File.copy`, `File.delete`, `File.chmod`, `File.symlink`, `File.basename`, `File.extname`, `File.dirname`, `File.join`, `File.expand_path`, `File.tempfile(suffix) { |f| ... }` (or `File.tempfile(prefix, suffix)`).
- Errors: `File::NotFoundError` and `File::AccessDeniedError` subclass `File::Error` (an `IO::Error`).

Gotchas:
- `File.read` loads everything into memory; stream large files.
- Always use the block form to avoid leaked descriptors.
- Writes are buffered; `flush` or close before reading elsewhere. `File.write(path, content, perm:, mode: "a")` appends.

Verify: spec writes then reads a tempfile.

## Checked

Date 2026-11-03. Confirmed File.read, write (perm and mode parameters), read_lines, open with block, new, info, size, chmod, delete, rename, copy, symlink, extname, expand_path, tempfile (suffix and prefix forms) and the File::NotFoundError and File::AccessDeniedError classes in the File source. Removed the unlisted mode list and tightened the error hierarchy.

Method: documentation only; no commands were run.
