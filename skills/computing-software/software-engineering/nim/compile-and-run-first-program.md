---
id: computing-software.software-engineering.nim.compile-and-run-first-program
name: compile-and-run-first-program
category: computing-software
field: software-engineering
product: nim
tags: [compile-and-run-first-program, tutorial-basics, hello-world, nim-c, nim-r, nimcache, echo, nim]
level: intro
status: docs-checked
description: "Create hello.nim, build with nim c, run in one step with nim c -r, and understand where the generated C and nimcache go."
sources:
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compile and run a first Nim program

Goal: go from source file to running binary.

1. Save `echo "Hello, World!"` as `hello.nim`.
2. `nim c hello.nim` compiles the project (`compile` or `c`, default code generator C). `nim c -r hello.nim` (long form `nim compile --run hello.nim`) compiles and then runs it. Program arguments go after the file name: `nim c -r hello.nim a b`.
3. Generated files go into the `nimcache` directory: `$XDG_CACHE_HOME/nim/$projectname(_r|_d)` or `~/.cache/nim/$projectname(_r|_d)` on POSIX, `$HOME\nimcache\$projectname(_r|_d)` on Windows. `_d` marks debug builds, `_r` release builds.
4. Layout switches: `--nimcache:PATH` (generated files), `--outdir:DIR` (where the output file is written), `-o:FILE` / `--out:FILE` (output file name).
5. `nim r hello.nim` compiles to `$nimcache/projname` and runs it with the given arguments.

Gotchas:
- The default build is a debug build with many runtime checks; use `-d:release` for release builds. For comparing speed with C use `-d:danger`.
- Switching C compilers for a project that already has a nimcache needs `-f` (force rebuild).
- Indentation is spaces only; tabs are not allowed.

Verify: the program prints the greeting.

## Checked

2026-11-08. Confirmed in tut1.md (first program, `nim compile --run`, `nim c -r`, debug versus `-d:release`/`-d:danger`, spaces-only indentation) and nimc.md, basicopt.txt, advopt.txt from nim-lang/Nim doc/ (nimcache paths and `_r`/`_d` suffixes, `--nimcache`, `--outdir`, `-o:FILE`, `nim r` description, `-f`). Read in full: tut1 first-program section and nimc compiler-usage section; manual.md and lib.html were not needed and are dropped from sources. Removed: binary path and `.exe` claims, the "quiet" description of `nim r`, module-name and missing-C-compiler gotchas, and `ls` verification (not in the docs read).
Method: documentation only; no commands were run.
