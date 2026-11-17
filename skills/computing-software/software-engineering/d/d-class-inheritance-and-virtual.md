---
id: computing-software.software-engineering.d.d-class-inheritance-and-virtual
name: d-class-inheritance-and-virtual
category: computing-software
field: software-engineering
product: d
tags: [d-class-inheritance-and-virtual, classes, class, inheritance, virtual, override, final, abstract, super, object, d]
level: intro
status: docs-checked
description: "Write D classes: reference semantics, single inheritance, virtual methods, override/final/abstract, constructor chaining with super, and Object base methods."
sources:
  - https://dlang.org/spec/class.html
  - https://dlang.org/spec/function.html
  - https://dlang.org/spec/expression.html
  - https://dlang.org/phobos/object.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class inheritance, virtual methods, override and final

Goal: model hierarchies with classes.

- Class variables are references: after `Foo g = f;` both name one object.
- Member functions are virtual unless `final`, `static`, `private`, `package` or member templates; a derived class overrides with `override`, and `final` prevents overriding.
- Single inheritance plus interfaces; a class with an `abstract` member function (or declared `abstract`) cannot be instantiated; a `final class` cannot be subclassed and its methods are final.
- Constructors: `super(3);` calls the base constructor. Every path through a constructor must make exactly one delegating `this(...)` or `super(...)` call, and `this` cannot be used before it. With none written and a no-argument base constructor, `super()` is inserted at the start.
- `Object` provides `toString`, `toHash`, `opCmp` and `opEquals(Object)`; override them with matching signatures.
- `a == b` on class references is rewritten to `object.opEquals(a, b)`, which handles null; the default `Object.opEquals` only compares identity (like `is`).
- Downcast: `auto d = cast(Derived) b;` (null when wrong).

Gotchas:
- Override `opEquals` for value equality; the default only compares identity.

Verify: unittest creating Derived via Base reference and calling an overridden method.

## Checked
Checked 2026-11-03 against the D language spec Classes and Functions (virtual functions) pages, the Expressions page (equality, identity, cast) and the object module page. Confirmed: non-virtual member kinds, `final` classes, `super` and delegating constructor rules, abstract classes, `Object` methods, `==` rewrite, downcast returning null. Removed: `super.method()`, the clone remark and the devirtualisation remark (not in those pages).

Method: documentation only; no commands were run.
