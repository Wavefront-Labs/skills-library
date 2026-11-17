---
id: computing-software.software-engineering.nim.c-wrapper-generation-c2nim
name: c-wrapper-generation-c2nim
category: computing-software
field: software-engineering
product: nim
tags: [c-wrapper-generation-c2nim, ffi-c-interop, c2nim, futhark, nimterop, bindings, wrapper, header-translation, nim]
level: advanced
status: docs-checked
description: "Translate C headers to Nim with c2nim (preprocessor directives and --header, --cdecl, --skipinclude, --prefix, --nep1), then check importc types with completeStruct and sizeof."
sources:
  - https://github.com/nim-lang/c2nim/blob/master/doc/c2nim.rst
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Wrapping C libraries with c2nim

Goal: produce a maintainable wrapper.

- c2nim translates ANSI C/C++ (mainly header files) to human-readable Nim that is meant to be tweaked by hand. It is not a real compiler: it does not follow include files, cannot parse everything, and some constructs (Duff's device) cannot be represented in Nim.
- Use `--nep1` always: the manual advises it so generated names follow the Nim style guide.
- The preprocessor is part of the parser: `#define abc 123` becomes `const abc* = 123`. c2nim defines the symbol `C2NIM`; code in `#ifdef C2NIM` sections is seen only by c2nim, `#ifndef C2NIM` hides code from it.
- Directives (each also has a command-line option): `#skipinclude` / `--skipinclude` (skip all `#include`; otherwise a non-angle-bracket include becomes a Nim `import`), `#stdcall` / `--stdcall` and `#cdecl` / `--cdecl` (annotate every proc with the calling convention), `#header` / `--header` (annotate procs with the header pragma; exclusive with `#dynlib`), `#prefix` / `--prefix` and `#suffix` / `--suffix` (strip prefixes/suffixes), `#def` (macro that c2nim should expand like `#define`).
- After translation, review by hand. A `{.cdecl.}` procedure type uses the C calling convention (manual). For a C struct, `sizeof` at compile time on an `importc` type needs the `{.completeStruct.}` pragma, which promises the Nim definition has all the C fields; without it the compiler errors. The `checkAbi` define adds checks comparing Nim types with the C header.

Gotchas:
- The manual notes `importcpp` patterns are understood by c2nim, but you rarely need to learn them.

Verify: a minimal call into the library works and `sizeof` of key structs matches C.

## Checked

2026-11-03. Confirmed in the c2nim manual (scope, `--nep1`, `C2NIM` symbol, each directive/option above) and the Nim manual/compiler guide (`cdecl`, `completeStruct`, `checkAbi`). Removed: futhark and nimterop claims, `nimble install c2nim`, the exact `c2nim --header --cdecl mylib.h` output name, `ptr cchar` to `cstring` advice, `=destroy` wrapper advice, `static: assert sizeof(...)` example, and the bitfield/macro gotchas (macros are translated by c2nim).
Method: documentation only; no commands were run.
