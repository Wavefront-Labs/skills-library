---
id: computing-software.software-engineering.assembly.symbol-naming-mangling
name: symbol-naming-mangling
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, symbol-naming-mangling, asm-interop]
level: practitioner
status: docs-checked
description: "Symbol naming from assembly: NASM global/local prefix and postfix options, %pragma equivalents, and demangling with nm -C and c++filt."
sources:
  - https://www.nasm.us/doc/nasm02.html
  - https://sourceware.org/binutils/docs/binutils/nm.html
  - https://sourceware.org/binutils/docs/binutils/c_002b_002bfilt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Symbol naming and mangling
**Goal:** make assembly symbols match what C and C++ expect.

- C++ and Java encode function overloads into a low-level assembler name (mangling). The name an assembler sees for a C++ function is therefore not the source name; assembly intended to be called from C++ must use the mangled name or be declared with C linkage on the C++ side.
```cpp
extern "C" long add2(long, long);
```
- Inspect: `nm -C file.o` (`--demangle`) shows user-level names; demangling is off by default (`--no-demangle`). `c++filt _Z1fv` decodes a symbol given on the command line; with no arguments it reads names from standard input, so a whole assembler listing can be piped through it.
- Some calling conventions expect a prefix such as an underscore on C symbols (NASM's own example is the Mach-O format). NASM can add one globally: `nasm -f macho --gprefix _ add2.asm` prepends the argument to all `extern`, `common`, `static` and `global` symbols, and is equivalent to `%pragma macho gprefix _` at the top of the file.
- Related options: `--lprefix` prepends to all other symbols, and `--gpostfix` and `--lpostfix` append. `--prefix` is an alias for `--gprefix`. Since NASM 3.01 the directive forms exist and directives, pragmas and options all accept every spelling.

## Gotchas
- A mismatch between the symbol in the object file and the name the C or C++ side expects shows up as an undefined-reference link error; compare with `nm`.
- `--prefix` is not a prefix for every symbol: it is the same as `--gprefix` (globals and externs only).

## Self-check
Compile a C++ function without `extern "C"` and read its mangled name with `nm`, then decode it with `c++filt`.

## Checked
Method: docs-checked 2026-11-09 against NASM manual chapter 2 (section 2.1.28, prefix and postfix options), the binutils nm page and the c++filt page. Dropped per-platform naming rules (ELF, Windows decoration, Itanium examples), the C preprocessor `.S` advice and the SYM macro example as not confirmed by these pages.
