---
id: computing-software.software-engineering.cpp.override-final-and-virtual-dispatch
name: override-final-and-virtual-dispatch
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, cpp-hierarchies, cpp-hi-override, override, final, virtual-functions, devirtualization, pure-virtual, override-final]
level: practitioner
status: docs-checked
description: "Write safe C++ virtual hierarchies with override and final, and avoid silent signature mismatches and name hiding."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c128-virtual-functions-should-specify-exactly-one-of-virtual-override-or-final", "https://en.cppreference.com/w/cpp/language/override"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# override, final and virtual dispatch

Each virtual function declaration should say exactly one of `virtual`, `override`, `final` (C.128).

```cpp
struct Base {
  virtual ~Base() = default;
  virtual void draw(int scale) const;
  virtual void save() = 0;
};
struct D : Base {
  void draw(int scale) const override;     // ok
  // void draw(int scale) override;        // error: not const, would silently be a NEW function without 'override'
  void save() final;                        // no further override allowed
};
```

Without `override`, a typo, a missing `const`, or a base-class signature change silently creates an unrelated function and the base version keeps being called. With it the compiler errors.

## Rules and tips
- `virtual` means "a new virtual function", `override` means "a non-final overrider", `final` means "a final overrider"; writing more than one of them is redundant and error-prone (C.128). The enforcement list flags overrides with neither `override` nor `final`.
- `override` makes the program ill-formed if the function is not virtual or does not override a base virtual function. It can also be applied to a destructor (`~B() override`).
- `override` is a special identifier only after a member function declarator; it is not a reserved keyword.
- On a class defined `final`, each virtual function should use either `override` or `final` with no semantic difference.
- Use `final` on functions sparingly: C.128 notes it does not necessarily lead to optimization and it precludes further overriding.

## Gotchas
- Name hiding: C.128's bad example has `void f3(double)` in a derived class hiding `virtual void f3(int)` of the base; marking it `override` turns the mistake into a compile error.

## Verify
- [ ] Every overrider is marked `override` or `final`, with no `virtual` repeated.
- [ ] Test calls through `Base&` hit the derived implementation (a counter or return value differs).

## Checked
2026-11-03. Confirmed on Core Guidelines C.128 (one of virtual/override/final, hiding example, final note, enforcement) and cppreference override specifier (ill-formed when not overriding, destructor use, contextual keyword). Removed: compiler warning flags and clang-tidy `modernize-use-override`, the claim that `final` enables devirtualisation (C.128 says it does not necessarily optimise), covariant returns, default arguments, non-virtual interface, private virtuals, `using Base::draw`, constructor/destructor virtual calls, the indirect-call cost figure and pure-virtual bodies.
Method: documentation only; no commands were run.
