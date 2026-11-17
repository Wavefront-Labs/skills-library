---
id: computing-software.software-engineering.crystal.case-type-dispatch
name: case-type-dispatch
category: computing-software
field: software-engineering
product: crystal
tags: [case-type-dispatch, case-when, type-dispatch, case-type, visitor, polymorphism, narrowing-case, crystal]
level: practitioner
status: docs-checked
description: "Replace is_a? chains with Crystal case/when on types, with variable narrowing."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/case.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Type dispatch with case

Goal: replace is_a? chains.

```crystal
case var
when String then var.size  # var : String
when Int32  then var + 1   # var : Int32
else                       # neither String nor Int32
end
```
- `when Type` uses `is_a?`; if the case expression is a variable or variable assignment, the variable's type is restricted inside each branch.
- `when` conditions use `===`: `Class` matches instances, `Regex` matches the string, `Range` matches inclusion.
- Implicit-object calls work: `when .even?`.
- Tuple subjects with tuple `when` conditions test per element; `_` skips that element.
- `case/when` is rewritten to an if/elsif chain; use `in` for an exhaustive form (see case-in-pattern-matching).

Verify: compile with each type; remove one `when` and switch to `in` to see exhaustiveness.

## Checked
Checked 2026-11-02 against the crystal-book `case` page. Removed: polymorphism advice, generic `Array(Int32)` matching claims, overlap-order and module-matching remarks.

Method: documentation only; no commands were run.
