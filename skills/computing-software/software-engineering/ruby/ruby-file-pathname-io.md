---
id: computing-software.software-engineering.ruby.ruby-file-pathname-io
name: ruby-file-pathname-io
category: computing-software
field: software-engineering
product: ruby
tags: [ruby, ruby-io-security, file-pathname-io]
level: practitioner
status: docs-checked
description: "Read and write files with File, Pathname, block forms and explicit encodings."
sources: ["https://docs.ruby-lang.org/en/master/File.html", "https://docs.ruby-lang.org/en/master/Pathname.html", "https://docs.ruby-lang.org/en/master/Dir.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File and Pathname IO
- `File.open` with a block yields the file and closes it on exit from the block; `File.rename` moves a file; `File.expand_path` returns the absolute path, expanding `~`; `Kernel#__dir__` gives the directory of the current method's file.
- `Pathname` has core methods `+`, `join`, `children`, `parent`, `cleanpath`, `relative_path_from`.
- `String#force_encoding` changes the encoding label in place; `String#encode` transcodes.
Verify: tests using a temporary directory.

## Checked
2026-11-02. Confirmed against: File, Pathname, String and Kernel pages. Removed or softened (not stated on those pages): File.read/foreach/write option details, rb mode, mktmpdir, atomic-write advice.
Method: documentation only; no commands were run.
