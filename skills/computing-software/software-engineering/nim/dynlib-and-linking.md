---
id: computing-software.software-engineering.nim.dynlib-and-linking
name: dynlib-and-linking
category: computing-software
field: software-engineering
product: nim
tags: [dynlib-and-linking, ffi-c-interop, dynlib, passc, passl, compile, link, shared-library, static-library, loadlib, nim]
level: advanced
status: docs-checked
description: "Load shared libraries with dynlib, compile C sources with {.compile.}, and pass compiler/linker flags from Nim."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/dynlib.html
  - https://nim-lang.org/docs/backends.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dynlib, passC/passL and linking C code

Goal: link against external code.

- Dynamic: `proc foo(): cint {.cdecl, importc, dynlib: "libtcl(|8.5|8.4).so.(1|0)".}` style names load at run time; the `(a|b)` form lists alternatives for versioned libraries. The `dynlib` argument may be a compile-time expression, but passing a variable fails at runtime (initialisation order). `--dynlibOverride:name` overrides an import. The `dynlib` module offers `loadLib`, `symAddr` and `unloadLib`.
- Compile C sources into the build: `{.compile: "myfile.c".}` (rebuilt only when its SHA1 changes; `-f` forces), `{.compile("myfile.c", "--custom flags").}` since Nim 1.4; `{.passc: "-Wall".}` and `{.passl: "-lSDL".}` pass options; `{.link: "myfile.o".}` links an extra file.
- From the CLI: `--passC:OPTION` / `--passL:OPTION` / `--cincludes:DIR` / `--clibdir:DIR` / `--clib:LIBNAME`.
- `--app:lib` and `--app:staticlib` select a library build (with `console|gui`), `--noMain` does not generate a main procedure; the host must call `NimMain` to initialise Nim (prefix settable with `--nimMainPrefix:prefix`).

Gotchas:
- The `dynlib` import is resolved when the program runs, not at compile time.

Verify: the program runs and loads the expected library.

## Checked

2026-11-02. Confirmed against manual.md (dynlib, compile, link, passc, passl pragmas), lib/pure/dynlib.nim, backends.md (`NimMain`, `--nimMainPrefix`), basicopt.txt and advopt.txt (`--app`, `--noMain`, `--passC`, `--passL`, `--cincludes`, `--clibdir`, `--clib`). Removed: `--passL:-static`, ldd/otool, the relative-path gotcha.
Method: documentation only; no commands were run.
