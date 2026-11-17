---
id: computing-software.software-engineering.crystal.hello-world-compile-run
name: hello-world-compile-run
category: computing-software
field: software-engineering
product: crystal
tags: [hello-world-compile-run, getting-started, hello-world, crystal-run, crystal-build, first-program, crystal]
level: intro
status: draft
description: "Write a first program and compare crystal run (compile and execute) with crystal build (produce a binary)."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hello world: run versus build

Goal: understand the compile-then-run model.

```crystal
# hello.cr
puts "Hello, #{ARGV[0]? || "world"}!"
```
- `crystal hello.cr -- Ada` or `crystal run hello.cr -- Ada` compiles to a temp binary and runs it; args after `--` go to the program.
- `crystal build hello.cr` writes a `./hello` binary (debug build, fast compile).
- `crystal build --release hello.cr` enables LLVM -O3 and is much slower to compile.

Gotchas:
- Crystal is compiled; there is no REPL in the stable toolchain, use `crystal eval`.
- Without `--` the compiler may treat program args as its own options.
- Debug builds are noticeably slower at runtime than release builds; benchmark only with `--release`.

Verify: the binary prints the greeting and `echo $?` gives 0.
