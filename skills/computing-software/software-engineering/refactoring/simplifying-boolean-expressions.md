---
id: computing-software.software-engineering.refactoring.simplifying-boolean-expressions
name: simplifying-boolean-expressions
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, boolean-simplification, conditional-logic, de-morgan, decompose-conditional, readability]
level: intro
status: draft
description: "Simplify boolean expressions: De Morgan, removing double negatives and boolean literals, naming sub-conditions, and positive conditionals, verified with truth tables."
sources: ["https://refactoring.com/catalog/decomposeConditional.html", "https://www.oreilly.com/library/view/code-complete-2nd/0735619670/", "https://rules.sonarsource.com/java/RSPEC-1125/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Simplifying boolean expressions

## Mechanical simplifications (always safe, check side effects)
| Before | After |
|---|---|
| `if (x == true)` / `if (flag == false)` | `if (x)` / `if (!flag)` |
| `return cond ? true : false;` | `return cond;` |
| `if (c) return true; else return false;` | `return c;` |
| `!(a && b)` | `!a \|\| !b` (De Morgan) |
| `!(a \|\| b)` | `!a && !b` |
| `!(x >= 10)` | `x < 10` (beware NaN for floats) |
| `a && a` / `a \|\| (a && b)` | `a` (idempotence / absorption) |
| `if (!notReady)` | rename to `ready`, then `if (ready)` |

## Readability refactorings
- **Name sub-expressions** (Extract Variable or Extract Function, Fowler's Decompose Conditional):
  ```java
  boolean isSummer = date.isAfter(SUMMER_START) && date.isBefore(SUMMER_END);
  boolean isLoyal = customer.years() >= 3 && !customer.hasArrears();
  if (isSummer && isLoyal) ...
  ```
- **Positive form first**: `if (isValid)` rather than `if (!isInvalid)`; put the normal case first.
- **Consolidate Conditional Expression** when several checks lead to the same result.
- **Guard clauses** to flatten nested ifs.
- Number-line ordering (McConnell): write ranges as `min <= x && x < max`.

## Verify equivalence
- For 2-4 variables write a truth table or a quick exhaustive test:
  ```python
  from itertools import product
  assert all(old(a,b,c) == new(a,b,c) for a,b,c in product([True,False], repeat=3))
  ```
- Watch short-circuit side effects: `a() && b()` -> `b() && a()` changes which functions run.
- Nullable/tri-state booleans (SQL NULL, `Boolean` objects, JS truthiness): `!(a == b)` and
  `a != b` can differ with NULL; `if (value)` treats `0` and `""` as false in JS/Python.

## Linters
Sonar `S1125` (boolean literals), ESLint `no-unneeded-ternary`, `no-extra-boolean-cast`,
Ruff `SIM` rules (`SIM103` return condition directly, `SIM108` ternary), IntelliJ "Simplify" inspection.
