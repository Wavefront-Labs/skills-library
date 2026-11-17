---
id: computing-software.software-engineering.v-lang.v-compile-time-constants-and-defines
name: v-compile-time-constants-and-defines
category: computing-software
field: software-engineering
product: v-lang
tags: [v-compile-time-constants-and-defines, const-and-globals, compile-time-define, pseudo-variables, build-flags, v-lang]
level: advanced
status: docs-checked
description: "Pass flags with -d name=value, read them with $d(), branch with $if name ? {}, read $env() at compile time, and use pseudo variables such as @FILE and @LINE."
sources:
  - https://raw.githubusercontent.com/vlang/v/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile-time constants and -d defines

Goal: configure builds without code changes.

- Custom flags: build with `v -d option ...` and test with `$if option ? { ... }`. The trailing `?` is required for custom ifdefs. Built-in options (`debug`, `prod`, `windows`, ...) need no `?`.
- `$if debug` is enabled when compiled with `v -g` or `v -cg`; `prod` corresponds to `v -prod`.
- Builtin options listed in the docs table: OS (`windows`, `linux`, `macos`, `darwin`, `freebsd`, `android`, and others); compilers (`gcc`, `tinyc`, `clang`, `mingw`, `msvc`, `cplusplus`); platforms (`amd64`, `arm64`, `x64`, `x32`, `little_endian`, ...); other (`debug`, `prod`, `test`, `js`, `glibc`, `prealloc`, `no_bounds_checking`, `freestanding`, `autofree`, `threads`, `wasm32`, ...).
- Value defines: `v -d my_i64=4096 -d my_string="V rocks" run .` and in code `$d('my_i64', 1024)`. `-d ident` alone means `-d ident=true`. The default (second argument) is returned when no flag is given and must be a pure literal: `false` for booleans, an integer for i64, a float for f64, a string, or a char.
- `$d('ident', false)` also works inside `$if $d('ident', false) { ... }` to turn code sections on or off, and in top-level `#flag`/`#include` (default must then be a string literal).
- `$env('NAME')` brings an environment variable in at compile time, and can be used in `#flag`/`#include` lines.
- Pseudo variables substituted at compile time include `@FN`, `@METHOD`, `@MOD`, `@STRUCT`, `@FILE` (absolute path), `@DIR`, `@LINE`, `@FILE_LINE`, `@LOCATION`, `@COLUMN`, `@VEXE`, `@VEXEROOT`, `@VHASH`, `@VCURRENTHASH`, `@VMOD_FILE`, `@VMODHASH`, `@VMODROOT`, `@BUILD_DATE`, `@BUILD_TIME`, `@BUILD_TIMESTAMP`. Build date and time are UTC; the docs suggest setting `SOURCE_DATE_EPOCH` for reproducible builds.

Verify: build twice with different `-d` values and compare output.

## Checked
2026-11-08. Checked against the V language documentation (`doc/docs.md` from the vlang/v repository, the source behind docs.vlang.io): compile-time `$if`, builtin options table, `$env`, `$d`, and the pseudo variable list. Removed: `gcboehm` as a builtin condition (not in the table), the claim that unknown `-d` flags without `?` are a compile error, and "confirm exact set" hedging (the set is now listed). The generic landing pages docs.vlang.io, modules.vlang.io and the repo root were replaced by the raw docs file.
Method: documentation only; no commands were run.
