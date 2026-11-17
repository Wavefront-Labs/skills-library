---
id: computing-software.software-engineering.d.d-ufcs-method-chaining
name: d-ufcs-method-chaining
category: computing-software
field: software-engineering
product: d
tags: [d-ufcs-method-chaining, ufcs, uniform-function-call-syntax, extension-method, chaining, free-function, d]
level: intro
status: draft
description: "Use a.f(b) as f(a, b) for free functions, chain pipelines, extend built-in types, and understand name lookup, shadowing and import placement."
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

# UFCS: calling free functions as methods

Goal: write fluent code and extend any type.

- `x.f(y)` is rewritten to `f(x, y)` if `x` has no member `f`. Works for arrays, ints, strings, structs, classes.
- Extension: `int twice(int n) { return n * 2; }  5.twice;` (also with `@property`-like zero-arg calls: no parentheses needed).
- Chain: `text.splitter.map!strip.filter!(a => a.length).array`.
- Lookup: members take priority over free functions; free function must be visible at the call site (imported in that scope or declared in the same module).
- Local imports: `import std.algorithm : map;` inside the function enables UFCS for that scope.
- Works with templates: `5.to!string` means `to!string(5)`.

Gotchas:
- A member with the same name shadows the free function silently.
- UFCS does not apply to function-local functions that are declared after use, or to non-function symbols.

Verify: unittest `assert(3.twice == 6);`
