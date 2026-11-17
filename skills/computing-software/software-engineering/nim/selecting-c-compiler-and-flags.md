---
id: computing-software.software-engineering.nim.selecting-c-compiler-and-flags
name: selecting-c-compiler-and-flags
category: computing-software
field: software-engineering
product: nim
tags: [selecting-c-compiler-and-flags, compiler-commands-and-backends, cc, gcc, clang, vcc, zigcc, passc, passl, compiler-selection, linker, nim]
level: practitioner
status: docs-checked
description: "Select gcc, clang, vcc or zig cc with --cc, pass flags with --passC/--passL, and read the generated build commands."
sources:
  - https://nim-lang.org/docs/nimc.html
  - https://nim-lang.org/docs/manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing the C compiler and passing flags

Goal: control the C toolchain.

- `--cc:SYMBOL` selects the C compiler (for example `gcc`, `clang`, `vcc`); `--cc:env` reads the `CC` variable for `nim c` and `CXX` for `nim cpp` (since Nim 1.4).
- Add flags: `--passC:OPTION` (`-t`), `--passL:OPTION` (`-l`), `--cincludes:DIR`, `--clibdir:DIR`, `--clib:LIBNAME`.
- Compiler path override goes in config as `<compiler>.exe` and `<compiler>.linkerexe`, for example `gcc.exe` and `gcc.linkerexe` (the compiler guide shows `arm.linux.gcc.exe`).
- `--listCmd` lists the compilation commands (combine with `--hint:exec:on` and `--hint:link:on`); `--debuginfo:on|off` enables debug information; `--lineDir:on|off` controls `#line` directives.
- `--genScript:on|off` generates a compile script in the nimcache; the guide's cross-compile example is `nim c --cpu:i386 --os:linux --compileOnly --genScript myproject.nim`.

Gotchas:
- Changing compiler for the same project: add `-f` so nimcache is rebuilt.

Verify: `--listCmd` output shows your extra flags.

## Checked

2026-11-02. Confirmed against advopt.txt (`--cc`, `--passC`, `--passL`, `--cincludes`, `--clibdir`, `--clib`, `--listCmd`, `--debuginfo`, `--lineDir`, `--genScript`) and nimc.md (`--cc:env`, `.exe`/`.linkerexe`, `-f`, genScript example). Removed: icc/tcc list, zig wrapper line, the MinGW/vcc and `-march=native` gotchas, `-g` shorthand (not in the option help).
Method: documentation only; no commands were run.
