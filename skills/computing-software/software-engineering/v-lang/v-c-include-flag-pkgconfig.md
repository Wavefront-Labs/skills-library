---
id: computing-software.software-engineering.v-lang.v-c-include-flag-pkgconfig
name: v-c-include-flag-pkgconfig
category: computing-software
field: software-engineering
product: v-lang
tags: [v-c-include-flag-pkgconfig, c-interop, include, flag, pkgconfig, c headers, linker flags, -l, -i, c interop, v-lang]
level: practitioner
status: docs-checked
description: "Include C headers and set compiler and linker flags per OS with #include, #flag and #pkgconfig directives, guarded with $pkgconfig."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# #include, #flag and #pkgconfig

Goal: tell V how to build against a C library.

- `#include <stdio.h>` only appears in the generated C code. V has no C parser, so it knows nothing about the header's declarations; redeclare the functions and structs you use in `.c.v` files with the `C.` prefix, for example `fn C.dprintf(fd int, const_format &char, ...voidptr) int`.
- `#flag` directives at the top of a V file pass `-I` (include paths), `-l` (libraries), `-L` (library paths) and `-D` (defines). Each flag goes on its own line.
- Per OS: `#flag linux -lsdl2`, `#flag linux -Ivig`, `#flag freebsd -I/usr/local/include -L/usr/local/lib`.
- Local sources: `#flag "@VMODROOT/my_test_cshim.c"`. Lowercase `.c` compiles as C; `.C`, `.cc` and `.cpp` compile as C++. Static libraries: `#flag /path/to/ffi.a`; `@START_LIBS` on a flag prepends it to the libs section.
- `#pkgconfig sqlite3` or `#pkgconfig --cflags --libs r_core`. With no flags V adds `--cflags` and `--libs`. `PKG_CONFIG_PATH` adds search paths; several modules may be listed.
- If `pkg-config` is missing or the package unknown, the directive yields no flags and reports nothing; the build fails later on a missing header or symbol. Guard it: `$if $pkgconfig('mysqlclient') { #pkgconfig mysqlclient } $else $if $pkgconfig('mariadb') { #pkgconfig mariadb }` and give fallback `#flag` lines in `$else`.
- `$env('VAR')` and `$d('name','default')` can appear in `#flag` lines, for example `#flag linux -I $env('JAVA_HOME')/include`.
- `-cflags`, `-ldflags` and `-cc` on the command line, or a `VFLAGS` environment variable, add compiler and linker flags.

Gotchas:
- Missing dev headers cause C compiler errors, not V errors.
- Sources and headers outside the V install, or `#pkgconfig`, bypass V's module and whole-program caches (`v crun` and `.vsh` rebuild each run).

Verify: `v -showcc .` prints the C command line with your flags, and `-dump-c-flags -` prints the selected flags.

## Checked

2026-11-08. Read: the "V and C" sections of doc/docs.md (vlang/v) covering "Calling C from V", "Passing C compilation flags" and "#pkgconfig", plus the comptime `$env`/`$d` lines. Removed: `#insert` and `$if` embedding advice, `@VMODROOT/c` header-search example, `#flag -lm`/`-framework Cocoa` examples that were not shown, and `.o` flag example. docs.vlang.io, modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
