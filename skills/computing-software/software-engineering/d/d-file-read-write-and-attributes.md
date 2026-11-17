---
id: computing-software.software-engineering.d.d-file-read-write-and-attributes
name: d-file-read-write-and-attributes
category: computing-software
field: software-engineering
product: d
tags: [d-file-read-write-and-attributes, std-file, readtext, read, write, append, exists, isfile, isdir, remove, rename, copy, getsize, timelastmodified, d]
level: intro
status: docs-checked
description: "Read and write whole files with readText/read/write/append, check exists/isFile/isDir, copy, rename, remove, getSize, timeLastModified and attributes."
sources:
  - https://dlang.org/phobos/std_file.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# std.file: read, write, readText, append, exists, remove, rename, copy, stat

Goal: whole-file I/O and file metadata.

```d
import std.file;
write("a.txt", "hello\n");          // creates/truncates
append("a.txt", "more\n");
string t = readText("a.txt");       // validates UTF-8
ubyte[] raw = cast(ubyte[]) read("a.bin");
```
- `readText` reads and validates (with `std.utf.validate`) a text file; it throws `FileException` on read errors and `std.utf.UTFException` on decoding errors.
- Check: `exists`, `isFile`, `isDir`, `isSymlink`, `getSize`, `timeLastModified`, `getTimes`, `setTimes`, `attrIsDir(getAttributes(p))`.
- Operate: `copy`, `rename`, `remove`, `rmdir`, `rmdirRecurse`, `mkdir`, `mkdirRecurse`, `symlink`, `readLink`, `chdir`, `getcwd`, `tempDir`, `slurp`.
- Errors: failures throw `FileException`.
- For big files use `std.stdio.File` (`byLine`, `byChunk`) rather than reading whole files.

Gotchas:
- `readText` fails on invalid UTF-8; use `read` and handle the bytes yourself.

Verify: unittest in a temp directory under `tempDir`, cleaned with `rmdirRecurse`.

## Checked

2026-11-03. Confirmed against: std.file reference page.

Removed because the pages read did not confirm it: `truncate` (not on the page), the non-atomic `write` advice, the mmfile and `std.encoding` advice, the temp-dir test recipe detail.

Method: documentation only; no commands were run.
