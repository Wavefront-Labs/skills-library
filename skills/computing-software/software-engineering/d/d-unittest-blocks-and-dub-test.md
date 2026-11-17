---
id: computing-software.software-engineering.d.d-unittest-blocks-and-dub-test
name: d-unittest-blocks-and-dub-test
category: computing-software
field: software-engineering
product: d
tags: [d-unittest-blocks-and-dub-test, unit-tests, unittest, dub-test, -unittest, -main, assertthrown, testing, ddoc-unittest, d]
level: intro
status: docs-checked
description: "Write unittest {} blocks beside code, enable them with -unittest or dub test, use assertThrown/collectException, and document examples."
sources:
  - https://dlang.org/spec/unittest.html
  - https://dlang.org/dmd-linux.html
  - https://dub.pm/cli-reference/dub-test/
  - https://dlang.org/phobos/std_exception.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unittest blocks, -unittest and dub test

Goal: test in the same file as the code.

```d
int add(int a, int b) { return a + b; }
unittest { assert(add(2, 3) == 5); }
```
- Enabled with the compiler switch `-unittest`; within a module they run in lexical order, while the order of modules and whether the program stops on the first failure are implementation defined. `-main` adds a default `main()` when compiling a library. With unittests enabled the version identifier `unittest` is predefined.
- `dub test` builds the package and runs its unit tests: it prefers an existing `unittest` configuration, else the first library configuration, else the first executable one; for library configurations dub generates the main file, and `--main-file` supplies a custom one.
- `std.exception` has `assertThrown!E(expr)`, `assertNotThrown` and `collectException`; `assert(a == b, "msg")` also works.
- A `///` ddoc comment above a unittest makes it a documented unittest, inserted into the example section of the declaration; a unittest may carry function attributes such as `@safe nothrow`.
- `-checkaction=context` is one of the documented `-checkaction` values (`D|C|halt|context`).

Gotchas:
- Whether the program stops on the first failing unittest is implementation defined.
- When unittests are not enabled, the compiler is not required to check the unittest body for correctness, though its tokens must still be valid.

Verify: `dub test` exits non-zero when an assert is flipped.

## Checked
Checked 2026-11-03 against the D spec Unit Tests page, the dmd command-line page (`-unittest`, `-main`, `-checkaction`), the dub-test reference page and the std.exception page. Removed: the `mainSourceFile` remark, `@("description")` naming, `rdmd`, the third-party runners (`unit-threaded`, `silly`) and the `version(unittest)` remark (not on those pages).

Method: documentation only; no commands were run.
