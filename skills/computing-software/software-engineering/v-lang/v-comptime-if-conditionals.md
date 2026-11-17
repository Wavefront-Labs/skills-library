---
id: computing-software.software-engineering.v-lang.v-comptime-if-conditionals
name: v-comptime-if-conditionals
category: computing-software
field: software-engineering
product: v-lang
tags: [v-comptime-if-conditionals, compile-time-programming, if, comptime, conditional-compilation, platform, flag, v-lang]
level: practitioner
status: docs-checked
description: "Select V code per OS, compiler, platform or -d flag with $if/$else, use builtin option names, custom ? flags and platform file suffixes like _windows.c.v."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile-time $if conditionals

Goal: write portable code with compile-time branches.

```v
$if ios || android { println('mobile') }
$if linux && x64 { println('64-bit Linux') }
os := $if windows { 'Windows' } $else { 'UNIX' }
$if option ? { println('custom option') }   // v -d option
```

- An `if` is compile-time only when prefixed with `$`. It detects an OS, compiler, platform or compilation option. `$else $if` chains are allowed, and `$if` can be used as an expression.
- Builtin names per the docs table: OS `windows linux macos darwin ios bsd freebsd openbsd netbsd android` and more; compilers `gcc tinyc clang mingw msvc cplusplus`; platforms `amd64 arm64 aarch64 i386 arm32 rv64 rv32 s390x ppc64le x64 x32 little_endian big_endian`; other `debug prod test js glibc prealloc no_bounds_checking freestanding no_segfault_handler no_backtrace no_main fast_math apk threads js_node js_browser js_freestanding interpreter es5 profile wasm32 wasm32_emscripten wasm32_wasi native autofree`.
- `$if debug` is true when compiled with `v -g` or `v -cg`; `$if prod` with `v -prod`.
- A custom ifdef needs the trailing `?` in `$if option ? {}` and compiling with `v -d option`.
- Files with an environment suffix compile only there: `.js.v` (JS backend), `.c.v` (C backend), `.native.v`, `_nix.c.v` (non Windows), `_bsd.c.v`, `_${os}.c.v` (for example `_windows.c.v` when compiling on Windows or with `-os windows`), and `_default.c.v` (only if no more specific file exists).
- On a function, `@[if trace_logs ?]` removes the function and its calls unless `-d trace_logs` is passed; V still type checks them.
- Inside `$for` reflection loops, `$if field.typ is string` is decided per item at compile time.

Gotchas:
- In a compile-time condition, mutable locals stay runtime and using one is an error (reflection-loop rule in the docs).
- Use `?` for user flags, as the docs show.

Verify: `v -os windows .` and `v -os linux .` select different branches (cross compiling needs a toolchain; see the cross-compiling skill).

## Checked

Confirmed against the "Conditional compilation" and "Compile time if" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: the claim that dead branches are only parsed, silent-false behaviour for misspelt names, the "expression statement" gotcha, `gcboehm` as a name (not in the table read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
