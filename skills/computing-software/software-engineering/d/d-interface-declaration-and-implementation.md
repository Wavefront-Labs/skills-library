---
id: computing-software.software-engineering.d.d-interface-declaration-and-implementation
name: d-interface-declaration-and-implementation
category: computing-software
field: software-engineering
product: d
tags: [d-interface-declaration-and-implementation, interfaces, interface, implements, final-interface-method, static-interface-method, multiple-interfaces, d]
level: intro
status: docs-checked
description: "Declare D interfaces with abstract methods, implement several, and add final and static methods with bodies."
sources:
  - https://dlang.org/spec/interface.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interface declaration, multiple implementation and final/static members

Goal: define contracts for classes.

- `interface Shape { double area() const; string name() const; }`; a class lists it: `class Circle : Base, Shape, Drawable`.
- Virtual interface methods have no body; `final` and `static` functions with bodies are allowed, and classes may not override them. Function templates in an interface are implicitly `final`.
- Interfaces can extend other interfaces (`interface A : B, C {}`) but not classes; a class cannot list the same interface twice.
- A class converts implicitly to its interfaces, and an interface converts to its inherited interfaces; an interface cannot be instantiated with `new`.
- A class must implement every virtual interface function with a matching signature; a derived class can override it, or reimplement the interface by listing it again (`class B : A, I`).

Gotchas:
- An implementation with a different return type or signature (`int foo()` for `void foo()`) does not satisfy the interface.

Verify: unittest calls through the interface reference on two implementers.

## Checked
Checked 2026-11-03 against the D spec Interfaces page (declarations, method bodies, implementing and reimplementing interfaces). Removed: casts to `Object`, diamond resolution, "no data fields", `is(Circle : Shape)`, the `alias method` remark and the exact-const remark (not on that page).

Method: documentation only; no commands were run.
