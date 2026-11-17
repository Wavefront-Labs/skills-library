---
id: computing-software.software-engineering.scheme-racket.file-io
name: file-io
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, file-io]
level: practitioner
status: docs-checked
description: "Read and write files with call-with-input-file, call-with-output-file, file->string, file->lines, display-to-file, #:exists modes."
sources:
  - https://docs.racket-lang.org/reference/Filesystem.html
  - https://docs.racket-lang.org/reference/file-ports.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading and writing files
**Goal:** file handling without leaks.
```racket
(require racket/file)
(display-to-file "text" "out.txt" #:exists 'replace)
(file->string "out.txt")
(call-with-output-file "o.txt" #:exists 'append (lambda (o) (displayln "x" o)))
(with-input-from-file "o.txt" read-line)
```
- Output to an existing file errors unless `#:exists` is set (`'replace`, `'append`, `'truncate`, ...).
- Use `call-with-*` forms so ports close on exit.
- File is created in `current-directory`.
## Self-check
Write twice without `#:exists` to see the exists error.

## Checked

2026-11-02. Confirmed against the Racket Reference, Guide, Foreign Interface, raco and pkg manuals at docs.racket-lang.org (pages named in sources): the functions, keywords, flags and behaviours stated above. Removed or corrected claims the pages did not support (see the version history). Example outputs are illustrative.

Method: documentation only; no commands were run.
