---
id: computing-software.software-engineering.crystal.conditionals-and-loops
name: conditionals-and-loops
category: computing-software
field: software-engineering
product: crystal
tags: [conditionals-and-loops, syntax-basics, if, unless, ternary, while, until, loop, break, next, truthiness, crystal]
level: intro
status: draft
description: "Use if, unless, ternary, while, until, loop, break, next and the truthiness rule where only nil, false and null pointers are falsy."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Conditionals and loops

Goal: write idiomatic control flow.

- `if/elsif/else/end` is an expression and returns the branch value; `unless` the negation; modifier forms `x if cond`.
- Falsy values: `nil`, `false`, and null pointers. `0` and `""` are truthy.
- Loops: `while cond`, `until cond`, `loop do ... end` (infinite, use `break`). `break value` can return a value from `while`.
- Iterate with `each`, `times`, `upto`, `step`, or `each_with_index` rather than C-style loops.
- `next` skips to the next iteration; in blocks `next value` returns from the block.

Gotchas:
- Variables assigned in a loop may widen to a union type.
- `break` inside a block exits the method that yielded, not just the block.
- Assignment in a condition (`if x = foo`) is allowed and enables flow typing.

Verify: a spec covering each branch; `p (if false; 1; end)` prints nil.
