---
id: computing-software.software-engineering.d.d-in-out-contracts
name: d-in-out-contracts
category: computing-software
field: software-engineering
product: d
tags: [d-in-out-contracts, contracts, in-contract, out-contract, preconditions, postconditions, design-by-contract, assert, enforce, d]
level: practitioner
status: docs-checked
description: "Specify preconditions with in {} and postconditions with out(result) {}, new expression syntax in (cond) out (r; cond), release behaviour and input validation."
sources:
  - https://dlang.org/spec/function.html
  - https://dlang.org/dmd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in and out contracts, assert vs enforce

Goal: state function obligations in code.

```d
int isqrt(int x)
in (x >= 0, "negative input")
out (r; r * r <= x && (r + 1) * (r + 1) > x)
{ ... }
```
- Older block form: `in { assert(x >= 0); } out (r) { assert(r >= 0); } do { ... }`.
- `in` checks the caller's obligation; `out` the function's promise; `out` blocks can reference parameters and the result.
- Inheritance: overriding method preconditions may only be weakened (OR'd with base), postconditions strengthened (AND'd).
- `-release` does not emit run-time checks for contracts and asserts; `assert(0)` may still generate a halt instruction. `-check=in=off`, `-check=out=off` etc. switch single checks (`-check=help` lists them).
- By default (`-checkaction=D`) a failed contract throws an unrecoverable `AssertError`; use `std.exception.enforce` for input from outside the program (errors you handle) rather than programming errors.

Gotchas:
- Side effects in contract conditions disappear in release builds.
- Don't catch `AssertError` for control flow.

Verify: unittest expects `assertThrown!AssertError(isqrt(-1))`.

## Checked

Date 2026-11-02. Confirmed in/out contract syntax and semantics (Functions spec) and -release, -check, -checkaction (DMD switches). Replaced the unconfirmed -release wording with the documented behaviour.

Method: documentation only; no commands were run.
