---
id: computing-software.software-engineering.r.r-paths-and-files
name: r-paths-and-files
category: computing-software
field: software-engineering
product: r
tags: [r, r-io, paths-and-files]
level: practitioner
status: docs-checked
description: "Use file.path, here::here and fs for portable paths instead of setwd."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/file.path.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/list.files.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/tempfile.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/normalizePath.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/unlink.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/files2.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# File paths and the filesystem
- `file.path()` builds paths from components; `list.files(path, pattern, full.names)` lists files (`?list.files`).
- `dir.create(path, recursive = TRUE)` creates intermediate directories (`?files2`).
- `tempfile()` and `tempdir()` give scratch locations (`?tempfile`); `normalizePath()` resolves paths (`?normalizePath`); `unlink()` deletes files and directories (`?unlink`).
Verify: Run the script from another working directory.

## Checked

Date: 2026-11-02. Confirmed on: ?file.path, ?list.files, ?files2 (dir.create recursive), ?tempfile, ?normalizePath, ?unlink. Removed as not confirmed on those pages: here::here and the setwd advice (package docs not read here).

Method: documentation only; no commands were run.
