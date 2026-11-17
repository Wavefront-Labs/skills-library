---
id: computing-software.software-engineering.d.d-nested-inner-anonymous-classes-invariants
name: d-nested-inner-anonymous-classes-invariants
category: computing-software
field: software-engineering
product: d
tags: [d-nested-inner-anonymous-classes-invariants, classes, inner-class, nested-class, anonymous-class, invariant, outer, static-nested, d]
level: advanced
status: draft
description: "Use inner classes with outer-this access, static nested classes, anonymous classes via new class, and invariant() blocks checking class state."
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

# Nested, inner, anonymous classes and class invariants

Goal: use nested class forms correctly.

- Inner class (non-static) captures the enclosing object: `class Outer { int v; class In { int get() { return v; } } }`; create with `outerObj.new In()`; `this.outer` refers to the outer.
- `static class` nested: no outer pointer, just namespacing.
- Classes defined inside functions capture the function frame (closure context) and may keep stack variables alive via heap closure.
- Anonymous: `auto o = new class Base { override void f() { ... } };` or `new class(args) Iface {...}`.
- `invariant() { assert(x >= 0); }` runs on entry/exit of public methods when contracts are enabled (not in `-release`); also valid on structs.
- Interact with `in`/`out` contracts on methods; derived classes inherit base invariants.

Gotchas:
- Inner class instances of different outer objects are distinct types of the same class.
- Invariants run only for public/export members called from outside, and not during construction until the ctor finishes.

Verify: unittest triggers an `AssertError` by violating an invariant (skip with `-release`).
