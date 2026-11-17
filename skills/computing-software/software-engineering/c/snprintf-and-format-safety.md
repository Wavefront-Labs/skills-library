---
id: computing-software.software-engineering.c.snprintf-and-format-safety
name: snprintf-and-format-safety
category: computing-software
field: software-engineering
product: c
tags: [c, snprintf, printf-format, format-specifiers, truncation-detection]
level: practitioner
status: docs-checked
description: "Build strings with snprintf, detect truncation and match every printf conversion to its argument type."
sources: ["https://en.cppreference.com/w/c/io/fprintf", "https://man7.org/linux/man-pages/man3/printf.3.html", "https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html", "https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Common-Function-Attributes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snprintf and format safety

Goal: formatted output that cannot overflow and has no type mismatches.

- `int n = snprintf(buf, sizeof buf, "%s-%d", name, id);` returns the length that WOULD have been written; `n < 0` is an encoding error; `(size_t)n >= sizeof buf` means truncated. `snprintf(NULL, 0, ...)` measures the needed size.
- Never use `sprintf`/`vsprintf` on unbounded data.
- Specifiers must match types: `%d` int, `%u` unsigned, `%zu` size_t, `%td` ptrdiff_t, `%lld` long long, `%p` with a `(void *)` cast, `%c` int, `%s` needs a terminated `char *`. Mismatches are UB.
- `%n` writes the count of characters so far through a pointer; avoid it entirely.
- Enable `-Wformat -Wformat-security` and mark your own printf-like wrappers with `__attribute__((format(printf, 1, 2)))` (GCC).
- Never pass user input as the format string: `printf(user)` is a vulnerability; use `printf("%s", user)`.

Verify: compile with `-Wformat=2` and test truncation by shrinking the buffer.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference fprintf (snprintf returns the length that would have been written, negative on encoding error, `bufsz` of zero writes nothing and the buffer may be null; `%zu`, `%td`, `%p` takes `void *`, `%n` is a security risk); GCC manual `-Wformat`, `-Wformat-security`, `-Wformat=2` and the `format` attribute. Removed: the Clang claim for the format attribute (not on the page read).
Method: documentation only; no commands were run.
