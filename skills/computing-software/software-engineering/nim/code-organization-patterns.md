---
id: computing-software.software-engineering.nim.code-organization-patterns
name: code-organization-patterns
category: computing-software
field: software-engineering
product: nim
tags: [code-organization-patterns, formatting-and-linting, project-layout, idioms, structure, src-layout, best-practices, conventions, oop-style, nim]
level: practitioner
status: docs-checked
description: "Lay out a Nimble package (src, tests, private modules) and follow the standard library style guide for naming and API shape."
sources:
  - https://nim-lang.github.io/nimble/create-packages.html
  - https://github.com/nim-lang/Nim/blob/devel/doc/nep1.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project layout and idiomatic patterns

Goal: structure projects idiomatically.

- Recommended layout for a package `foobar`: `foobar.nimble`, `LICENSE`, `README.md`, `src/foobar.nim` (imported via `import foobar`), `src/foobar/utils.nim` (imported via `import foobar/utils`), and `tests/` holding `config.nims` and test files. `nimble init` creates the structure.
- Sources in `src` need `srcDir = "src"` in the `.nimble` file; `nimble init` writes it. Put extra modules in a directory named after the package.
- Hide modules from users by placing them in a `private` directory, e.g. `src/foobar/private/hidden.nim`.
- `nimble test` compiles and runs files in `tests` whose names start with the letter `t`.
- Naming (stdlib style guide): types in PascalCase, everything else camelCase; `initFoo` initializes a value type, `newFoo` a reference type; exception types end in `Error` or `Defect`; `subjectVerb` not `verbSubject` (`fileExists`); `add` not `append`; `len` for length; `cmp` for comparison.
- Mutating versus copying: `sort` mutates and `sorted` returns a copy; mutable-view operations start with `m` (`mitems`, `mpairs`).
- Use a proc when possible; reach for macros, templates, iterators and converters only when necessary. Use `let` for variables that do not change; use the implicit `result` instead of `return` unless control flow needs it.
- Getter for a private field `foo` is named `foo`, not `getFoo`, unless it has side effects or is not O(1).
- Use `std/` prefixes for stdlib imports: `std/os`, `std/[os, sysrand, posix]`. Two-space indentation, no tabs.

Gotchas:
- The style guide is mandatory only for Nim itself and official projects; elsewhere it is a convention.
- Whole-package imports expose clashes; the guide does not cover import hygiene, so check the manual's import rules if in doubt.

Verify: a new contributor runs `nimble test` from a fresh clone.

## Checked

2026-11-08. Read in full: the Nimble User Guide page "Creating Nimble packages" (init wizard, project structure, private directory, srcDir, nimble test rule) and doc/nep1.md from nim-lang/Nim (naming, coding and misc conventions). Removed: `docs/` folder, `method`/`func`/`Option`/`{.raises.}` advice, `when isMainModule` and the "macros hurt tooling" gotcha (not stated in these sources); manual, tutorial and lib.html dropped from sources.
Method: documentation only; no commands were run.
