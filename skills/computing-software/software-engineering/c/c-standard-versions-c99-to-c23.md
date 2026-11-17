---
id: computing-software.software-engineering.c.c-standard-versions-c99-to-c23
name: c-standard-versions-c99-to-c23
category: computing-software
field: software-engineering
product: c
tags: [c, c-standards-portability, c-standard-versions, c99, c11, c17, c23, std-flag]
level: practitioner
status: docs-checked
description: "Choose a C standard with -std and know what each of C99, C11, C17 and C23 adds."
sources: ["https://en.cppreference.com/w/c/99", "https://en.cppreference.com/w/c/11", "https://en.cppreference.com/w/c/23", "https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html", "https://gcc.gnu.org/onlinedocs/gcc/Standards.html", "https://clang.llvm.org/docs/UsersManual.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C standard versions c99 to c23

Goal: pick a dialect deliberately and write to it.

- Select with `-std=c99|c11|c17|c23` (GCC documents `c23` with `c2x` as the deprecated earlier name, and Clang lists C23 support; check your compiler version) or `-std=gnu11` to keep GNU extensions. Use `-pedantic-errors` to reject extensions you did not intend.
- C99: `//` comments, `inline`, `long long`, `<stdint.h>`, `<stdbool.h>`, VLAs, designated initialisers, compound literals, flexible array members, `restrict`, `__func__`, variadic macros, mixed declarations and code.
- C11: `_Static_assert`, `_Generic`, `_Alignas`/`_Alignof`, `<stdatomic.h>`, `<threads.h>`, anonymous structs/unions, `_Noreturn`, `aligned_alloc`; VLAs, threads, atomics and the Annex K bounds-checking functions became optional (feature macros `__STDC_NO_VLA__`, `__STDC_NO_THREADS__`, `__STDC_NO_ATOMICS__`, `__STDC_LIB_EXT1__`).
- C17: a bug-fix release of C11 with no new features.
- C23: `bool`/`true`/`false`, `nullptr`, `constexpr` objects, `typeof`, `#embed`, `<stdckdint.h>`, binary literals and digit separators, `static_assert` without message, empty initialiser `{}`, and `[[attributes]]`. Check compiler support tables before depending on a feature.

Verify: compile with `-std=c99 -pedantic-errors` to find accidental use of newer features.

## Checked

- Date: 2026-11-02
- Confirmed: cppreference C99 list (`//`, `restrict`, `_Bool`, `long long`, flexible array members, VLAs, designated initialisers, compound literals, mixed declarations, `inline`, `__func__`, variadic macros, `<stdint.h>`, `<stdbool.h>`); C11 list (`_Static_assert`, `_Generic`, `_Alignas`/`_Alignof`, `_Noreturn`, anonymous structs/unions, `<stdatomic.h>`, `<threads.h>`, `aligned_alloc`, feature macros); C23 list (`nullptr`, `constexpr`, `typeof`, `#embed`, `<stdckdint.h>`, binary constants, digit separator, empty initialiser, attributes, `bool` keywords, `static_assert`); GCC manual `-std` names including `c23`/`c2x`, `gnu11`, `-pedantic-errors`, and that C17 is C11 plus defect fixes; Clang manual lists C23. Removed: GCC 14/Clang 18 version numbers, the `snprintf` C99 item (not on the page), and the MSVC bullet.
Method: documentation only; no commands were run.
