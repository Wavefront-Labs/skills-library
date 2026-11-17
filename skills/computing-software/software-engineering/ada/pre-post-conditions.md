---
id: computing-software.software-engineering.ada.pre-post-conditions
name: pre-post-conditions
category: computing-software
field: software-engineering
product: ada
tags: [ada, pre-post-conditions, ada-contracts]
level: practitioner
status: docs-checked
description: "Ada 2012 Pre and Post aspects, 'Old and 'Result attributes, quantified expressions and enabling checks with -gnata."
sources:
  - https://www.ada-auth.org/standards/
  - https://learn.adacore.com/courses/intro-to-ada/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pre and Post conditions
```ada
function Pop (S : in out Stack) return Integer
  with Pre  => not Empty (S),
       Post => Size (S) = Size (S)'Old - 1;
function Sqrt2 (X : Float) return Float with Post => Sqrt2'Result >= 0.0;
```
- GNAT turns pre- and postconditions into run-time assertions, but assertions are off by default: compile with `-gnata`.
- `for all` and `for some` quantified expressions state conditions over arrays and containers, e.g. `(for all I in A'Range => A (I) = 0)`.
- `A'Old (I)` refers to the value before the call.
## Gotchas
- Without `-gnata`, contracts are not checked.
## Self-check
Compile with and without -gnata and confirm a failing Pre is detected only in the first.

## Checked
2026-11-03. Confirmed in Introduction to Ada, Contract-Based Programming: `Pre`, `Post`, `'Old`, `'Result`, `-gnata` default-off, quantified expressions. Removed `Pre'Class`/`Post'Class`, `Contract_Cases`, `Assertion_Policy` and the named exception `Assertion_Error` (not on the pages read).
Method: documentation only; no commands were run.
