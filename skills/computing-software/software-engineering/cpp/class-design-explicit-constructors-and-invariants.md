---
id: computing-software.software-engineering.cpp.class-design-explicit-constructors-and-invariants
name: class-design-explicit-constructors-and-invariants
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, cpp-class-design, explicit-constructors, class-invariants, special-member-functions, value-semantics, cpp-core-guidelines]
level: practitioner
status: docs-checked
description: "Design C++ classes well: establish invariants in constructors, explicit single-arg constructors, member init order, defaulted/deleted special members, and value semantics."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-class", "https://github.com/cplusplus/draft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Class design: explicit constructors, invariants and special members

**Goal:** classes that cannot be constructed in an invalid state, do not convert implicitly by
accident, and get copy/move/compare right with the least code.

## struct vs class
Use `struct` for plain aggregates with no invariant (all members public, any combination valid).
Use `class` with private data when there is an **invariant** (a relationship members must keep,
e.g. `lo <= hi`, a sorted vector, a non-null handle). (Core Guidelines C.2)

## Constructors establish the invariant
```cpp
class Range {
public:
    Range(int lo, int hi) : lo_{lo}, hi_{hi} {
        if (lo_ > hi_) throw std::invalid_argument("lo > hi");
    }
    int lo() const noexcept { return lo_; }
    int hi() const noexcept { return hi_; }
private:
    int lo_;
    int hi_;
};
```
- If construction cannot satisfy the invariant, throw (or use a factory returning
  `std::expected<Range, Error>` / `std::optional` in no-exception code). Avoid two-phase `init()`.
- Members are initialised in **declaration order**, not mem-initializer order. Initialising
  `hi_` from `lo_` when `hi_` is declared first reads garbage. Enable `-Wreorder`.
- Default member initialisers (`int retries_ = 3;`) keep constructors short and consistent.
- Delegating constructors (`Range() : Range(0, 0) {}`) avoid duplication.

## explicit
Mark single-argument constructors (and conversion operators) `explicit` unless implicit
conversion is genuinely the intended semantics (`std::string` from `const char*`):
```cpp
class Meters { public: explicit Meters(double v) : v_{v} {} ... };
void run(Meters m);
run(5.0);            // error, good: was it metres or feet?
run(Meters{5.0});
```
Also `explicit operator bool() const`. Clang-tidy: `google-explicit-constructor`.

## Special members: rule of zero first
Own resources only through RAII members (`std::unique_ptr`, `std::vector`, `std::string`); then
write **none** of destructor/copy/move and the compiler generates correct ones. If you must manage
a resource, define or `= delete` all five. Patterns:
```cpp
class Connection {                      // move-only
public:
    Connection(const Connection&) = delete;
    Connection& operator=(const Connection&) = delete;
    Connection(Connection&&) noexcept = default;
    Connection& operator=(Connection&&) noexcept = default;
};
```
- A user-declared destructor (even `= default`) prevents the implicit move constructor from being declared, so
  copies silently replace moves. Do not add an empty `~T() {}` "for completeness".
- Polymorphic base: public virtual (or protected non-virtual) destructor (C.35), and suppress public copy/move
  to prevent slicing (C.67).
- Move operations should be `noexcept` (C.66).

## Comparisons (C++20)
```cpp
struct Version {
    int major, minor, patch;
    auto operator<=>(const Version&) const = default;   // also gives ==, <, <=, ...
};
```
Hand-write the operators when the member order or semantics differ from what you want compared.

## Other habits
- Accessors `const` and `noexcept` where true; `[[nodiscard]]` on functions whose result must be used.
- Keep data private; avoid setters that let callers break invariants - offer operations instead.
- Non-member non-friend functions for operations that need only the public API (better encapsulation).

## Verify
- [ ] No implicit conversions found by `clang-tidy -checks=google-explicit-constructor`.
- [ ] Each class with an invariant has a constructor test with invalid input.
- [ ] `static_assert(std::is_nothrow_move_constructible_v<T>)` for types stored in vectors.

## Checked

Date: 2026-10-25. Documentation: C++ Core Guidelines (isocpp/CppCoreGuidelines C.2, C.21, C.35, C.42, C.46, C.47, C.66, C.67, C.131) and the C++ working draft (cplusplus/draft classes.tex, head 2026-10-24), clang-tidy check pages (llvm/llvm-project).

Confirmed: class vs struct and invariants (C.2); constructors throw when they cannot establish the invariant (C.42); single-argument constructors explicit (C.46); members initialised in declaration order (C.47); rule of five (C.21); noexcept moves (C.66); polymorphic class copy/move (C.67); trivial getters/setters (C.131); the implicit move constructor is only declared when there is no user-declared copy operation or destructor; `google-explicit-constructor` exists.
Removed as unconfirmed: the `-Wall` membership of `-Wreorder`, `explicit(cond)` remark, hicpp check name, and the default-comparison ordering sentence. `sources` now lists fetched pages.

Method: documentation only; no commands were run.
