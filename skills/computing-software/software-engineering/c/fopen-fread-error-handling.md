---
id: computing-software.software-engineering.c.fopen-fread-error-handling
name: fopen-fread-error-handling
category: computing-software
field: software-engineering
product: c
tags: [c, c-stdio, stdio-error-handling, fopen, fread, ferror, feof, fclose]
level: practitioner
status: docs-checked
description: "Check every stdio call, tell EOF from error with feof/ferror, and report failures with strerror."
sources: ["https://en.cppreference.com/w/c/io/fread", "https://en.cppreference.com/w/c/io/fgets", "https://en.cppreference.com/w/c/io/fopen", "https://man7.org/linux/man-pages/man3/fgetc.3.html", "https://man7.org/linux/man-pages/man2/rename.2.html", "https://man7.org/linux/man-pages/man4/full.4.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fopen fread error handling

Goal: file code that fails loudly and correctly.

- `FILE *f = fopen(path, "rb");` returns NULL on failure with `errno` set; report with `fprintf(stderr, "%s: %s\n", path, strerror(errno));`.
- `fread(buf, 1, n, f)` returning less than `n` means EOF or error; distinguish with `feof(f)` vs `ferror(f)`. Never loop on `while (!feof(f))` before reading; test the read's return value.
- `fgets(buf, size, f)` returns NULL at EOF/error; a missing `'\n'` in the buffer means the line was truncated.
- `getchar`/`fgetc` return `int`: store in `int` to compare with `EOF`, not `char`.
- Writes are buffered: errors may only show at `fflush` or `fclose`; check `fclose`'s return when writing.
- Atomic file replace: write to temp in the same directory, `fflush`, `fsync(fileno(f))` (POSIX), close, then `rename()`.
- Open binary data with "b" (matters on Windows).

Verify: test with a read-only file, a directory path, a full disk (`/dev/full` on Linux) and an empty file.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference fread (short count, callers use `feof`/`ferror`), fgets (stops at newline or EOF), fopen (mode `b` has no effect on POSIX, matters on Windows); man7 fgetc (returns an `int`, EOF at end of file or error), rename(2) (atomic replace), full(4) (`/dev/full` fails with ENOSPC). Nothing removed.
Method: documentation only; no commands were run.
