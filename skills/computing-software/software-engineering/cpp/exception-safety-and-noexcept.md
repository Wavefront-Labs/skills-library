---
id: computing-software.software-engineering.cpp.exception-safety-and-noexcept
name: exception-safety-and-noexcept
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, raii, resource-management, exception-safety, noexcept, strong-guarantee, copy-and-swap, move-if-noexcept, destructors]
level: advanced
status: docs-checked
description: "Write exception-safe C++: basic/strong/nothrow guarantees, copy-and-swap, why move constructors must be noexcept for vector, and destructor rules."
sources: ["https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#e-error-handling", "https://github.com/cplusplus/draft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception safety and noexcept

**Goal:** when an exception flies, nothing leaks and objects stay valid; and containers
use fast moves instead of copies.

## The guarantees
| Guarantee | Promise |
|---|---|
| Nothrow | never throws (destructors, swap, move ops, deallocation) |
| Strong | succeeds or has no effect (commit-or-rollback) |
| Basic | no leaks, invariants hold, but state may have changed |
Every function should offer at least basic. RAII gives you most of it automatically:
if every resource is owned by an object, unwinding releases it (Core Guidelines E.6).

## Strong guarantee by doing work on the side
```cpp
void Document::set_lines(std::vector<std::string> lines) {
    auto index = build_index(lines);   // may throw: nothing modified yet
    lines_.swap(lines);                // nothrow commit
    index_.swap(index);
}
```
Copy-and-swap assignment: `T& operator=(T other) noexcept { swap(*this, other); return *this; }`
- strong guarantee, but always copies; often a plain defaulted operator= is fine.

## noexcept matters for performance
`std::move_if_noexcept` yields a copy instead of a move unless the move constructor is `noexcept` (or the type is
not copyable); the standard's `vector` insertion guarantees depend on `T` being CopyInsertable or nothrow move
constructible, so a throwing move constructor can make reallocation copy.
```cpp
Widget(Widget&&) noexcept = default;
Widget& operator=(Widget&&) noexcept = default;
static_assert(std::is_nothrow_move_constructible_v<Widget>);
```

## noexcept rules
- Mark noexcept: move ops (C.66), swap, functions that truly cannot fail (E.12); destructors, deallocation and
  swap must never fail (E.16). Exiting a noexcept function through an exception calls `std::terminate`.
- Don't mark functions noexcept just because they "shouldn't" throw today; it's an API
  promise and removing it later breaks callers that rely on it.
- `noexcept(expr)` conditional specs in templates: `noexcept(noexcept(T(std::declval<T>())))`.

## Destructors
Never let exceptions escape destructors (E.16).
If cleanup can fail (flush, commit), provide an explicit `close()` that reports errors
and have the destructor do best-effort cleanup swallowing errors.

## Exceptions vs error codes
Core Guidelines: use exceptions for errors that the immediate caller can't handle;
error codes (or `std::expected`) where failure is expected and local.

## Verify
- [ ] `static_assert(std::is_nothrow_move_constructible_v<T>)` for types stored in vectors.
- [ ] Fault-injection test (allocator or mock throwing on the Nth call) leaves objects valid and leaks nothing (ASan/LSan).

## Checked

Date: 2026-10-25. Documentation: C++ Core Guidelines (isocpp/CppCoreGuidelines E.6, E.12, E.16, C.66) and the C++ working draft (cplusplus/draft, head 2026-10-24: move_if_noexcept, vector insertion requirements, noexcept termination).

Confirmed: RAII for leaks (E.6); noexcept use (E.12); destructors, deallocation and swap never fail (E.16); noexcept moves (C.66); `std::move_if_noexcept` returns `const T&` unless the move is nothrow or the type is not copy constructible; vector insertion strong guarantee conditions; exiting a noexcept function by exception terminates.
Removed as unconfirmed: the statement that vector always copies on a throwing move (reworded), implicit noexcept of defaulted moves, and the `-fno-exceptions` remark. `sources` now lists fetched pages.

Method: documentation only; no commands were run.
