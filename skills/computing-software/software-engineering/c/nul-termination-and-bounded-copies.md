---
id: computing-software.software-engineering.c.nul-termination-and-bounded-copies
name: nul-termination-and-bounded-copies
category: computing-software
field: software-engineering
product: c
tags: [c, c-strings, nul-termination, strncpy-pitfalls, strlcpy, strnlen, memcpy]
level: practitioner
status: docs-checked
description: "Copy and concatenate C strings without overflow or missing terminators; know why strncpy is not a safe strcpy."
sources: ["https://en.cppreference.com/w/c/string/byte/strncpy", "https://en.cppreference.com/w/c/io/fprintf", "https://man7.org/linux/man-pages/man3/strlcpy.3.html", "https://man7.org/linux/man-pages/man3/strnlen.3.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nul termination and bounded copies

Goal: every string buffer is bounded and terminated.

- A C string is bytes up to the first `'\0'`; buffer size must be length + 1.
- `strcpy`/`strcat` do no bounds checks. `strncpy(dst, src, n)` does NOT terminate when `strlen(src) >= n`, and pads the rest with zeros (slow for large buffers). If used, set `dst[n-1] = '\0'`.
- Preferred: `snprintf(dst, sizeof dst, "%s", src)` and check the return value (>= size means truncation). `strlcpy`/`strlcat` are in POSIX.1-2024 and glibc 2.38 (man7 lists OpenBSD 2.4 as the origin); do not assume them on older systems.
- Use `strnlen(s, max)` (POSIX.1-2008) for possibly unterminated data; `memcpy` with explicit lengths for binary data, including embedded NULs.
- `sizeof` of a pointer parameter is not the buffer size; carry the capacity.
- Concatenation in loops is O(n^2) with `strcat`; track the end pointer.

Verify: run tests with `-fsanitize=address` using inputs of length size-1, size and size+1.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference strncpy (no terminator when the source is not shorter than n; zero padding) and snprintf return value; man7 strlcpy(3) (HISTORY: OpenBSD 2.4, POSIX.1-2024, glibc 2.38) and strnlen(3) (POSIX.1-2008 via `_POSIX_C_SOURCE >= 200809L`). Removed: the macOS claim and the 'not in ISO C through C17' claim.
Method: documentation only; no commands were run.
