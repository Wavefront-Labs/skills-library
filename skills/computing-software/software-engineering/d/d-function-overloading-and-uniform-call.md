---
id: computing-software.software-engineering.d.d-function-overloading-and-uniform-call
name: d-function-overloading-and-uniform-call
category: computing-software
field: software-engineering
product: d
tags: [d-function-overloading-and-uniform-call, functions, overloading, overload-set, overload-resolution, alias-overload, module-overloads, d]
level: advanced
status: draft
description: "Understand D overload resolution (exact, conversion, qualifier match), explicit alias overload sets across modules, and ordering gotchas with templates."
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

# Function overloading, overload sets, and UFCS on functions

Goal: predict which overload is called.

- Matching levels: exact, with qualifier conversion, with implicit conversion, no match. Ties are ambiguous: compile error.
- Non-template beats a template when equally good.
- Overloads across modules are not merged automatically: define `alias foo = a.foo; alias foo = b.foo;` or import the module whose names you want (selective import only imports that name's set from that module).
- Local declarations hide imported functions of the same name unless aliased together.
- Class members: derived-class declaration hides all base overloads of that name; restore with `alias f = Base.f;`.
- `void f(int[])` vs `void f(const(char)[])`: string literals match `const(char)[]`, not `int[]`.
- Use `__traits(getOverloads, T, "name")` to inspect.

Gotchas:
- Adding an overload in another module can silently change resolution for callers that import both.
- `short` literal arguments prefer `int` over `byte`.

Verify: unittest calls each overload and asserts via return value tags.
