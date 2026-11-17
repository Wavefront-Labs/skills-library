---
id: computing-software.software-engineering.v-lang.v-main-function-and-entry
name: v-main-function-and-entry
category: computing-software
field: software-engineering
product: v-lang
tags: [v-main-function-and-entry, hello-world-and-program-structure, fn-main, entry-point, script-mode, v-run, v-lang]
level: intro
status: docs-checked
description: "Structure a V program with fn main, run it with v run, skip main in single-file scripts, and compile a folder of files in one module with v run ."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# main function and program entry

Goal: write the smallest valid V program and know how the entry point is chosen.

- `fn main() { println('hello world') }` saved as `hello.v`, run with `v run hello.v`. Compile without running with `v hello.v`; `v help` lists commands.
- `main` is the entry point and returns nothing, so it has no return type. `println` is a built-in function that prints to standard output. V source files use UTF-8.
- `fn main()` can be skipped in single-file programs (scripts): `println('hello world')` alone is a valid program.
- Without an explicit `fn main() {}`, put all declarations before any variable assignment or top-level function call, because V treats everything after the first assignment or call as part of the implicit main function.
- A folder with several `.v` files that declare the same module (usually `module main`) compiles together with `v run .`; you do not `import` sibling files, and one of them holds `main()`.
- Arguments after the source file or folder go to your program as is (`v run . --yourparam some_other_stuff`); `os.args` gives them. V compiler flags go before `run`.
- After a successful `v run`, V deletes the generated executable; keep it with `v -keepc run .` or compile with `v .`.

Verify: `v run hello.v` prints the greeting.

## Checked

Confirmed against the "Hello World" and "Running a project folder with several files" sections of doc/docs.md in the vlang/v repository, read 2026-11-08. Removed: exit code and `exit(1)` guidance, unused variable/import compile error gotcha, naming convention claims and `eprintln` (not located in the sections read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
