---
id: computing-software.software-engineering.crystal.if-var-responds-to
name: if-var-responds-to
category: computing-software
field: software-engineering
product: crystal
tags: [if-var-responds-to, flow-typing-is-a, responds-to, truthiness-narrowing, if-var, duck-typing, flow-typing, crystal]
level: practitioner
status: docs-checked
description: "Narrow Crystal types by responds_to? and by truthiness: if x, if a = expr, and the local-variable-only limit."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_varresponds_to.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/if_var.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# responds_to? and if var truthiness

Goal: narrow by capability or by non-nil.

- `if a.responds_to?(:abs)` restricts `a` in the `then` branch to the types that respond to `abs`, and in `else` to those that do not (`Int32 | String` becomes `Int32` then `String`).
- `if a` makes `a` truthy (not `nil`) in the `then` branch; the same applies to `if a = some_expression`.
- With `&&` (`if a && b`) both are non-nil, and the right-hand side also sees `a` as non-nil.
- Reassigning inside the `then` branch gives the variable the new expression's type.

Gotchas:
- Local variables only: not instance or class variables, constants, closure-bound variables, or proc/method calls (including getters and properties), since another fiber or a second call may change the value.
- Workarounds: `if a = @a`, `a = @a` before the test, `(a = @a).responds_to?(:abs)`, or `@a.try { |a| ... }`.

Verify: use `typeof(x)` inside each branch to confirm the narrowed type.

## Checked
Checked 2026-11-02 against the crystal-book `if var.responds_to?` and `if var` pages. Removed: the by-name-only/arity remark, the `Bool | Nil` becomes `true` remark, `while (line = io.gets)`, "symbol literal only" and the flow-merge remark.

Method: documentation only; no commands were run.
