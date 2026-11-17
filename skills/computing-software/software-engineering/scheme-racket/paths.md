---
id: computing-software.software-engineering.scheme-racket.paths
name: paths
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, paths, racket-system]
level: practitioner
status: docs-checked
description: "Build and inspect file paths with build-path, path->string, file-exists?, directory-list, make-directory*, delete-file and find-system-path."
sources:
  - https://docs.racket-lang.org/reference/Filesystem.html
  - https://docs.racket-lang.org/reference/Manipulating_Paths.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Paths and directories
**Goal:** portable file system code.
```racket
(build-path "a" "b.txt")
(directory-list "." #:build? #t)
(make-directory* "out/deep")
(find-system-path 'home-dir)
(path->string (simplify-path "a/../b"))
```
- Never concatenate paths with `/` strings for portability; use `build-path`.
- `racket/file` provides `delete-directory/files`, `copy-directory/files`, `file->lines`.
## Self-check
`(path->string (build-path "a" "b"))` is `"a/b"` on Unix-like systems.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
