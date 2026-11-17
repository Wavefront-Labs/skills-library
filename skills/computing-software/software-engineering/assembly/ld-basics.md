---
id: computing-software.software-engineering.assembly.ld-basics
name: ld-basics
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, ld-basics, asm-linking]
level: practitioner
status: docs-checked
description: "Link assembly objects with GNU ld or the gcc driver: entry point selection, static versus dynamic, startup files, map files and library order."
sources:
  - https://sourceware.org/binutils/docs/ld/Options.html
  - https://sourceware.org/binutils/docs/ld/Entry-Point.html
  - https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Linking asm objects with ld
**Goal:** turn `.o` files into runnable programs.

```sh
# assemble first (as, nasm, ...) to produce hello.o
ld hello.o -o hello                          # entry chosen as below
ld -e main hello.o -o hello                  # custom entry
ld -static hello.o -o hello
ld -Map=hello.map hello.o -o hello           # link map
# with libc: let gcc link, provide main
gcc hello_main.s -o hello
gcc -nostartfiles -static hello.o -o hello   # you provide the entry point
gcc -nostdlib -static hello.o -o hello       # no startup files, no libraries
# explicit dynamic linking (loader path is distro specific)
ld hello.o -o hello -lc --dynamic-linker=<loader-path>
```
- Entry point: ld tries, in order, the `-e` option, an `ENTRY(symbol)` in a linker script, a target-specific symbol (for many targets named `start`), the address of the first byte of the code section (usually `.text`), and finally address 0. So a program without a matching entry symbol silently starts at the first code byte; do not rely on it.
- `-e` takes a symbol name; if no such symbol exists ld tries to parse it as a number.
- `gcc -nostartfiles` skips the standard system startup files but still uses the system libraries; `-nostdlib` skips both; `-nodefaultlibs` skips only the libraries. `gcc -static` prevents linking with shared libraries.
- ld searches an archive only once, at the place it appears on the command line, so put objects that need a library before it (`ld a.o -lm`). `-Wl,option` passes an option from gcc to ld.
- `-static` (ld) means "do not link against shared libraries"; `--dynamic-linker=file` sets the dynamic linker name for dynamically linked ELF executables, and the default is normally correct.
- `-z noexecstack` marks the object as not requiring an executable stack; `-s` omits all symbol information; `-S` omits only debugger symbols.
- `-Map=mapfile` writes a link map (`-` writes it to stdout).
- `--gc-sections` drops unused input sections, keeping the one holding the entry symbol and what it references through relocations; `--print-gc-sections` lists what was removed.

## Gotchas
- The manual spells the map option `-Map=mapfile`; a path that is a directory gets `<output>.map` written inside it.
- `-static` also implies `--unresolved-symbols=report-all`.

## Self-check
Link the same object statically and dynamically and compare `file` and `ldd` output.

## Checked
2026-11-08. Checked against the GNU ld manual (Options page: -e, -static, -s, -S, -z noexecstack, -Map, --dynamic-linker, --gc-sections, archive search order; Setting the Entry Point page) and the GCC Link Options page (-nostartfiles, -nostdlib, -nodefaultlibs, -static, -Wl). Removed: the claim that gcc adds crt1.o, crti.o and the loader path, the listed linker error messages and their causes, the "No such file" symptom of a missing loader, and the cross-linker name, none of which the pages state. The `as -o` example line was replaced by a comment (the GNU as invocation page was unreadable).

Method: documentation only; no commands were run.
