---
id: computing-software.software-engineering.d.d-template-constraints-and-concepts
name: d-template-constraints-and-concepts
category: computing-software
field: software-engineering
product: d
tags: [d-template-constraints-and-concepts, templates, template-constraint, if-constraint, sfinae, isinputrange, isnumeric, concepts, static-assert, d]
level: advanced
status: draft
description: "Restrict templates with if (...) constraints, std.traits predicates (isInputRange, isNumeric), static if/else overload resolution, and clear error messages with static assert."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Template constraints and compile-time concepts

Goal: reject wrong types early and dispatch by capability.

```d
auto sum(R)(R r) if (isInputRange!R && isNumeric!(ElementType!R)) {
    ElementType!R s = 0; foreach (x; r) s += x; return s;
}
```
- Constraint runs at overload selection; if false the template is not a candidate (compile error "none of the overloads match" lists them).
- Multiple overloads with disjoint constraints form capability-based dispatch (e.g. random-access vs input range).
- Predicates: `std.traits` (`isIntegral`, `isFloatingPoint`, `isSomeString`, `isCallable`, `hasMember`), `std.range.primitives` (`isInputRange`, `isForwardRange`, `hasLength`, `isRandomAccessRange`).
- Make your own: `enum isFoo(T) = is(typeof(T.init.foo()) == int);`
- Inside the body, `static if` / `static assert(cond, msg)` give readable messages.
- Compile-time test: `static assert(!__traits(compiles, sum(5)))`.

Gotchas:
- Constraints that themselves error (instead of being false) abort resolution; wrap in `is(typeof(...))`.
- Constraint order of evaluation is left to right with short-circuit.

Verify: call with a wrong type and read the reported failing constraint.
