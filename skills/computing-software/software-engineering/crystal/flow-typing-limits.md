---
id: computing-software.software-engineering.crystal.flow-typing-limits
name: flow-typing-limits
category: computing-software
field: software-engineering
product: crystal
tags: [flow-typing-limits, flow-typing-is-a, closure-narrowing, ivar-narrowing, capture, reassignment, not-nil, crystal]
level: advanced
status: draft
description: "Know where narrowing fails: instance variables, procs and blocks that capture variables, and calls that may mutate state."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flow typing limits: closures, ivars and method calls

Goal: fix narrowing that silently does not apply.

- Instance variables, class variables and getters are not narrowed because another call could change them. Fix: `if v = @v`, or `@v.try`, or `v = @v.not_nil!`.
- A local that is captured by a closure and assigned inside it loses narrowing everywhere it is used after the closure is created.
- `Hash#[]?` twice does not narrow the second call; store the result.
- Using `.as(Type)` is the escape hatch when you know more than the compiler.

Gotchas:
- Error text says the type is `(String | Nil)` even after a nil check on an ivar; that is this limit.
- `property!` and `getter!` are a way to declare a non-nil view.
- Excessive `not_nil!` hides bugs; prefer local copies.

Verify: reproduce the error, apply a local copy, rebuild.
