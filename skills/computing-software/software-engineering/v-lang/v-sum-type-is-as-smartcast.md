---
id: computing-software.software-engineering.v-lang.v-sum-type-is-as-smartcast
name: v-sum-type-is-as-smartcast
category: computing-software
field: software-engineering
product: v-lang
tags: [v-sum-type-is-as-smartcast, sum-types, is, as, smartcast, type narrowing, cast sum type, typeof, v-lang]
level: practitioner
status: docs-checked
description: "Test the variant with is/!is, narrow in if conditions, force with as, and read the value of sum types of primitives."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# is, !is, as and smartcasting

Goal: narrow sum types without match.

- `w is Mars` checks whether a sum type instance holds a given type: `assert w is Moon`.
- `mars := w as Mars` casts to a variant and panics if `w` does not hold a `Mars`; the docs call a smart cast the safer way.
- Smart cast: inside `if w is Mars { ... }`, `w` has type `Mars` (flow-sensitive typing), so `w.dust_storm()` works.
- If `w` is a mutable identifier, declare it with `mut` before the `is` expression: `if mut w is Mars { ... }`; otherwise `w` keeps its original type. This works for simple variables and complex expressions like `user.name` and `values[i]`, and for mutable method receivers.
- Smart casts also work on indexed expressions in `match` branches: `match values[0] { string { ... } else { ... } }`.
- `typeof(w).name` and `w.type_name()` give the held variant name.
- For named variants, `is`/`!is` use the variant: `e is Expr.Void`, `e is Expr.Count`.

Verify: `assert World(Moon{}) is Moon`.

## Checked

Date: 2026-11-02. Confirmed in the V documentation (doc/docs.md, "Dynamic casts", "Smart casting", "Named variants"). Removed as not stated there: `!is` early-return narrowing, `&&` narrowing in conditions, the mutable struct field workaround, "is on non-sum type is an error", the lost-on-reassignment remark.

Method: documentation only; no commands were run.
