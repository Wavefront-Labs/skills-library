---
id: computing-software.software-engineering.nim.nim-c-cpp-js-commands
name: nim-c-cpp-js-commands
category: computing-software
field: software-engineering
product: nim
tags: [nim-c-cpp-js-commands, compiler-commands-and-backends, nim-c, nim-cpp, nim-js, nim-check, nim-r, subcommand, outdir, output, nim]
level: intro
status: docs-checked
description: "Pick the right nim subcommand (c, cpp, js, objc, check, r, doc, dump) and the output location flags."
sources:
  - https://nim-lang.org/docs/nimc.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nim c, cpp, js, check and r commands

Goal: drive the compiler.

- `nim c file.nim` compile via C; `nim cpp` via C++; `nim js` JavaScript; `nim objc` Objective-C; `nim check` type-check only (fast, no codegen); `nim r` compile and run; `nim doc` generate docs; `nim dump` dumps all defined conditionals and search paths.
- Output: `-o:path` output file, `--outdir:DIR` where the output is written, `--nimcache:PATH` for generated files; `-r`/`--run` runs the program (arguments follow the file); `-f`/`--forceBuild:on|off` rebuilds all modules.
- Diagnostics: `--hints:on|off|list`, `--warnings:on|off|list`, `--warningAsError:X:on|off`, `--verbosity:0|1|2|3` (1 is default), `--listCmd` lists the compilation commands.
- `--project` is a documentation option (`document the whole project`, used with `nim doc`), not a compile mode; `--noNimblePath` deactivates the Nimble path.
- Help: `nim --version` (`-v`) shows version information; `nim --fullhelp` shows all switches.

Verify: `nim check` on a bad file reports errors without a C compile.

## Checked

2026-11-02. Confirmed against basicopt.txt and advopt.txt (commands `c`, `r`, `doc`, `objc`, `dump`, `check`; `--outdir`, `--nimcache`, `--run`, `--forceBuild`, `--hints`, `--warnings`, `--warningAsError`, `--verbosity`, `--listCmd`, `--noNimblePath`, `--version`, `--fullhelp`). Fixed: `nim c --project` is a `nim doc` option, not a whole-program compile. Removed: `--listFullPaths`, `--output`/`-o` details beyond the option name, flag-syntax and main-module gotchas.
Method: documentation only; no commands were run.
