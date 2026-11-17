---
id: computing-software.software-engineering.nim.custom-exceptions-and-hierarchy
name: custom-exceptions-and-hierarchy
category: computing-software
field: software-engineering
product: nim
tags: [custom-exceptions-and-hierarchy, exceptions, custom-exception, catchableerror, defect, exception-hierarchy, newexception, nim]
level: practitioner
status: docs-checked
description: "Define exception types deriving from CatchableError, understand Defect vs CatchableError and ordering of except branches."
sources:
  - https://nim-lang.org/docs/manual.html
  - https://nim-lang.org/docs/nep1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom exceptions and the exception hierarchy

Goal: model failures with proper types.

- Every exception inherits from `Exception`. Children: `CatchableError` (recoverable: `IOError` with `EOFError`, `OSError`, `ResourceExhaustedError`, `ValueError` with `KeyError`) and `Defect` (programming bugs: `IndexDefect`, `NilAccessDefect`, `AssertionDefect`, `FieldDefect`, `RangeDefect`, `ArithmeticDefect` with `DivByZeroDefect` and `OverflowDefect`, and others).
- Define: `type AppError = object of CatchableError`, optionally with fields; create with `newException(AppError, "text")` (a template in `system`). NEP 1: exception types end in `Error` or `Defect` and should inherit `CatchableError` or `Defect`, not `Exception`.
- Defects are strictly speaking not catchable, because they may be mapped to an operation that terminates the process; with `--panics:on` they become unrecoverable errors.
- `-d:danger` turns off all runtime checks (see the release-vs-danger skill).

Verify: an `except AppError` branch catches the custom type but not a ValueError.

## Checked

2026-11-02. Confirmed against manual.md (Exception hierarchy tree, Defect wording, `--panics`), nep1.md (suffix and inheritance rule), lib/system.nim (`newException`) and nimc.md (`danger`). Removed: the `(ref AppError)(...)` construction, except-ordering, non-ref raise and thread/FFI gotchas.
Method: documentation only; no commands were run.
