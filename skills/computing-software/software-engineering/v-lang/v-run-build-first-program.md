---
id: computing-software.software-engineering.v-lang.v-run-build-first-program
name: v-run-build-first-program
category: computing-software
field: software-engineering
product: v-lang
tags: [v-run-build-first-program, hello-world-and-program-structure, v run, v build, compile, binary, v hello.v, v-lang]
level: intro
status: draft
description: "Use v run for quick execution and v hello.v or v . to produce a binary, including how V emits C and calls a C compiler."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running and building a first program

Goal: go from source to a running executable.

- `v run hello.v` compiles to a temp binary and runs it; extra args after the file go to the program (`v run app.v --port 80`).
- `v hello.v` compiles to `./hello` (hello.exe on Windows). `v .` builds the module in the current directory; `v -o out file.v` names the output.
- Under the hood V translates to C and invokes a C compiler (tcc is bundled for fast dev builds; gcc/clang for `-prod`). Confirm which compiler your install defaults to with `v -showcc file.v`.
- `v watch run file.v` reruns on save.

Gotchas:
- `v run` of a directory needs `v run .`.
- Debug builds are fast but unoptimised; benchmark only with `-prod`.

Verify: `v hello.v && ./hello` prints the output; `v -showcc` shows the C compiler command.
