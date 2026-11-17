---
id: computing-software.software-engineering.d.d-switch-final-goto-statements
name: d-switch-final-goto-statements
category: computing-software
field: software-engineering
product: d
tags: [d-switch-final-goto-statements, statements, switch, final-switch, goto-case, case-range, fallthrough, d]
level: practitioner
status: docs-checked
description: "Use D switch with strings and ranges (case 1: .. case 5:), final switch exhaustiveness for enums, goto case, default and scoped fallthrough rules."
sources:
  - https://dlang.org/spec/statement.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# switch, final switch, goto case and mixin statements

Goal: write exhaustive, safe dispatch.

- Works on integers, enums, chars and strings (arrays of `char`, `wchar`, `dchar`); `case 1, 2, 3:` and `case 'a': .. case 'z':` ranges.
- Fallthrough from a non-empty case is an error unless you add `goto case;` (next) or `goto case X;` / `goto default;`. Empty adjacent cases are fine.
- `final switch (e)` on an enum requires every member and no `default`; adding an enumerator then breaks the build, which is useful.
- A non-empty case (unless the last) must end with `continue`, `break`, `return`, `goto`, `assert(0)` or a `noreturn` expression; a normal `switch` must have exactly one `default:`.

Gotchas:
- `final switch` allows no `default:` and no `case a: .. case b:` ranges.
- Case expressions must be compile-time values or runtime-initialized `const`/`immutable` integral variables, and compile-time values must be distinct; `goto case X;` needs a compile-time `X`.

Verify: add a new enum member and confirm the final switch fails to compile.

## Checked

Date 2026-11-02. Confirmed switch, final switch, goto case/default and case rules (Statements spec). Errors fixed: missing default is not described as a SwitchError rule; final switch restrictions corrected; case values may also be runtime-initialized const/immutable. Removed the static foreach plus mixin claim.

Method: documentation only; no commands were run.
