---
id: computing-software.software-engineering.v-lang.v-if-guard-and-optional-unwrapping
name: v-if-guard-and-optional-unwrapping
category: computing-software
field: software-engineering
product: v-lang
tags: [v-if-guard-and-optional-unwrapping, control-flow-if-and-match, if guard, if unwrap, optional binding, if x, else err, option unwrapping, v-lang]
level: practitioner
status: docs-checked
description: "Unwrap options and results in the if condition with if x := f() {} else {} and use err in the else branch."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if guards with option and result

Goal: use a value only when it exists.

- "If unwrapping" works anywhere `or {}` works: it binds the unwrapped value to a variable when the expression is not `none` nor an error.
- Result: `fn res() !int { return 42 }` then `if v := res() { println(v) }`.
- Maps: `if v := m['foo'] { println(v) } else { println('not found') }` handles missing keys.
- Arrays: `if v := arr[0] { ... }` works too, and as an expression: `u_name := if v := arr[0] { v.name } else { 'Unnamed' }`.
- Use `if mut value := expression { ... }` when the unwrapped variable must be mutable, for example to pass it to a `mut` parameter. This applies to option/result, map lookup, array lookup, and channel receive guards.
- An optional struct field can be unwrapped this way even after an earlier `none` check.

Verify: unit test both branches with present and absent values.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "If unwrapping"). Fixed: the earlier text said `if v := m['k']` is not valid for map reads; the docs use exactly that form. Removed as not stated there: the `err` variable in the else branch, `else if` chaining of guards, `index_opt`, bound-variable scope and `&&` combination remarks.

Method: documentation only; no commands were run.
