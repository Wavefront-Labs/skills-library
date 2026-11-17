---
id: computing-software.software-engineering.nim.nbe-hello-and-basics-patterns
name: nbe-hello-and-basics-patterns
category: computing-software
field: software-engineering
product: nim
tags: [nbe-hello-and-basics-patterns, learning-resources-nim-by-example, nim-by-example, hello-world, values, variables, closures, recursion, examples, basics, nim]
level: intro
status: draft
description: "Cover the introductory example set: hello world, values, variables, if/else, case, for, while, procs, closures and recursion."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim by Example basics: hello, values, variables, loops

Goal: practise the foundational examples.

- Work through: Hello World, Values (int, float, bool, string ops), Variables (var/let/const), If/Else, Case, For, While, Procs, Closures, Recursion, Defer, Importing modules.
- Pattern: write a tiny program per concept, compile with `nim c -r`, and vary it.
- Closures: a proc returning a proc capturing a local `var`: `proc counter(): proc(): int = var n = 0; return proc(): int = inc n; n` (needs the `{.closure.}` default for anonymous procs).
- Recursion: factorial/fibonacci with `int` and memoisation using `Table`.
- Output tools: `echo`, `repr`, `fmt`.
- Extend each by adding a unit test with `unittest`.

Gotchas:
- Closures capturing loop variables share them unless copied (`capture` from sugar).
- Deep recursion can overflow the stack: default stack depends on OS (8 MB Linux typical).

Verify: each example prints the expected output.
