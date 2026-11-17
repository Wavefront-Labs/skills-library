---
id: computing-software.software-engineering.d.d-template-mixins-and-alias-parameters
name: d-template-mixins-and-alias-parameters
category: computing-software
field: software-engineering
product: d
tags: [d-template-mixins-and-alias-parameters, templates, alias-parameter, template-this, mixin-template, template-alias, policy-based-design, d]
level: advanced
status: draft
description: "Pass symbols and functions as alias parameters, use this-template parameters, and compose behaviour with mixin templates added to classes and structs."
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

# Template alias parameters, template this and template mixins

Goal: parametrise by symbols and inject members.

- `alias` parameter: `auto apply(alias f, T)(T x) { return f(x); }` accepts any symbol (function, lambda, template, variable, module), evaluated at compile time with the symbol's context. `apply!(a => a + 1)(3)`.
- `string` lambdas (legacy): `"a + b"` form in std.functional/std.algorithm still works via `unaryFun/binaryFun`.
- `this` template parameter: `string name(this T)() { return T.stringof; }` gets the most-derived static type; used for CRTP-like patterns.
- `mixin template Counted() { int n; void inc() { ++n; } }` then `class A { mixin Counted; }` injects members; a name defined in the class wins over mixin names.
- Template mixins see their own scope (not the instantiation point), unlike string mixins.
- Policy design: `struct Cache(alias evict) { ... }`.

Gotchas:
- An alias to a local variable makes the template depend on a frame pointer (needs a closure/delegate context).
- Overloaded names passed as `alias` pass the entire overload set.

Verify: compile `apply!(x => x * 2)(4) == 8` in a unittest.
