---
id: computing-software.software-engineering.c.feature-test-macros-posix-gnu-source
name: feature-test-macros-posix-gnu-source
category: computing-software
field: software-engineering
product: c
tags: [c, feature-test-macros, posix-c-source, gnu-source, default-source, implicit-declaration]
level: advanced
status: docs-checked
description: "Request POSIX and GNU APIs with feature test macros and fix implicit-declaration errors under -std=c11."
sources: ["https://en.cppreference.com/w/c", "https://www.open-std.org/jtc1/sc22/wg14/", "https://gcc.gnu.org/onlinedocs/", "https://man7.org/linux/man-pages/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Feature test macros posix gnu source

Goal: get declarations like `strdup`, `getline`, `clock_gettime` without silent breakage.

- Strict `-std=c11` hides POSIX/GNU declarations in glibc. Define a macro BEFORE any system header: `#define _POSIX_C_SOURCE 200809L` (POSIX.1-2008) or `#define _GNU_SOURCE` (all GNU/Linux extensions; the accept4(2) and getrlimit(2) synopses show `#define _GNU_SOURCE`), or pass `-D_POSIX_C_SOURCE=200809L` on the command line.
- Without them, calling `strdup` gives "implicit declaration"; GCC 14 makes implicit function declarations an error by default, and Porting to GCC 14 describes this exact `-std=c11` case. Fix the include/macro rather than casting.
- Putting `_GNU_SOURCE` in a header rarely works (include order); put it in the build flags.
- Other platforms use different macros; on Linux the available ones are listed in `feature_test_macros(7)`.
- Use `-std=gnu11` for convenience in applications, `-std=c11 -D_POSIX_C_SOURCE=200809L` for portable POSIX code.

Verify: compile with `-Werror=implicit-function-declaration -std=c11` and check each missing declaration resolves with the right macro.

## Checked

2026-11-02. Confirmed in feature_test_macros(7), open(2), accept(2), Porting to GCC 14 and GCC Standards: `_POSIX_C_SOURCE >= 200809L`, `_GNU_SOURCE` in synopses, `-Werror=implicit-function-declaration` in GCC 14, `-std=gnu11`. Removed: the `pipe2`/`memmem`/`asprintf` list, the C99-removal and Clang claims, and the non-Linux macro list.

Method: documentation only; no commands were run.
