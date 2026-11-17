---
id: computing-software.software-engineering.crystal.nil-safe-operators
name: nil-safe-operators
category: computing-software
field: software-engineering
product: crystal
tags: [nil-safe-operators, nil-and-nilable, try, safe-navigation, not-nil, nil-default, or-default, nil-coalescing, crystal]
level: practitioner
status: docs-checked
description: "Handle nil in Crystal: nil?, truthiness, if-assignment narrowing, try, and why &. is block shorthand."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/nil_question.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_var.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/truthy_and_falsey_values.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/blocks_and_procs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nil-safe helpers: try, &., not_nil!, ||

Goal: pick the right nil handler.

- `x.nil?` is a pseudo-method the compiler understands; it is the same as `is_a?(Nil)` and narrows types.
- `Object#try { |v| ... }` runs the block only if the value is not `nil`; `@a.try do |a| ... end` is the workaround for instance variables.
- `&.` is not a safe-navigation operator: `&.some_method` is block shorthand (`method &.some_method` is `{ |x| x.some_method }`), so use `try` for nil-safe calls.
- Narrow by assignment in a condition: `if a = some_expression` makes `a` non-nil in the branch. Also `if a && b`.
- Only `nil`, `false` and null pointers are falsey; everything else is truthy.

Gotchas:
- Narrowing works only for local variables, not instance variables, class variables, closure-bound variables or method calls (getters). Copy to a local first: `a = @a`.

Verify: spec feeding nil and non-nil, assert no exceptions.

## Checked
Checked 2026-11-02 against the crystal-book `nil?`, `if var`, Truthy and falsey values and Blocks and Procs pages. Removed: `not_nil!` and `NilAssertionError`, `Hash#fetch`, `Hash#[]?`, the `||` default-value remarks, and the `try`-adds-Nil remark (API docs not read).

Method: documentation only; no commands were run.
