---
id: computing-software.software-engineering.cpp.move-semantics-and-perfect-forwarding
name: move-semantics-and-perfect-forwarding
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, move-semantics, rvalue-reference, perfect-forwarding, std-move, universal-reference, forwarding-reference, rule-of-five, copy-elision, std-forward]
level: advanced
status: docs-checked
description: "Use C++ move semantics and perfect forwarding correctly: forwarding references, std::move pitfalls, noexcept moves, and the Rule of Five."
sources: ["https://raw.githubusercontent.com/isocpp/CppCoreGuidelines/master/CppCoreGuidelines.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Move semantics and perfect forwarding — avoid the accidental copy and the dangling move

**Goal:** write constructors/functions that transfer ownership cheaply instead of
copying, and template code that forwards arguments without losing their value
category. Rule numbers below are from the C++ Core Guidelines.

## 1. Rule of Five (C.21)
If you define or `=delete` any copy, move, or destructor function, define or `=delete`
them all. Declaring any of them, even as `=default` or `=delete`, suppresses the
implicit move constructor and move assignment, so potential moves silently become the
more expensive copies. Declaring a move operation makes the implicit copy operations
deleted, which can make a class move-only. Declare the full set deliberately.

## 2. Don't `return std::move(local)` (F.48)
```cpp
S good() { S result; return result; }              // named RVO: elision at best, move at worst
S bad()  { S result; return std::move(result); }   // pessimisation
```
Returning a local variable implicitly moves it anyway; an explicit `std::move` prevents
return value optimisation, which can eliminate the move completely. ES.56 says to
write `std::move()` only when you need to explicitly move an object to another scope.

## 3. Forwarding references (F.19)
```cpp
template<class F, class... Args>
decltype(auto) invoke(F&& f, Args&&... args) { return std::forward<F>(f)(std::forward<Args>(args)...); }
```
For "forward" parameters, pass by `TP&&` where `TP` is a template type parameter, and only
`std::forward` the parameter. `TP&&` ignores and preserves const-ness and rvalue-ness, so
the function is declaring it doesn't care about them but passes the value on to code that
does. Forward the parameter once on each control-flow path. Use `std::move` instead only
for "will-move-from" parameters passed as `X&&` (F.18).

## 4. Make move operations `noexcept` (C.66)
A throwing move violates most people's assumptions, and a non-throwing move will be used
more efficiently by standard-library and language facilities. Mark move constructors
and move assignment `noexcept` where that is true.

## 5. Self-move and moved-from state (C.65)
Make move assignment safe for self-assignment: `x = x` should not change `x`, and a
self-move can arise indirectly, for example through `std::swap(a, b)` where both refer
to the same object. The Guidelines note that the standard guarantees only a
"valid but unspecified" state for moved-from standard-library containers, so do not
depend on a moved-from value being empty.

## Verify
- [ ] Every type that declares any copy, move or destructor function declares or deletes
      all five, rather than relying on implicit suppression.
- [ ] No `return std::move(local)`.
- [ ] Forwarding-reference template parameters are passed on with `std::forward`, not
      `std::move`.
- [ ] Move constructors and move assignment are `noexcept` wherever true, and move
      assignment survives self-assignment.

## Checked
2026-11-01. Confirmed in the C++ Core Guidelines (read from the project's GitHub source):
C.21 (suppression of implicit moves, deleted copies), F.48 (named RVO, explicit move is a
pessimisation), ES.56, F.18, F.19 (`TP&&`, ignores and preserves const-ness and
rvalue-ness, forward once per path, `invoke` example), C.65 (self-move, `std::swap` case,
"valid but unspecified" note), C.66. Removed unconfirmed claims: `std::move` as
`static_cast<T&&>`, guaranteed prvalue elision wording, `vector` reallocation using
`is_nothrow_move_constructible`, moving from `const` objects, and lambda init-capture.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.cpp.raii-and-smart-pointers
