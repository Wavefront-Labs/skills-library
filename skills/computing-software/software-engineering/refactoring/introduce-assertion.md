---
id: computing-software.software-engineering.refactoring.introduce-assertion
name: introduce-assertion
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, conditional-logic, introduce-assertion, invariants, preconditions, design-by-contract, fail-fast]
level: practitioner
status: verified
description: "Make hidden assumptions explicit with assertions (Fowler's Introduce Assertion), know when to use asserts vs validation errors, and how each language treats them."
sources: ["https://refactoring.com/catalog/introduceAssertion.html", "Refactoring, 2nd ed. (Fowler), ch10 Introduce Assertion", "https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement", "https://docs.oracle.com/javase/8/docs/technotes/guides/language/assert.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Introduce Assertion

**Goal:** turn an assumption that code silently relies on ("discount rate is never
negative here") into an executable statement that fails loudly when violated.

## Mechanics
When you see code that only works if some condition holds, add an assertion stating it:
```js
const assert = require("node:assert");   // Node: assert(cond, message) throws AssertionError; browsers have no built-in assert()
applyDiscount(aNumber) {
  if (!this.discountRate) return aNumber;
  assert(this.discountRate >= 0, "discountRate must be non-negative");
  return aNumber - this.discountRate * aNumber;
}
```
Fowler's rule: the program must behave identically with the assertion removed; it
documents and checks, it doesn't control flow. Better still, move the check to where the
value is SET (setter/constructor) so the bad state is caught at its origin.

## Assertion vs validation
| Condition comes from | Use |
|---|---|
| Your own code's logic (invariant, "can't happen") | assertion |
| External input (users, files, network, callers of a public API) | validation that raises a proper error, always on |
Never validate user input with `assert`: in several languages assertions can be
disabled in production.

## Language behaviour
- **Python**: `assert` is stripped with `python -O` (run on 3.14: `f(-1)` raised `AssertionError: x=-1` normally and returned -1 under `-O`); use `if not x: raise ValueError` for checks that must run.
- **Java**: `assert` disabled by default; enable with `-ea` (tests should run with it).
  Guava `Preconditions.checkState/checkArgument` and `Objects.requireNonNull` are always on.
- **C/C++**: `assert` removed with `NDEBUG` (release builds). `static_assert` for compile time.
- **C#**: `Debug.Assert` only in Debug builds; `ArgumentOutOfRangeException.ThrowIfNegative` (always on; documented in Microsoft Learn, .NET 8+).
- **Go**: no assert; use explicit checks and `panic` for invariant violations.
- **Rust**: `assert!` always on; `debug_assert!` only in debug builds (run on rustc 1.99.1: both panicked in a plain build; with `-O` the `debug_assert!` was skipped and the `assert!` still panicked).

## Guidelines
- Assert invariants that are cheap to check; expensive checks belong in debug-only
  asserts or tests.
- Include the offending value in the message.
- Don't over-assert every obvious fact; assert assumptions a future reader would not
  know.

## Verify
- [ ] Tests run with assertions enabled (Java `-ea`, no `-O`, debug builds).
- [ ] No `assert` used for input validation (grep at API boundaries).
