---
id: computing-software.software-engineering.d.d-file-direntries-and-paths
name: d-file-direntries-and-paths
category: computing-software
field: software-engineering
product: d
tags: [d-file-direntries-and-paths, std-file, direntries, spanmode, glob, std-path, buildpath, basename, dirname, extension, withextension, absolutepath, globmatch, d]
level: practitioner
status: docs-checked
description: "Walk directories with dirEntries (SpanMode, glob), and build portable paths with buildPath, baseName, dirName, extension, withExtension, absolutePath, globMatch."
sources:
  - https://dlang.org/phobos/std_file.html
  - https://dlang.org/phobos/std_path.html
  - https://dlang.org/phobos/std_process.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Directory traversal with dirEntries and path manipulation (std.path)

Goal: list files and handle paths portably.

- `dirEntries(path, pattern, SpanMode, followSymlink)` returns a lazy input range of `DirEntry`; `followSymlink` defaults to true. `pattern` is a wildcard string such as `"*.d"` (see `std.path.globMatch`). Entry order is whatever the filesystem returns.
- `SpanMode.shallow` spans one directory; `depth` is depth-first post-order (a directory's contents before the directory itself, handy for deleting); `breadth` is depth-first pre-order and is not a true breadth-first traversal.
- Combine with ranges: `dirEntries(".", SpanMode.depth).filter!(e => e.isFile)`.
- `std.path`: `buildPath`, `buildNormalizedPath`, `baseName`, `dirName`, `extension` (includes the dot), `stripExtension`, `withExtension`, `setExtension`, `isAbsolute`, `absolutePath`, `relativePath`, `expandTilde`, `pathSplitter`, `driveName`, `isValidFilename`, `globMatch`.
- `std.process.environment`, `thisExePath` (std.file).

Gotchas:
- `dirEntries` throws `FileException` for a bad directory; sort entries yourself when order matters.

Verify: unittest creating a temp tree and checking the listing with sorted names.

## Checked

2026-11-03. Confirmed against: std.file (dirEntries, SpanMode, DirEntry), std.path and std.process reference pages.

Removed because the pages read did not confirm it: `extension` returns empty for dotfiles, `\\` hard-coded-separator advice, `FileException` mid-iteration permission claim, `isFile` filter example kept as an idiom.

Method: documentation only; no commands were run.
