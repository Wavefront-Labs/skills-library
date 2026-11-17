---
id: computing-software.software-engineering.d.d-function-and-aggregate-templates
name: d-function-and-aggregate-templates
category: computing-software
field: software-engineering
product: d
tags: [d-function-and-aggregate-templates, templates, template, function-template, struct-template, ifti, eponymous-template, template-parameters, generics, d]
level: practitioner
status: draft
description: "Write generic D code with function templates, templated structs/classes, implicit function template argument deduction (IFTI), default type arguments and eponymous templates."
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

# Function, struct and class templates

Goal: write generic functions and types.

```d
T max(T)(T a, T b) { return a > b ? a : b; }
struct Stack(T) { T[] data; void push(T x) { data ~= x; } }
auto s = Stack!int();       // explicit instantiation
auto m = max(2, 3);         // IFTI deduces T=int
```
- Parameter kinds: type (`T`), value (`size_t N`), alias (`alias f`), `this` (`this T`), tuple (`Ts...`).
- Defaults: `Stack(T = int)`; `!` instantiates, `!(...)` multiple args, single token args drop parentheses (`to!int`).
- Eponymous: a template that contains a member with its own name collapses: `enum isInt(T) = is(T == int);` and `template Foo(T) { alias Foo = ...; }`.
- Each instantiation is a distinct type; unrelated instances do not convert.
- Templates are always compiled with the attributes of the instance; use `static assert` to explain misuse.

Gotchas:
- IFTI fails for mixed argument types (`max(1, 2.0)`): give `max!double`.
- A template function cannot be virtual (use a template wrapper calling virtual).

Verify: unittest instantiates with two types; `pragma(msg, typeof(s))` shows the instance.
