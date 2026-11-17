---
id: computing-software.software-engineering.cobol.cobc-compile-flags
name: cobc-compile-flags
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, cobc-compile-flags, cobol-compiler-gnucobol, cobc-x, cobc-free, cobc-std, cobc-debug, executable-vs-module]
level: practitioner
status: docs-checked
description: "Build programs and modules with cobc using the key flags for format, dialect, debugging and optimization."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cobc command line (-x, -m, -free, -std, --debug, -O)
**Goal:** reliable local builds.
```bash
cobc -x -o hello hello.cob              # executable
cobc -m sub.cob                         # dynamically loadable module (default)
cobc -x -free -std=cobol2014 prog.cob   # free format, 2014 dialect
cobc -x --debug -g -Wall prog.cob       # runtime checks, debug info, warnings
cobc -x -O2 -o prog main.cob util.cob   # multiple sources, optimize
cobc -x -j prog.cob                     # compile and run
```
- `-x` builds an executable (main entry point is the first program in the file); `-m` builds a dynamically loadable module and is the default; `-o file` names the output; `-j [args]` runs the program after the build.
- `-std=` dialects: default, cobol85, cobol2002, cobol2014, xopen, ibm, ibm-strict, mvs, mvs-strict, mf, mf-strict, bs2000, bs2000-strict, acu, acu-strict, rm, rm-strict, realia, realia-strict, gcos, gcos-strict (configuration files in the `config` directory).
- `-I dir` copybook search path, `-L dir`/`-l lib` link libraries, `-ext ext` adds a file extension for COPY, `-C` translates to C only, `-E` preprocesses only, `-c` compiles without linking.
- `-free` (or `-F`, `-fformat=free`) and `-fixed` force source format; without them the compiler autodetects from the first line.
- `-O`, `-O2`, `-O3`, `-Os` optimize, `-O0` disables optimization.
- `--list-reserved`, `--list-intrinsics`, `--list-system`, `--list-mnemonics`, `--list-exceptions` print the built-in lists; `-i` (`--info`) shows build and environment information.

## Gotchas
- A module (`-m`) is found by CALL through `COB_LIBRARY_PATH` or the current directory; the file name must match the called name.
- Use the C compiler GnuCOBOL was built for (`COB_CC` overrides it at your own risk).

## Self-check
`cobc -V` prints the version, and `cobc -x hello.cob` then running `./hello` works.

## Checked
2026-11-02. Checked against the GnuCOBOL manual (cobc options, source format, multiple sources, optimize) and the Programmer's Guide cobc option list. Corrected: `-m` is the default build mode, `-debug` is `--debug`/`-d`, `--fixed`/`-fixed` and `-free` are the format switches, and the option list also names realia, xopen and gcos. Removed: the Windows MinGW/MSVC remark and the "-O2 optimize" speed claims.

Method: documentation only; no commands were run.
