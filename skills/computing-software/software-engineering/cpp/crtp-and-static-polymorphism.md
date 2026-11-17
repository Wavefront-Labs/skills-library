---
id: computing-software.software-engineering.cpp.crtp-and-static-polymorphism
name: crtp-and-static-polymorphism
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-hierarchies, cpp-hi-crtp, crtp, static-polymorphism, mixins, deducing-this, templates, crtp-static-polymorphism]
level: advanced
status: docs-checked
description: "Use the curiously recurring template pattern for compile-time polymorphism and mixins, with a protected base constructor, static_cast, and C++23 deducing this as the alternative."
sources: ["https://en.cppreference.com/w/cpp/language/crtp", "https://en.cppreference.com/w/cpp/language/member_functions#Explicit_object_parameter"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CRTP and static polymorphism

CRTP: a class derives from a template instantiated with itself, so the base can call derived members without virtual dispatch. cppreference describes it as a way to implement "compile-time polymorphism": the base exposes an interface and derived classes implement it.

```cpp
template <class Derived>
struct Base {
  void name() { static_cast<Derived*>(this)->impl(); }
protected:
  Base() = default;      // prohibits creating Base objects, which would be UB
};
struct D1 : Base<D1> { void impl() { std::puts("D1::impl()"); } };
struct D2 : Base<D2> { void impl() { std::puts("D2::impl()"); } };
```

## When to use
- Reusable behaviour mixins. The standard library itself uses the pattern: `std::enable_shared_from_this` and `std::ranges::view_interface` (cppreference lists both as CRTP helpers).
- Each `Base<T>` is a different type, so one container or one function parameter cannot hold both a `Base<D1>` and a `Base<D2>`; use virtual functions, `std::variant`, or type erasure for that.

## C++23 alternative: deducing this
```cpp
struct Base { void name(this auto&& self) { self.impl(); } };   // self is the most derived type, no template parameter
struct D1 : Base { void impl() { std::puts("D1::impl()"); } };
```
cppreference's own example switches between the two forms with the `__cpp_explicit_this_parameter` feature-test macro; use it to support compilers without the feature.

## Gotchas
- A wrong template argument (`struct A : Base<B>`) still compiles and the `static_cast` is then undefined behaviour; a protected base constructor limits who can create the base.
- One base instantiation exists per derived type.

## Verify
- [ ] Both `D1` and `D2` call their own `impl()`.

## Checked
2026-11-03. Confirmed on cppreference CRTP (static_cast to `Derived*`, protected constructor comment, the `this auto&& self` form, `__cpp_explicit_this_parameter` switch, `enable_shared_from_this` and `view_interface` as related) and the explicit object parameter page. Removed: the Comparable mixin and Shape examples, claims about inlining and vtables, compiler version numbers for deducing this, the incomplete-type note, the `static_assert(is_base_of)` guard, the protected-destructor advice, the code-bloat claim and the disassembly check.
Method: documentation only; no commands were run.
