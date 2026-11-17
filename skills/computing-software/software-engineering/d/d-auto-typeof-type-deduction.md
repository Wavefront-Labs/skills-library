---
id: computing-software.software-engineering.d.d-auto-typeof-type-deduction
name: d-auto-typeof-type-deduction
category: computing-software
field: software-engineering
product: d
tags: [d-auto-typeof-type-deduction, types-and-conversions, auto, typeof, type-inference, returntype, unqual, decltype, d]
level: practitioner
status: draft
description: "Use auto, typeof, typeof(return), alias and std.traits ReturnType/Unqual to deduce and name types; inferred return types and storage class inference."
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

# auto, typeof, ReturnType and type deduction

Goal: let the compiler infer types without losing clarity.

- `auto x = expr;` deduces the type; `const x = 1;` and `immutable x = 1;` also infer.
- `typeof(expr)` names the type without evaluating it (`typeof(a+b) c;`); `typeof(return)` inside a function is the return type.
- Functions can have inferred return: `auto f(int a) { return a * 2.0; }` (multiple returns must agree or share a common type).
- `std.traits`: `ReturnType!f`, `Parameters!f`, `Unqual!T`, `ElementType!R`, `CommonType!(A,B)`.
- `alias Pair = Tuple!(int,string);` names types; `alias` also renames symbols and template instances.
- `auto ref` return forwards ref-ness for templates.

Gotchas:
- `auto` strips top-level `const`/`immutable` only for value types; arrays and pointers keep their element qualifiers.
- Mutually recursive functions with inferred return types fail; annotate one.

Verify: `static assert(is(typeof(1.0f + 1) == float));`
