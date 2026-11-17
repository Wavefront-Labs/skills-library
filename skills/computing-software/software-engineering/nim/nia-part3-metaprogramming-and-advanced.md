---
id: computing-software.software-engineering.nim.nia-part3-metaprogramming-and-advanced
name: nia-part3-metaprogramming-and-advanced
category: computing-software
field: software-engineering
product: nim
tags: [nia-part3-metaprogramming-and-advanced, nim-in-action-projects, nim-in-action, metaprogramming, dsl, macros, templates, advanced, exercises, learning-path, nim]
level: advanced
status: draft
description: "Map the book's advanced chapters (templates, macros, DSLs, memory, concurrency) to hands-on exercises on the current compiler."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/tut1.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nim in Action part 3: metaprogramming and advanced topics

Goal: apply advanced chapters with modern Nim.

- Core: generics, templates, macros (AST manipulation, `dumpTree`), writing a DSL for configuration parsing, and a macro that generates object-to-JSON code.
- Exercises: (1) template `retry(n): body`, (2) macro `defineEnumWithStrings`, (3) DSL for CLI definition generating a parseopt loop, (4) custom `=destroy` for a file wrapper, (5) async TCP client with timeouts.
- Use `expandMacros`/`--expandMacro` to check output, and `static:` asserts to test at compile time.
- Replace old GC topics with ARC/ORC ownership practice; replace `locks` with `Atomic` where simpler.
- Reference cross-links: macros, templates, destructors, threads topics in this library.

Gotchas:
- Macro APIs gained helpers since the book; prefer `quote do` plus `newLit`.
- Do not build giant DSLs for what a proc can do.

Verify: each exercise has a passing compile-time or unit test.
