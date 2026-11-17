---
id: computing-software.software-engineering.d.d-user-defined-property-syntax
name: d-user-defined-property-syntax
category: computing-software
field: software-engineering
product: d
tags: [d-user-defined-property-syntax, properties, property-function, getter, setter, optional-parentheses, property-attribute, d]
level: practitioner
status: draft
description: "Write getter/setter style properties in D using functions with @property, optional-parens calls, and the rules since dmd stopped enforcing @property strictly."
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

# Property functions and @property

Goal: expose fields through functions with field-like syntax.

```d
struct Temp {
    private double c_;
    @property double celsius() const { return c_; }
    @property void celsius(double v) { c_ = v; }
    @property double kelvin() const { return c_ + 273.15; }
}
Temp t; t.celsius = 20; auto k = t.kelvin;
```
- A zero-arg function can be called without parens; a one-arg function can be assigned via `obj.f = v` (assignment rewrites to `obj.f(v)`).
- `@property` marks intent and prevents `obj.f()` misuse when `-property` style checks apply (confirm per compiler version: enforcement is largely relaxed).
- Use `const`/`inout` on getters so they work on const objects.
- Combine with UFCS: free functions can serve as properties for any type.

Gotchas:
- A property returning a delegate is ambiguous: `obj.f()` calls the property then the delegate.
- `obj.prop += 1` rewrites to getter + setter; both must exist.

Verify: unittest that assigns and reads back, `assert(t.kelvin == 293.15);`.
