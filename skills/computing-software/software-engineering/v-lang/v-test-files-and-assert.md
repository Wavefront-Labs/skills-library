---
id: computing-software.software-engineering.v-lang.v-test-files-and-assert
name: v-test-files-and-assert
category: computing-software
field: software-engineering
product: v-lang
tags: [v-test-files-and-assert, testing, test-files, assert, test-function, unit-test, testsuite, v-lang]
level: intro
status: docs-checked
description: "Write V tests in _test.v files with test_ functions and assert, extra messages, assert_continues, internal vs external tests, testsuite hooks and v test."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test files, test functions and assert

Goal: write unit tests with the built-in runner.

- Test functions live in a file whose name ends in `_test.v`, and their names must begin with `test_`. Normal functions and types may also be defined there; call them manually.
- Internal tests declare the module (for example `module main` in `hello_test.v`) and can call private functions. External tests `import` the module and see only its public API.
- `assert expr` checks an expression; on failure it is reported to stderr and the values on each side of a comparison are printed when possible, and the program usually aborts. Asserts work in any function, not just tests, and are for programming errors.
- Extra message: `assert i * 2 - 45 < 75 + 10, 'assertion failed for i: ${i}'`. Any string expression works.
- All `assert` statements are removed when compiling with `-prod`.
- `@[assert_continues]` on a function makes failures print and continue; `-assert continues` does that globally.
- Special functions: `testsuite_begin` runs before all other test functions, `testsuite_end` after.
- A test function with an error return type (`fn test_atoi() !`) fails if an error propagates.
- Every `_test.v` file is compiled as a separate program.
- Run one file with `v foo_test.v`; a module with `v test mymodule`; everything in the folder and subfolders with `v test .`; add `-stats` for details. Folders named `testdata` next to tests are ignored by the scanner.

Verify: `v test .` runs all test functions and reports failures.

## Checked

Confirmed against the "Testing" section of doc/docs.md (Asserts, Test files, Running tests) in the vlang/v repository, read 2026-11-08. Removed: PASS-output claim, per-assert "continues with next test" claim, `fn init()` remark, `assert ... or {}` idioms (not in the docs read), and the docs.vlang.io and modules.vlang.io sources.
Method: docs-only read of cited pages, 2026-11-08
