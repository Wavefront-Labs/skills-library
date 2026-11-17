---
id: computing-software.software-engineering.v-lang.v-match-on-sum-types
name: v-match-on-sum-types
category: computing-software
field: software-engineering
product: v-lang
tags: [v-match-on-sum-types, sum-types, match, sum type match, exhaustive, variants, else branch, pattern matching, v-lang]
level: practitioner
status: docs-checked
description: "Use match to branch on the variant of a sum type with exhaustiveness checks and automatic smartcasting inside each branch."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Matching on sum types

Goal: handle every variant safely.

```v
struct Moon {}
struct Mars {}
struct Venus {}

type World = Mars | Moon | Venus

fn land(w World) {
    match w {
        Moon {} // no atmosphere
        Mars { open_parachutes(3) }
        Venus { open_parachutes(1) }
    }
}
```
- A match on a sum type is exhaustive when every variant type is listed, so no `else` is needed. Otherwise `match` must have a pattern for each variant or an `else` branch.
- Inside a branch the match variable is smart cast to that variant (`Moon { w.moon_walk() }`), so its fields and methods are accessible.
- Recursive example from the docs: `Empty { 0 }` and `Node { tree.value + sum(tree.left) + sum(tree.right) }`.
- Named variants bind the payload: `Expr.Count(n) { 'count ${n}' }`. The binding is an immutable copy; to change a value in a `match mut` branch, assign a new variant to the matched variable. A branch can list several variants (`Expr.IntLit, Expr.Count {`) when it binds no payload.
- A `match` is an expression and returns the value of the final expression of the matching branch.

Verify: remove one branch and confirm the compiler complains about a missing variant.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Matching sum types", "Named variants", "Match"). Removed as not stated there: the `Num, Mul { }` no-smartcast remark for unnamed variants, `match mut e` for unnamed variants, the exact compile error wording.

Method: documentation only; no commands were run.
